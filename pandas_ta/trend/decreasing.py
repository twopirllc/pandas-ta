# -*- coding: utf-8 -*-
from ..utils import get_offset, verify_series

def decreasing(close, length=None, asint=True, offset=None, **kwargs):
    """Indicator: Decreasing"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    decreasing = close.diff(length) < 0
    if asint:
        decreasing = decreasing.astype(int)

    # Offset
    if offset != 0:
        decreasing = decreasing.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        decreasing.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        decreasing.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    decreasing.name = f"DEC_{length}"
    decreasing.category = 'trend'

    return decreasing



decreasing.__doc__ = \
"""Decreasing

Returns True or False if the series is decreasing over a periods.  By default,
it returns True and False as 1 and 0 respectively with kwarg 'asint'.

Sources:

Calculation:
    decreasing = close.diff(length) < 0
    if asint:
        decreasing = decreasing.astype(int)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    asint (bool): Returns as binary.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""