# -*- coding: utf-8 -*-
from pandas_ta import Imports
from pandas_ta.utils import get_offset, verify_series


def hlc3(high, low, close, talib=None, offset=None, **kwargs):
    """HLC3

    Calculation:
        HLC3 = (high + low + close) / 3.0

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's

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
