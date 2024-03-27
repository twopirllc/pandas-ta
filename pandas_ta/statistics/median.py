# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_pos_default, v_series



def median(
    close: Series, length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Rolling Median

    Calculates the Median over a rolling period.

    Sources:
        https://www.incrediblecharts.com/indicators/median_price.php

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 30
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 30)
    if "min_periods" in kwargs and kwargs["min_periods"] is not None:
        min_periods = int(kwargs["min_periods"])
    else:
        min_periods = length
    close = v_series(close, max(length, min_periods))

    if close is None:
        return

    offset = v_offset(offset)

    # Calculate
    median = close.rolling(length, min_periods=min_periods).median()

    # Offset
    if offset != 0:
        median = median.shift(offset)

    # Fill
    if "fillna" in kwargs:
        median.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    median.name = f"MEDIAN_{length}"
    median.category = "statistics"

    return median
