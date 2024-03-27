# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import (
    is_percent,
    v_bool,
    v_drift,
    v_offset,
    v_pos_default,
    v_series
)



def decreasing(
    close: Series, length: Int = None, strict: bool = None,
    asint: bool = None, percent: IntFloat = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Decreasing

    Returns True if the series is decreasing over a period, False otherwise.
    If the kwarg 'strict' is True, it returns True if it is continuously
    decreasing over the period. When using the kwarg 'asint', then it
    returns 1 for True or 0 for False.

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 1
        strict (bool): If True, checks if the series is continuously
            decreasing over the period. Default: False
        percent (float): Percent as an integer. Default: None
        asint (bool): Returns as binary. Default: True
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 1)
    close = v_series(close, length)

    if close is None:
        return

    strict = v_bool(strict, False)
    asint = v_bool(asint, True)
    percent = float(percent) if is_percent(percent) else False
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    close_ = (1 - 0.01 * percent) * close if percent else close
    if strict:
        # Returns value as float64? Have to cast to bool
        decreasing = close < close_.shift(drift)
        for x in range(3, length + 1):
            decreasing &= (close.shift(x - (drift + 1)) < close_.shift(x - drift))

        decreasing.fillna(0, inplace=True)
        decreasing = decreasing.astype(bool)
    else:
        decreasing = close_.diff(length) < 0

    if asint:
        decreasing = decreasing.astype(int)

    # Offset
    if offset != 0:
        decreasing = decreasing.shift(offset)

    # Fill
    if "fillna" in kwargs:
        decreasing.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _percent = f"_{0.01 * percent}" if percent else ''
    _props = f"{'S' if strict else ''}DEC{'p' if percent else ''}"
    decreasing.name = f"{_props}_{length}{_percent}"
    decreasing.category = "trend"

    return decreasing
