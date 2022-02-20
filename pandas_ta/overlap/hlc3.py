# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.utils import get_offset, verify_series


def hlc3(
    high: Series, low: Series, close: Series, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """HLC3

    HLC3 is the average of high, low and close.

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value). Only works if
            result is offset.
        fill_method (value, optional): Type of fill method. Only works if
            result is offset.

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import TYPPRICE
        hlc3 = TYPPRICE(high, low, close)
    else:
        avg = (high.values + low.values + close.values) / 3.0
        hlc3 = Series(avg, index=close.index)

    # Offset
    if offset != 0:
        hlc3 = hlc3.shift(offset)

        # Fill
        if "fillna" in kwargs:
            hlc3.fillna(kwargs["fillna"], inplace=True)
        if "fill_method" in kwargs:
            hlc3.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    hlc3.name = "HLC3"
    hlc3.category = "overlap"

    return hlc3
