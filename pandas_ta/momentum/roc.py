# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.maps import Imports
from pandas_ta.utils import get_offset, verify_series
from .mom import mom


def roc(
        close: Series, length: int = None,
        scalar: float = None, talib: bool = None,
        offset: int = None, **kwargs
    ) -> Series:
    """Rate of Change (ROC)

    Rate of Change is an indicator is also referred to as Momentum (yeah, confusingly).
    It is a pure momentum oscillator that measures the percent change in price with the
    previous price 'n' (or length) periods ago.

    Sources:
        https://www.tradingview.com/wiki/Rate_of_Change_(ROC)

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 1
        scalar (float): How much to magnify. Default: 100
        talib (bool): If TA Lib is installed and talib is True, Returns the TA Lib
            version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 10
    scalar = float(scalar) if scalar and scalar > 0 else 100
    close = verify_series(close, length)
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if close is None: return

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import ROC
        roc = ROC(close, length)
    else:
        roc = scalar * mom(close=close, length=length, talib=mode_tal) / close.shift(length)

    # Offset
    if offset != 0:
        roc = roc.shift(offset)

    # Fill
    if "fillna" in kwargs:
        roc.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        roc.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    roc.name = f"ROC_{length}"
    roc.category = "momentum"

    return roc
