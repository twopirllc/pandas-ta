# -*- coding: utf-8 -*-
from numpy import array as npArray
from numpy import arange as npArange
from numpy import polyfit as npPolyfit
from numpy import std as npStd
from pandas import DataFrame, DatetimeIndex, Series
# from pandas_ta import Imports
from .stdev import stdev as stdev
from pandas_ta.utils import get_offset, verify_series

def tos_stdevall(close, length=None, stds=None, ddof=None, offset=None, **kwargs):
    """Indicator: TD Ameritrade's Think or Swim Standard Deviation All"""
    # Validate Arguments
    stds = stds if isinstance(stds, list) and len(stds) > 0 else [1, 2, 3]
    if min(stds) <= 0: return
    if not all(i < j for i, j in zip(stds, stds[1:])):
        stds = stds[::-1]
    ddof = int(ddof) if ddof and ddof >= 0 and ddof < length else 1
    offset = get_offset(offset)

    if length is None:
        length = close.size
        _props = f"STDEVALL"
    else:
        length = int(length) if length and length > 2 else 30
        close = close.iloc[-length:]
        _props = f"STDEVALL_{length}"

    close = verify_series(close, length)

    if close is None: return

    # Calculate Result
    if isinstance(close.index, DatetimeIndex):
        close_ = npArray(close)
        np_index = npArange(length)
        m, b = npPolyfit(np_index, close_, 1)
        lr_ = m * np_index + b
    else:
        m, b = npPolyfit(close.index, close, 1)
        lr_ = m * close.index + b

    lr = Series(lr_, index=close.index)
    stdevall = stdev(Series(close), length=length, ddof=ddof)
    # std = npStd(close, ddof=ddof)

    # Name and Categorize it
    df = DataFrame({f"{_props}_LR": lr}, index=close.index)
    for i in stds:
        df[f"{_props}_L_{i}"] = lr - i * stdevall.iloc[-1]
        df[f"{_props}_U_{i}"] = lr + i * stdevall.iloc[-1]
        df[f"{_props}_L_{i}"].name = df[f"{_props}_U_{i}"].name = f"{_props}"
        df[f"{_props}_L_{i}"].category = df[f"{_props}_U_{i}"].category = "statistics"

    # Offset
    if offset != 0:
        df = df.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        df.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        df.fillna(method=kwargs["fill_method"], inplace=True)

    # Prepare DataFrame to return
    df.name = f"{_props}"
    df.category = "statistics"

    return df


tos_stdevall.__doc__ = \
"""TD Ameritrade's Think or Swim Standard Deviation All (TOS_STDEV)

**UNDER DEVELOPMENT**

A port of TD Ameritrade's Think or Swim Standard Deviation All indicator which
returns the standard deviation of data for the entire plot or for the interval
of the last bars defined by the length parameter.

Sources:
    https://tlc.thinkorswim.com/center/reference/thinkScript/Functions/Statistical/StDevAll

Calculation:
    Default Inputs:
        length=30
    VAR = Variance
    STDEV = variance(close, length).apply(np.sqrt)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period. Default: 30
    ddof (int): Delta Degrees of Freedom.
                The divisor used in calculations is N - ddof,
                where N represents the number of elements. Default: 1
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
