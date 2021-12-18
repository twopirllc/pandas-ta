# -*- coding: utf-8 -*-
from pandas_ta.utils import get_offset, verify_series


def hl2(high, low, offset=None, **kwargs):
    """HL2

    HL2 is the midpoint/average of high and low.

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        offset (int): How many periods to offset the result. Default: 0

    Returns:
        pd.Series: New feature generated.
    """
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    offset = get_offset(offset)

    # Calculate Result
    hl2 = 0.5 * (high + low)

    # Offset
    if offset != 0:
        hl2 = hl2.shift(offset)

    # Name & Category
    hl2.name = "HL2"
    hl2.category = "overlap"

    return hl2
