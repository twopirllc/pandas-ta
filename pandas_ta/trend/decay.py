# -*- coding: utf-8 -*-
from math import exp
from pandas import DataFrame
from pandas_ta.utils import get_offset, verify_series


def decay(close, kind=None, length=None, mode=None, offset=None, **kwargs):
    """Indicator: Decay"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 5
    mode = mode.lower() if isinstance(mode, str) else "linear"
    offset = get_offset(offset)

    # Calculate Result
    _mode = "L"
    if mode == "exp" or kind == "exponential":
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

    # Handle fills
    if "fillna" in kwargs:
        ld.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ld.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    ld.name = f"{_mode}DECAY_{length}"
    ld.category = "trend"

    return ld


decay.__doc__ = \
"""Decay

Creates a decay moving forward from prior signals like crosses. The default is
"linear". Exponential is optional as "exponential" or "exp".

Sources:
    https://tulipindicators.org/decay

Calculation:
    Default Inputs:
        length=5, mode=None

    if mode == "exponential" or mode == "exp":
        max(close, close[-1] - exp(-length), 0)
    else:
        max(close, close[-1] - (1 / length), 0)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period. Default: 1
    mamode (str): Option "exponential" ("exp"). Default: 'linear' or None
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
