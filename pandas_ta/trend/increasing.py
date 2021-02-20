# -*- coding: utf-8 -*-
from pandas_ta.utils import get_offset, verify_series


def increasing(close, length=None, strict=None, asint=None, offset=None, **kwargs):
    """Indicator: Increasing"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 1
    strict = strict if isinstance(strict, bool) else False
    asint = asint if isinstance(asint, bool) else True
    offset = get_offset(offset)

    def stricly_increasing(series, n):
        return all([i < j for i,j in zip(series[-n:], series[1:])])

    # Calculate Result
    if strict:
        # Returns value as float64? Have to cast to bool
        increasing = close.rolling(length, min_periods=length).apply(stricly_increasing, args=(length,), raw=False)
        increasing.fillna(0, inplace=True)
        increasing = increasing.astype(bool)
    else:
        increasing = close.diff(length) > 0

    if asint:
        increasing = increasing.astype(int)

    # Offset
    if offset != 0:
        increasing = increasing.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        increasing.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        increasing.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    increasing.name = f"{'S' if strict else ''}INC_{length}"
    increasing.category = "trend"

    return increasing


increasing.__doc__ = \
"""Increasing

Returns True if the series is increasing over a period, False otherwise.
If the kwarg 'strict' is True, it returns True if it is continuously increasing
over the period. When using the kwarg 'asint', then it returns 1 for True
or 0 for False. 

Calculation:
    if strict:
        increasing = all(i < j for i, j in zip(close[-length:], close[1:]))
    else:
        increasing = close.diff(length) > 0

    if asint:
        increasing = increasing.astype(int)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period. Default: 1
    asint (bool): Returns as binary. Default: True
    strict (bool): If True, checks if the series is continuously increasing over the period. Default: False
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
