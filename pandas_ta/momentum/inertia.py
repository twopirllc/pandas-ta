# -*- coding: utf-8 -*-
from .rvi import rvi
from pandas_ta.overlap import linreg
from pandas_ta.utils import get_offset, non_zero_range, verify_series

def inertia(open_, high, low, close, length=None, swma_length=None, offset=None, **kwargs):
    """Indicator: Inertia (INERTIA)"""
    # Validate Arguments
    open_ = verify_series(open_)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    swma_length = int(swma_length) if swma_length and swma_length > 0 else 4
    offset = get_offset(offset)

    # Calculate Result
    rvidf = rvi(open_, high, low, close, length=length, swma_length=swma_length)
    inertia = linreg(rvidf[rvidf.columns[0]], length=length)

    # Offset
    if offset != 0:
        inertia = inertia.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        inertia.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        inertia.fillna(method=kwargs['fill_method'], inplace=True)

    # Name & Category
    inertia.name = f"INERTIA_{length}_{swma_length}"
    inertia.category = "momentum"

    return inertia



inertia.__doc__ = \
"""Inertia (INERTIA)

Inertia was developed by Donald Dorsey and was introduced his article
in September, 1995. It is the Relative Vigor Index smoothed by the Least
Squares Moving Average. Postive Inertia when values are greater than 50,
Negative Inertia otherwise.

Sources:
    https://www.investopedia.com/terms/r/relative_vigor_index.asp

Calculation:
    Default Inputs:
        length=14, swma_length=4
    LSQRMA = Least Squares Moving Average

    INERTIA = LSQRMA(RVI)

Args:
    open_ (pd.Series): Series of 'open's
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 14
    swma_length (int): It's period.  Default: 4
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""