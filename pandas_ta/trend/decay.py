# -*- coding: utf-8 -*-
from numpy import exp
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_pos_default, v_series, v_str


def decay(
    close: Series, length: Int = None, mode: str = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Decay

    Creates a decay moving forward from prior signals like crosses.
    The default is "linear".
    Exponential is optional as "exponential" or "exp".

    Sources:
        https://tulipindicators.org/decay

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 1
        mode (str): If 'exp' then "exponential" decay. Default: 'linear'
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

    mode = v_str(mode, "linear")
    offset = v_offset(offset)

    # Calculate
    _mode = "L"
    if mode in ["exp", "exponential"]:
        _mode = "EXP"
        diff = close.shift(1) - exp(-length)
    else:  # "linear"
        diff = close.shift(1) - (1 / length)
    diff[0] = close[0]
    tdf = DataFrame({"close": close, "diff": diff, "0": 0})
    ld = tdf.max(axis=1)

    # Offset
    if offset != 0:
        ld = ld.shift(offset)

    # Fill
    if "fillna" in kwargs:
        ld.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ld.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    ld.name = f"{_mode}DECAY_{length}"
    ld.category = "trend"

    return ld
