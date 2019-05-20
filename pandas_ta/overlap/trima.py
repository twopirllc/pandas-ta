# -*- coding: utf-8 -*-
from ..utils import get_offset, verify_series

def trima(close, length=None, offset=None, **kwargs):
    """Indicator: Triangular Moving Average (TRIMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    half_length = round(0.5 * (length + 1))
    sma1 = close.rolling(half_length, min_periods=half_length).mean()
    trima = sma1.rolling(half_length, min_periods=half_length).mean()

    # Offset
    if offset != 0:
        trima = trima.shift(offset)

    # Name & Category
    trima.name = f"TRIMA_{length}"
    trima.category = 'overlap'

    return trima



trima.__doc__ = \
"""Triangular Moving Average (TRIMA)

A weighted moving average where the shape of the weights are triangular and the
greatest weight is in the middle of the period.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/triangular-moving-average-trima/
    tma = sma(sma(src, ceil(length / 2)), floor(length / 2) + 1)  # Tradingview
    trima = sma(sma(x, n), n)  # Tradingview

Calculation:
    Default Inputs:
        length=10
    SMA = Simple Moving Average
    half_length = math.round(0.5 * (length + 1))
    SMA1 = SMA(close, half_length)
    TRIMA = SMA(SMA1, half_length)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    adjust (bool): Default: True
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""