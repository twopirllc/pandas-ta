# -*- coding: utf-8 -*-
from numpy import log as nplog
from numpy import NaN as npNaN
from pandas import Series
from ..overlap.hl2 import hl2
from ..utils import get_offset, verify_series, zero

def fisher(high, low, length=None, offset=None, **kwargs):
    """Indicator: Fisher Transform (FISHT)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    length = int(length) if length and length > 0 else 5
    offset = get_offset(offset)

    # Calculate Result
    m = high.size
    hl2_ = hl2(high, low)
    max_high = hl2_.rolling(length).max()
    min_low = hl2_.rolling(length).min()
    hl2_range = max_high - min_low
    hl2_range[hl2_range < 1e-5] = 0.001
    position = (hl2_ - min_low) / hl2_range
    
    v = 0
    fish = 0
    result = [npNaN for _ in range(0, length - 1)]
    for i in range(length - 1, m):
        v = 0.66 * (position[i] - 0.5) + 0.67 * v
        if v >  0.99: v =  0.999
        if v < -0.99: v = -0.999
        fish = 0.5 * (fish + nplog((1 + v) / (1 - v)))
        result.append(fish)
        
    fisher = Series(result)

    # Offset
    if offset != 0:
        fisher = fisher.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        fisher.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        fisher.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    fisher.name = f"FISHERT_{length}"
    fisher.category = 'momentum'

    return fisher



fisher.__doc__ = \
"""Fisher Transform (FISHT)

Attempts to identify trend reversals.

Sources:
    https://tulipindicators.org/fisher

Calculation:
    Default Inputs:
        drift=1

Args:
    close (pd.Series): Series of 'close's
    drift (int): The short period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""