# -*- coding: utf-8 -*-
from ..utils import get_drift, get_offset, verify_series
from ..overlap.linreg import linreg

def cfo(close, length=None, scalar=None, drift=None, offset=None, **kwargs):
    """Indicator: Chande Forcast Oscillator (CFO)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 9
    scalar = float(scalar) if scalar else 100
    drift = get_drift(drift)
    offset = get_offset(offset)

    #Finding linear regression of Series
    linreg_series = linreg(close,length=length)
    cfo = ((close-linreg_series)/close *100)
    # Offset
    if offset != 0:
        cfo = cfo.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        cfo.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        cfo.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    cfo.name = f"CFO_{length}"
    cfo.category = "momentum"

    return cmo

cfo.__doc__ = \
"""Chande Forcast Oscillator (CFO)

The Forecast Oscillator calculates the percentage difference between the actual price
and the Time Series Forecast (the endpoint of a linear regression line).

Sources:
    https://www.fmlabs.com/reference/default.htm?url=ForecastOscillator.htm

Calculation:
    Default Inputs:
        length=9, drift=1, scalar=100

    # Same Calculation as RSI except for this step
    CFO = ( ( CLOSE- LINERREG ) / CLOSE * 100 )

Args:
    close (pd.Series): Series of 'close's
    scalar (float): How much to magnify.  Default: 100
    drift (int): The short period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
