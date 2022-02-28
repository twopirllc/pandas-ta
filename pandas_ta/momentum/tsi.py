# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.ma import ma
from pandas_ta.overlap import ema
from pandas_ta.utils import v_drift, v_mamode, v_offset
from pandas_ta.utils import v_pos_default, v_scalar, v_series


def tsi(
    close: Series, fast: Int = None, slow: Int = None,
    signal: Int = None, scalar: IntFloat = None,
    mamode: str = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """True Strength Index (TSI)

    The True Strength Index is a momentum indicator used to identify
    short-term swings while in the direction of the trend as well as
    determining overbought and oversold conditions.

    Sources:
        https://www.investopedia.com/terms/t/tsi.asp

    Args:
        close (pd.Series): Series of 'close's
        fast (int): The short period. Default: 13
        slow (int): The long period. Default: 25
        signal (int): The signal period. Default: 13
        scalar (float): How much to magnify. Default: 100
        mamode (str): Moving Average of TSI Signal Line.
            See ``help(ta.ma)``. Default: 'ema'
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: tsi, signal.
    """
    # Validate
    fast = v_pos_default(fast, 13)
    slow = v_pos_default(slow, 25)
    close = v_series(close, max(fast, slow))
    if "length" in kwargs:
        kwargs.pop("length")

    if close is None:
        return

    signal = v_pos_default(signal, 13)
    scalar = v_scalar(scalar, 100)
    mamode = v_mamode(mamode, "ema")
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    diff = close.diff(drift)
    slow_ema = ema(close=diff, length=slow, **kwargs)
    fast_slow_ema = ema(close=slow_ema, length=fast, **kwargs)

    abs_diff = diff.abs()
    abs_slow_ema = ema(close=abs_diff, length=slow, **kwargs)
    abs_fast_slow_ema = ema(close=abs_slow_ema, length=fast, **kwargs)

    tsi = scalar * fast_slow_ema / abs_fast_slow_ema
    tsi_signal = ma(mamode, tsi, length=signal)

    # Offset
    if offset != 0:
        tsi = tsi.shift(offset)
        tsi_signal = tsi_signal.shift(offset)

    # Fill
    if "fillna" in kwargs:
        tsi.fillna(kwargs["fillna"], inplace=True)
        tsi_signal.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        tsi.fillna(method=kwargs["fill_method"], inplace=True)
        tsi_signal.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    tsi.name = f"TSI_{fast}_{slow}_{signal}"
    tsi_signal.name = f"TSIs_{fast}_{slow}_{signal}"
    tsi.category = tsi_signal.category = "momentum"

    df = DataFrame({tsi.name: tsi, tsi_signal.name: tsi_signal})
    df.name = f"TSI_{fast}_{slow}_{signal}"
    df.category = "momentum"

    return df
