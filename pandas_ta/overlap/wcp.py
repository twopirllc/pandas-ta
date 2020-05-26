# -*- coding: utf-8 -*-
from ..utils import get_offset, verify_series

def wcp(high, low, close, offset=None, **kwargs):
    """Indicator: Weighted Closing Price (WCP)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)

    # Calculate Result
    wcp = (high + low + 2 * close) / 4

    # Offset
    if offset != 0:
        wcp = wcp.shift(offset)

    # Name & Category
    wcp.name = "WCP"
    wcp.category = 'overlap'

    return wcp



wcp.__doc__ = \
"""Weighted Closing Price (WCP)

Weighted Closing Price is the weighted price given: high, low
and double the close.

Sources:
    https://www.fmlabs.com/reference/default.htm?url=WeightedCloses.htm

Calculation:
    WCP = (2 * close + high + low) / 4

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""