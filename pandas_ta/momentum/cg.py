# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_pos_default, v_series, weights



def cg(
    close: Series, length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Center of Gravity (CG)

    The Center of Gravity Indicator by John Ehlers attempts to identify
    turning points while exhibiting zero lag and smoothing.

    Sources:
        http://www.mesasoftware.com/papers/TheCGOscillator.pdf

    Args:
        close (pd.Series): Series of 'close's
        length (int): The length of the period. Default: 10
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

    offset = v_offset(offset)

    # Calculate
    coefficients = range(1, length + 1)
    numerator = close.rolling(length).apply(weights(coefficients), raw=True)
    cg = -numerator / close.rolling(length).sum()

    # Offset
    if offset != 0:
        cg = cg.shift(offset)

    # Fill
    if "fillna" in kwargs:
        cg.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    cg.name = f"CG_{length}"
    cg.category = "momentum"

    return cg
