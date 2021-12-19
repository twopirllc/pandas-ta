# -*- coding: utf-8 -*-
from pandas_ta import Imports
from pandas_ta.utils import get_offset, verify_series
from pandas import Series


def hlc3(high: Series, low: Series, close: Series, talib: bool = None, offset: int = None, **kwargs) -> Series:
    """HLC3

    HLC3 is the average of high, low and close.

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        offset (int): How many periods to offset the result. Default: 0

    Returns:
        pd.Series: New feature generated.
    """
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    # Calculate Result
    if Imports["talib"] and mode_tal:
        from talib import TYPPRICE
        hlc3 = TYPPRICE(high, low, close)
    else:
        hlc3 = (high + low + close) / 3.0

    # Offset
    if offset != 0:
        hlc3 = hlc3.shift(offset)

    # Name & Category
    hlc3.name = "HLC3"
    hlc3.category = "overlap"

    return hlc3
