# -*- coding: utf-8 -*-
# from numpy.version import version as np_version
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import (
    pascals_triangle,
    v_offset,
    v_ascending,
    v_pos_default,
    v_series,
    weights
)



def pwma(
    close: Series, length: Int = None, asc: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Pascal's Weighted Moving Average (PWMA)

    Pascal's Weighted Moving Average is similar to a symmetric triangular
    window except PWMA's weights are based on Pascal's Triangle.

    Source: Kevin Johnson

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period.  Default: 10
        asc (bool): Recent values weigh more. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 10)
    close = v_series(close, length)

    if close is None:
        return

    asc = v_ascending(asc)
    offset = v_offset(offset)

    # Calculate
    triangle = pascals_triangle(n=length - 1, weighted=True)
    pwma = close.rolling(length, min_periods=length) \
        .apply(weights(triangle), raw=True)

    # Offset
    if offset != 0:
        pwma = pwma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        pwma.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    pwma.name = f"PWMA_{length}"
    pwma.category = "overlap"

    return pwma
