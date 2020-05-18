# -*- coding: utf-8 -*-
from ..utils import get_offset, verify_series

def wcp(high, low, close, offset=None, **kwargs):
    """Indicator: WCP"""
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