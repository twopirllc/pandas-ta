# -*- coding: utf-8 -*-
from numpy import isnan
from pandas import DataFrame, Series
from pandas_ta.ma import ma
from pandas_ta.overlap import hlc3
from pandas_ta.utils import get_drift, get_offset, signed_series, verify_series


def kvo(
        high: Series, low: Series, close: Series, volume: Series,
        fast: int = None, slow: int = None, signal=None,
        mamode: str = None, drift: int = None,
        offset: int = None, **kwargs
    ) -> DataFrame:
    """Klinger Volume Oscillator (KVO)

    This indicator was developed by Stephen J. Klinger. It is designed to predict
    price reversals in a market by comparing volume to price.

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
        mamode (str): See ```help(ta.ma)```. Default: 'ema'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: KVO and Signal columns.
    """
    # Validate
    fast = int(fast) if fast and fast > 0 else 34
    slow = int(slow) if slow and slow > 0 else 55
    signal = int(signal) if signal and signal > 0 else 13
    mamode = mamode.lower() if mamode and isinstance(mamode, str) else "ema"
    _length = slow - 1
    high = verify_series(high, _length)
    low = verify_series(low, _length)
    close = verify_series(close, _length)
    volume = verify_series(volume, _length)
    drift = get_drift(drift)
    offset = get_offset(offset)

    if high is None or low is None or close is None or volume is None: return

    # Calculate
    signed_volume = volume * signed_series(hlc3(high, low, close), 1)
    sv = signed_volume.loc[signed_volume.first_valid_index():,]
    kvo = ma(mamode, sv, length=fast) - ma(mamode, sv, length=slow)
    if kvo is None or all(isnan(kvo.values)): return  # Emergency Break
    kvo_signal = ma(mamode, kvo.loc[kvo.first_valid_index():,], length=signal)
    if kvo_signal is None or all(isnan(kvo_signal.values)): return  # Emergency Break

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
