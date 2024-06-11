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

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    high = v_series(high)
    low = v_series(low)
    offset = v_offset(offset)

    if high is None or low is None:
        return

    # Calculate
    avg = 0.5 * (high.to_numpy() + low.to_numpy())
    hl2 = Series(avg, index=high.index)

    # Offset
    if offset != 0:
        hl2 = hl2.shift(offset)

        # Fill
        if "fillna" in kwargs:
            hl2.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    hl2.name = "HL2"
    hl2.category = "overlap"

    return hl2
