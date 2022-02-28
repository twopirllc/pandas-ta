# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_series


def hl2(
    high: Series, low: Series,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """HL2

    HL2 is the midpoint/average of high and low.

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
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
    high = v_series(high)
    low = v_series(low)
    offset = v_offset(offset)

    # Calculate
    avg = 0.5 * (high.values + low.values)
    hl2 = Series(avg, index=high.index)

    # Offset
    if offset != 0:
        hl2 = hl2.shift(offset)

        # Fill
        if "fillna" in kwargs:
            hl2.fillna(kwargs["fillna"], inplace=True)
        if "fill_method" in kwargs:
            hl2.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    hl2.name = "HL2"
    hl2.category = "overlap"

    return hl2
