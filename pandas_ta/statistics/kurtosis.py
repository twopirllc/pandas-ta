# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_pos_default, v_series


def kurtosis(
    close: Series, length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Rolling Kurtosis

    Calculates the Kurtosis over a rolling period.

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 30
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

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
    kurtosis = close.rolling(length, min_periods=min_periods).kurt()

    # Offset
    if offset != 0:
        kurtosis = kurtosis.shift(offset)

    # Fill
    if "fillna" in kwargs:
        kurtosis.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        kurtosis.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    kurtosis.name = f"KURT_{length}"
    kurtosis.category = "statistics"

    return kurtosis
