# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.utils import get_offset, verify_series


def hl2(
    high: Series, low: Series,
    offset: int = None, **kwargs
) -> Series:
    """HL2

    HL2 is the midpoint/average of high and low.

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        offset (int): How many periods to offset the result. Default: 0

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    high = verify_series(high)
    low = verify_series(low)
    offset = get_offset(offset)

    # Calculate
    hl2 = Series(0.5 * (high.values + low.values), index=high.index)

    # Offset
    if offset != 0:
        hl2 = hl2.shift(offset)

    # Name and Category
    hl2.name = "HL2"
    hl2.category = "overlap"

    return hl2
