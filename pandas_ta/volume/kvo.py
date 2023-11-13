# -*- coding: utf-8 -*-
from numpy import isnan
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.overlap import hlc3
from pandas_ta.utils import (
    signed_series,
    v_drift,
    v_mamode,
    v_offset,
    v_pos_default,
    v_series
)


def kvo(
    high: Series, low: Series, close: Series, volume: Series,
    fast: Int = None, slow: Int = None, signal: Int = None,
    mamode: str = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Klinger Volume Oscillator (KVO)

    This indicator was developed by Stephen J. Klinger. It attempts to
    predict price reversals in a market by comparing volume to price.

    Sources:
        https://www.investopedia.com/terms/k/klingeroscillator.asp
        https://www.daytrading.com/klinger-volume-oscillator

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        fast (int): The fast period. Default: 34
        slow (int): The slow period. Default: 55
        signal (int): The signal period. Default: 13
        mamode (str): See ``help(ta.ma)``. Default: 'ema'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: KVO and Signal columns.
    """
    # Validate
    fast = v_pos_default(fast, 34)
    slow = v_pos_default(slow, 55)
    signal = v_pos_default(signal, 13)
    _length = max(fast, slow) + signal
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)
    volume = v_series(volume, _length)

    if high is None or low is None or close is None or volume is None:
        return

    mamode = v_mamode(mamode, "ema")
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate Trend (T) and Trend groups (dtrend)
    trend = signed_series(hlc3(high, low, close), 1)
    dtrend = trend.diff().ne(0).cumsum()

    # Calculate the Daily Measurement (dm)
    dm = high - low

    # Calculate the Cumulative Measurement (cm)
    df = DataFrame({'dtrend': dtrend, 'dm': dm})
    df['dm_cumsum'] = df.groupby('dtrend')['dm'].cumsum()
    mask = df['dtrend'].ne(df['dtrend'].shift())
    df.loc[mask, 'previous_dm'] = df['dm'].shift()
    df['previous_dm'].ffill(inplace=True)
    cm = df['dm_cumsum'].add(df['previous_dm'], fill_value=0)

    # Avoid division by zero by adding a small number to 'cm' where it's zero
    cm += cm.where(cm == 0, 1e-10)

    # Calculate the Volume Force (VF)
    vf = volume * (2 * ((dm / cm) - 1)) * trend * 100

    kvo = ma(mamode, vf, length=fast) - ma(mamode, vf, length=slow)
    kvo_signal = ma(mamode, kvo.loc[kvo.first_valid_index():,], length=signal)

    if kvo is None or all(isnan(kvo.values)):
        return  # Emergency Break

    kvo_signal = ma(mamode, kvo.loc[kvo.first_valid_index():, ], length=signal)
    if kvo_signal is None or all(isnan(kvo_signal.values)):
        return  # Emergency Break

    # Offset
    if offset != 0:
        kvo = kvo.shift(offset)
        kvo_signal = kvo_signal.shift(offset)

    # Fill
    if "fillna" in kwargs:
        kvo.fillna(kwargs["fillna"], inplace=True)
        kvo_signal.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        kvo.fillna(method=kwargs["fill_method"], inplace=True)
        kvo_signal.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _props = f"_{fast}_{slow}_{signal}"
    kvo.name = f"KVO{_props}"
    kvo_signal.name = f"KVOs{_props}"
    kvo.category = kvo_signal.category = "volume"

    data = {kvo.name: kvo, kvo_signal.name: kvo_signal}
    df = DataFrame(data, index=close.index)
    df.name = f"KVO{_props}"
    df.category = kvo.category

    return df
