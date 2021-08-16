# -*- coding: utf-8 -*-
from numpy import NaN as npNaN
from numpy import cos as npCos
from numpy import exp as npExp
from numpy import full as npFull
from numpy import sqrt as npSqrt
from pandas import DataFrame, Series, concat
from pandas_ta.overlap import rma
from pandas_ta.utils import get_drift, get_offset, verify_series, signals


def reflex(close, length=None, smooth_bars=None, offset=None, **kwargs):
    """Indicator: Reflex"""
    # Validate arguments
    close = verify_series(close, length)
    length = int(length) if length and length > 0 else 20
    smooth_bars = int(smooth_bars) if smooth_bars and smooth_bars > 0 else 20
    offset = get_offset(offset)

    # Precalculations
    a1 = npExp(-1.414 * 3.14159 / smooth_bars)
    b1 = 2 * a1 * npCos(1.414 * 180 / smooth_bars)
    c2 = b1
    c3 = -a1 * a1
    c1 = 1 - c2 - c3
    Filt = npFull(close.size, 0)
    MS = npFull(close.size, 0)
    # Reflex = list(Filt)
    Reflex = npFull(close.size, npNaN)

    # Calculation
    for i in range(1, close.size):
        # Gently smooth the data in a SuperSmoother
        Filt[i] = c1 * (close[i] + close[i - 1]) / 2 + c2 * Filt[i - 1] + c3 * Filt[i - 2]

        # Length is assumed cycle period
        Slope = (Filt[i - length] - Filt[i]) / length

        # Sum the differences
        Sum = 0
        for count in range(1, length):
            Sum = Sum + (Filt[i] + count * Slope) - Filt[i - count]
        Sum = Sum / length

        # Normalize in terms of Standard Deviations
        MS[i] = .04 * Sum * Sum + .96 * MS[i - 1]
        if MS[i] != 0:
            Reflex[i] = Sum / npSqrt(MS[i])
        else:
            Reflex[i] = Sum / 0.00001

    result = Series(Reflex, index=close.index)

    # Neutralize pre-roll phase
    result.iloc[0:length] = npNaN

    # Offset
    if offset != 0:
        result = result.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        result.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        result.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    result.name = f"REFLEX_{length}_{smooth_bars}"
    result.category = "cycles"

    return result


reflex.__doc__ = \
"""Reflex (reflex)

John F. Ehlers introduced two indicators within the article "Reflex: A New Zero-Lag Indicator”
in February 2020, TASC magazine. One of which is the Reflex, a lag reduced cycle indicator.
Both indicators (Reflex/Trendflex) are oscillators and complement each other with the focus for 
cycle and trend.

Written for Pandas TA by rengel8 (2021-08-11) based on the implementation on prorealcode (refer to source).
Beyond the mentioned source, this implementation has a separate control parameter for the internal
applied SuperSmoother. 

Sources:
    https://www.prorealcode.com/prorealtime-indicators/reflex-and-trendflex-indicators-john-f-ehlers/

Calculation:
    Refer to provided source or the code above.   

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 20
    smooth_bars (int): Period of internal SuperSmoother (default: asmooth_bars = length).  Default: 20    
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
