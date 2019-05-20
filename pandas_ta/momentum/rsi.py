# -*- coding: utf-8 -*-
from ..utils import get_drift, get_offset, verify_series

def rsi(close, length=None, drift=None, offset=None, **kwargs):
    """Indicator: Relative Strength Index (RSI)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    negative = close.diff(drift)
    positive = negative.copy()

    positive[positive < 0] = 0  # Make negatives 0 for the postive series
    negative[negative > 0] = 0  # Make postives 0 for the negative series

    positive_avg = positive.ewm(com=length, adjust=False).mean()
    negative_avg = negative.ewm(com=length, adjust=False).mean().abs()

    rsi = 100 * positive_avg / (positive_avg + negative_avg)

    # Offset
    if offset != 0:
        rsi = rsi.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        rsi.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        rsi.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    rsi.name = f"RSI_{length}"
    rsi.category = 'momentum'

    return rsi



rsi.__doc__ = \
"""Relative Strength Index (RSI)

The Relative Strength Index is popular momentum oscillator used to measure the
velocity as well as the magnitude of directional price movements.

Sources:
    https://www.tradingview.com/wiki/Relative_Strength_Index_(RSI)

Calculation:
    Default Inputs:
        length=14, drift=1
    ABS = Absolute Value
    EMA = Exponential Moving Average
    positive = close if close.diff(drift) > 0 else 0
    negative = close if close.diff(drift) < 0 else 0
    pos_avg = EMA(positive, length)
    neg_avg = ABS(EMA(negative, length))
    RSI = 100 * pos_avg / (pos_avg + neg_avg)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""