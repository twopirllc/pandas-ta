# -*- coding: utf-8 -*-
from ..utils import get_offset, verify_series

def rma(close, length=None, offset=None, **kwargs):
    """Indicator: wildeR's Moving Average (RMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)
    alpha = (1.0 / length) if length > 0 else 0.5

    # Calculate Result
    rma = close.ewm(alpha=alpha, min_periods=min_periods).mean()

    # Offset
    if offset != 0:
        rma = rma.shift(offset)

    # Name & Category
    rma.name = f"RMA_{length}"
    rma.category = 'overlap'

    return rma



rma.__doc__ = \
"""wildeR's Moving Average (RMA)

The WildeR's Moving Average is simply an Exponential Moving Average (EMA)
with a modified alpha = 1 / length.

Sources:
    https://alanhull.com/hull-moving-average

Calculation:
    Default Inputs:
        length=10
    EMA = Exponential Moving Average
    alpha = 1 / length
    RMA = EMA(close, alpha=alpha)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""