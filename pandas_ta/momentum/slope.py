# -*- coding: utf-8 -*-
from numpy import arctan, pi
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_bool, v_offset, v_pos_default, v_series


def slope(
    close: Series, length: Int = None,
    as_angle: bool = None, to_degrees: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Slope

    Returns the slope of a series of length n. Can convert the slope to angle.
    Default: slope.

    Source: Algebra

    Calculation:
        Default Inputs:
            length=1
        slope = close.diff(length) / length

        if as_angle:
            slope = slope.apply(atan)
            if to_degrees:
                slope *= 180 / PI

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 1
        as_angle (value, optional): Converts slope to an angle. Default: False
        to_degrees (value, optional): Converts slope angle to degrees.
            Default: False
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 1)
    close = v_series(close, length)

    if close is None:
        return

    as_angle = v_bool(as_angle, False)
    to_degrees = v_bool(to_degrees, False)
    offset = v_offset(offset)

    # Calculate
    slope = close.diff(length) / length
    if as_angle:
        slope = slope.apply(arctan)
        if to_degrees:
            slope *= 180 / pi

    # Offset
    if offset != 0:
        slope = slope.shift(offset)

    # Fill
    if "fillna" in kwargs:
        slope.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        slope.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    slope.name = f"SLOPE_{length}" if not as_angle else f"ANGLE{'d' if to_degrees else 'r'}_{length}"
    slope.category = "momentum"

    return slope
