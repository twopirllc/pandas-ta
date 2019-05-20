# -*- coding: utf-8 -*-
from ..utils import get_offset, verify_series

def mom(close, length=None, offset=None, **kwargs):
    """Indicator: Momentum (MOM)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    offset = get_offset(offset)

    # Calculate Result
    mom = close.diff(length)

    # Offset
    if offset != 0:
        mom = mom.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        mom.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        mom.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    mom.name = f"MOM_{length}"
    mom.category = 'momentum'

    return mom



mom.__doc__ = \
"""Momentum (MOM)

Momentum is an indicator used to measure a security's speed (or strength) of
movement.  Or simply the change in price.

Sources:
    http://www.onlinetradingconcepts.com/TechnicalAnalysis/Momentum.html

Calculation:
    Default Inputs:
        length=1
    MOM = close.diff(length)

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