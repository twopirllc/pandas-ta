# -*- coding: utf-8 -*-
from pandas_ta.utils import get_offset, verify_series
from pandas import Series
import numpy as np
from numpy import nan as npNaN
import math

def jma(close, length=None, phase=0, offset=None, **kwargs):
    """
    Indicator: Jurik Moving Average (JMA)
    Implementation of: https://c.mql5.com/forextsd/forum/164/jurik_1.pdf
    Jurik Volty from: https://www.prorealcode.com/prorealtime-indicators/jurik-volatility-bands/
    """
    # Validate Arguments
    length = int(length) if length and length > 0 else 7
    close = verify_series(close, length)
    offset = get_offset(offset)
    if close is None: return

    # Define base variables
    jma = np.zeros_like(close)
    Volty = np.zeros_like(close)
    vSum = np.zeros_like(close)
    Kv = det0 = det1 = ma2 = 0.0
    jma[0] = ma1 = uBand = lBand = close[0]
    # Static variables
    SumLen = 10
    len = 0.5*(length-1)
    PR = 0.5 if phase<-100 else 2.5 if phase>100 else phase*0.01+1.5
    len1 = max((math.log(math.sqrt(len))/math.log(2.0))+2.0, 0)
    pow1 = max(len1-2.0, 0.5)
    len2 = math.sqrt(len)*len1
    bet = len2/(len2+1)
    beta = 0.45*(length-1)/(0.45*(length-1)+2.0)
    for i in range(1, close.shape[0]):
        price = close[i]
        # Price volatility
        del1 = price-uBand
        del2 = price-lBand
        Volty[i] = max(abs(del1),abs(del2)) if abs(del1)!=abs(del2) else 0
        # Relative price volatility factor
        vSum[i] = vSum[i-1] + (Volty[i]-Volty[max(i-SumLen,0)])/SumLen
        avgVolty = np.average(vSum[max(i-65,0):i+1])
        dVolty = 0 if avgVolty==0 else Volty[i]/avgVolty
        rVolty = max(1.0, min(math.pow(len1, 1/pow1), dVolty))
        # Jurik volatility bands
        pow2 = math.pow(rVolty, pow1)
        Kv = math.pow(bet, math.sqrt(pow2))
        uBand = price if (del1 > 0) else price - (Kv*del1)
        lBand = price if (del2 < 0) else price - (Kv*del2)
        # Jurik Dynamic Factor
        power = math.pow(rVolty, pow1)
        alpha = math.pow(beta, power)
        # 1st stage - prelimimary smoothing by adaptive EMA
        ma1 = ((1-alpha)*price)+(alpha*ma1) #
        # 2nd stage - one more prelimimary smoothing by Kalman filter
        det0 = ((price-ma1)*(1-beta))+(beta*det0)
        ma2 = ma1+PR*det0
        # 3rd stage - final smoothing by unique Jurik adaptive filter
        det1 = ((ma2-jma[i-1])*(1-alpha)*(1-alpha))+(alpha*alpha*det1)
        jma[i] = jma[i-1] + det1

    # Remove initial lookback data and convert to pandas frame
    jma[0:length-1] = npNaN
    jma = Series(jma, index=close.index)

    # Offset
    if offset != 0:
        jma = jma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        jma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        jma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    jma.name = f"JMA_{length}"
    jma.category = "overlap"

    return jma


jma.__doc__ = \
"""Volume Weighted Moving Average (VWMA)

Jurik Moving Average

Sources:
    Implementation of: https://c.mql5.com/forextsd/forum/164/jurik_1.pdf

Calculation:
    Default Inputs:
        length=7
        phase=0

Args:
    close (pd.Series): Series of 'close's
    length (int): Period of calculation. Default: 7
    phase (float): how heavy/light the average is [-100, 100] Default: 0
    offset (int): How many lengths to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
