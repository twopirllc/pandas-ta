# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.utils import v_offset, v_series, v_talib


def wcp(
    high: Series, low: Series, close: Series, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Weighted Closing Price (WCP)

    Weighted Closing Price is the weighted price given: high, low
    and double the close.

    Sources:
        https://www.fmlabs.com/reference/default.htm?url=WeightedCloses.htm

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
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
    high = v_series(high)
    low = v_series(low)
    close = v_series(close)
    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import WCLPRICE
        wcp = WCLPRICE(high, low, close)
    else:
        weight = high.values + low.values + 2 * close.values
        wcp = Series(weight, index=close.index)

    # Offset
    if offset != 0:
        wcp = wcp.shift(offset)

    # Fill
    if "fillna" in kwargs:
        wcp.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        wcp.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    wcp.name = "WCP"
    wcp.category = "overlap"

    return wcp
