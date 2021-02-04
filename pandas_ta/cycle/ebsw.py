# -*- coding: utf-8 -*-
from numpy import NaN as npNaN
from pandas import DataFrame, Series, concat
from pandas_ta.overlap import rma
from pandas_ta.utils import get_drift, get_offset, verify_series, signals
import math
  
def ebsw(close, length=None, bars=None, offset=None, **kwargs):
    """Indicator: Even Better SineWave (EBSW)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 40
    bars = int(bars) if bars and bars > 0 else 10
    offset = get_offset(offset)
    
    # variables
    alpha1 = 0
    HP = 0              # HighPass
    a1 = 0
    b1 = 0
    c1 = 0
    c2 = 0
    c3 = 0
    Filt = 0
    Wave = 0
    Pwr = 0

    # storage
    lastHP = 0          # last HighPass
    lastClose = 0       # last closing price
    FiltHist = [0, 0]   # Filt history

    # Calculate Result
    m = close.size
    result = [npNaN for _ in range(0, length -1)] + [0]
    for i in range(length, m):
        # HighPass filter cyclic components whose periods are shorter than Duration input
        alpha1 = (1 - math.sin(360 / length)) / math.cos(360 / length)
        HP = 0.5 * (1 + alpha1) * (close[i] - lastClose) + alpha1 * lastHP
        # print('alpha1: ', alpha1, ', HP (HighPass): ', HP)

        # Smooth with a Super Smoother Filter from equation 3-3
        a1 = math.exp(-1.414 * 3.14159 / bars)         # math.pi ~ 3.14159
        b1 = 2 * a1 * math.cos(1.414 * 180 / bars)
        c2 = b1
        c3 = -1 * a1 * a1
        c1 = 1 - c2 - c3
        Filt = c1 * (HP + lastHP) / 2 + c2 * FiltHist[1] + c3 * FiltHist[0]
        # Filt = float("{:.8f}".format(float(Filt)))        # to fix for small scientific notations, the big ones fail
        # print('Filt: ', Filt, 'FiltHist (list): ', FiltHist)

        # 3 Bar average of Wave amplitude and power
        Wave = (Filt + FiltHist[1] + FiltHist[0]) / 3
        Pwr = (Filt * Filt + FiltHist[1] * FiltHist[1] + FiltHist[0] * FiltHist[0]) / 3

        # Normalize the Average Wave to Square Root of the Average Power
        Wave = Wave / math.sqrt(Pwr)

        # update storage, result
        FiltHist.append(Filt)  # append new Filt value
        FiltHist.pop(0)  # remove first element of list (left) -> updating/trim
        lastHP = HP
        lastClose = close[i]
        result.append(Wave)

    ebsw = Series(result, index=close.index)

    # Offset
    if offset != 0:
        ebsw = ebsw.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        ebsw.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ebsw.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    ebsw.name = f"ebsw_{length}"
    ebsw.category = "cycles"

    return ebsw


ebsw.__doc__ = \
"""Even Better SineWave (EBSW) beta*

This indicator mesures market cycles and uses a low pass filter to remove noise. Its output is bound signal between 
-1 and 1 and the maximum length of a detected trend is limited by its length input.
Written by rengel8 for Pandas TA based on a publication at 'prorealcode.com' and a book by J.F.Ehlers.

* This implementation seems to be logically limited. It would make sense to implement exactly the version from 
  prorealcode and compare the behaviour. 


Sources:
    https://www.prorealcode.com/prorealtime-indicators/even-better-sinewave/
    J.F.Ehlers 'Cycle Analytics for Traders', 2014

Calculation:
    refer to 'sources' or implementation

Args:
    close (pd.Series): Series of 'close's
    length (int): It's max cycle/trend period.  Default: 40, values between 40-48 work like expected 
    bars (int): Period of low pass filtering. Default: 10
    drift (int): The difference period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
