# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.ma import ma
from pandas_ta.maps import Imports
from pandas_ta.utils import get_drift, get_offset, verify_series
from .true_range import true_range


def atr(
    high: Series, low: Series, close: Series, length: int = None,
    mamode: str = None, talib: bool = None, drift: int = None,
    offset: int = None, **kwargs
) -> Series:
    """Average True Range (ATR)

    Averge True Range is used to measure volatility, especially volatility caused by
    gaps or limit moves.

    Sources:
        https://www.tradingview.com/wiki/Average_True_Range_(ATR)

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        mamode (str): See ```help(ta.ma)```. Default: 'rma'
        talib (bool): If TA Lib is installed and talib is True, Returns the TA Lib
            version. Default: True
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        percent (bool, optional): Return as percentage. Default: False
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 14
    mamode = mamode.lower() if mamode and isinstance(mamode, str) else "rma"
    high = verify_series(high, length)
    low = verify_series(low, length)
    close = verify_series(close, length)
    drift = get_drift(drift)
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if high is None or low is None or close is None:
        return

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import ATR
        atr = ATR(high, low, close, length)
    else:
        tr = true_range(
            high=high,
            low=low,
            close=close,
            drift=drift,
            talib=mode_tal)
        atr = ma(mamode, tr, length=length, talib=mode_tal)

    percentage = kwargs.pop("percent", False)
    if percentage:
        atr *= 100 / close

    # Offset
    if offset != 0:
        atr = atr.shift(offset)

    # Fill
    if "fillna" in kwargs:
        atr.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        atr.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    atr.name = f"ATR{mamode[0]}_{length}{'p' if percentage else ''}"
    atr.category = "volatility"

    return atr
