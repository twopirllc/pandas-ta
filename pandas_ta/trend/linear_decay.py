# -*- coding: utf-8 -*-
from pandas import DataFrame
from ..utils import get_offset, verify_series

def linear_decay(close, length=None, offset=None, **kwargs):
    """Indicator: Linear Decay"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 5
    offset = get_offset(offset)

    # Calculate Result
    diff = close.shift(1) - (1 / length)
    diff[0] = close[0]
    tdf = DataFrame({'close': close, 'diff': diff, '0': 0})
    ld = tdf.max(axis=1)

    # Offset
    if offset != 0:
        ld = ld.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        ld.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        ld.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    ld.name = f"LDECAY_{length}"
    ld.category = 'trend'

    return ld



linear_decay.__doc__ = \
"""Linear Decay

Adds a linear decay moving forward from prior signals like crosses.

Sources:
    https://tulipindicators.org/decay

Calculation:
    Default Inputs:
        length=5
    max(close, close[-1] - (1 / length), 0)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""