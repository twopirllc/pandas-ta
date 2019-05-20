# -*- coding: utf-8 -*-
from numpy import NaN as npNaN
from ..utils import get_offset, verify_series

def ema(close, length=None, offset=None, **kwargs):
    """Indicator: Exponential Moving Average (EMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = kwargs.pop('min_periods', length)
    adjust = kwargs.pop('adjust', True)
    offset = get_offset(offset)
    sma = kwargs.pop('sma', True)
    ewm = kwargs.pop('ewm', False)

    # Calculate Result
    if ewm:
        # Mathematical Implementation of an Exponential Weighted Moving Average
        ema = close.ewm(span=length, min_periods=min_periods, adjust=adjust).mean()
    else:
        alpha = 2 / (length + 1)
        close = close.copy()

        def ema_(series):
            # Technical Anaylsis Definition of an Exponential Moving Average
            # Slow for large series
            series.iloc[1] = alpha * (series.iloc[1] - series.iloc[0]) + series.iloc[0]
            return series.iloc[1]

        seed = close[0:length].mean() if sma else close.iloc[0]

        close[:length - 1] = npNaN
        close.iloc[length - 1] = seed
        ma = close[length - 1:].rolling(2, min_periods=2).apply(ema_, raw=False)
        ema = close[:length].append(ma[1:])

    # Offset
    if offset != 0:
        ema = ema.shift(offset)

    # Name & Category
    ema.name = f"EMA_{length}"
    ema.category = 'overlap'

    return ema



ema.__doc__ = \
"""Exponential Moving Average (EMA)

The Exponential Moving Average is more responsive moving average compared to the
Simple Moving Average (SMA).  The weights are determined by alpha which is
proportional to it's length.  There are several different methods of calculating
EMA.  One method uses just the standard definition of EMA and another uses the
SMA to generate the initial value for the rest of the calculation.

Sources:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_averages
    https://www.investopedia.com/ask/answers/122314/what-exponential-moving-average-ema-formula-and-how-ema-calculated.asp

Calculation:
    Default Inputs:
        length=10
    SMA = Simple Moving Average
    if kwargs['presma']:
        initial = SMA(close, length)
        rest = close[length:]
        close = initial + rest

    EMA = close.ewm(span=length, adjust=adjust).mean()

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    adjust (bool, optional): Default: True
    sma (bool, optional): If True, uses SMA for initial value.
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""