# -*- coding: utf-8 -*-
from ..overlap.swma import swma
from ..utils import get_offset, verify_series

def rvi(open_, high, low, close, length=None, swma_length=None, offset=None, **kwargs):
    """Indicator: RVI"""
    # Validate Arguments
    open_ = verify_series(open_)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    swma_length = int(swma_length) if swma_length and swma_length > 0 else 4
    offset = get_offset(offset)

    # Calculate Result
    numerator = swma(close - open_, length=swma_length).rolling(length).sum()
    denominator = swma(high - low, length=swma_length).rolling(length).sum()
    
    rvi = numerator / denominator

    # Offset
    if offset != 0:
        rvi = rvi.shift(offset)

    # Name & Category
    rvi.name = f"RVI_{length}_{swma_length}"
    rvi.category = 'momentum'

    return rvi



rvi.__doc__ = \
"""Relative Vigor Index (RVI)

The Relative Vigor Index attempts to measure the strength of a trend relative to
its closing price to its trading range.  It is based on the belief that it tends 
to close higher than they open in uptrends or close lower than they open in
downtrends.

Sources:
    https://www.investopedia.com/terms/r/relative_vigor_index.asp

Calculation:
    Default Inputs:
        length=14, swma_length=4
    SWMA = Symmetrically Weighted Moving Average
    numerator = SUM(SWMA(close - open, swma_length), length)
    denominator = SUM(SWMA(high - low, swma_length), length)
    RVI = numerator / denominator

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