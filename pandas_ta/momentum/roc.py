# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.maps import Imports
from pandas_ta.utils import v_offset, v_pos_default, v_scalar
from pandas_ta.utils import v_series, v_talib
from .mom import mom


def roc(
    close: Series, length: Int = None,
    scalar: IntFloat = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Rate of Change (ROC)

    Rate of Change is an indicator is also referred to as Momentum
    (yeah, confusingly). It is a pure momentum oscillator that measures the
    percent change in price with the previous price 'n' (or length)
    periods ago.

    Sources:
        https://www.tradingview.com/wiki/Rate_of_Change_(ROC)

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 1
        scalar (float): How much to magnify. Default: 100
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 10)
    close = v_series(close, length)

    if close is None:
        return

    scalar = v_scalar(scalar, 100)
    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import ROC
        roc = ROC(close, length)
    else:
        roc = scalar * mom(close=close, length=length, talib=mode_tal)
        roc /= close.shift(length)

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
