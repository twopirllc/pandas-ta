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

    # Calculate base variables
    jma = Volty = vsum = np.zeros_like(close)
    det0 = det1 = ma2 = bsmax = bsmin = 0.0
    jma[0] = ma1 = close[0]
    len1 = max(((math.log(math.sqrt(0.5*(length-1)))/math.log(2.0))+2),0)
    len2 = math.sqrt(0.5*(length-1))*len1
    pow1 = max(len1-2.0,0.5)
    PR = 0.5 if phase<-100 else (2.5 if phase>100 else phase/100+1.5)
    beta = 0.45*(length-1)/(0.45*(length-1)+2)

    # Iterate through the dataset, calculate Volty and jma
    for i in range(1, close.shape[0]):
      hprice = np.amax(close[max(i-length,0):i])
      lprice = np.amin(close[max(i-length,0):i])
      del1 = hprice - bsmax
      del2 = lprice - bsmin
      Volty[i] = abs(del1) if del1>del2 else abs(del2) if del1<del2 else 0
      vsum[i] = vsum[i-1] + 0.1 * (Volty[i]-Volty[i-min(i,10)])
      avgVolty = np.mean(vsum[i-min(i,65):i])
      dVolty = max(min(math.exp((1/pow1)*math.log(len1)),Volty[i]/avgVolty),1)
      pow2 = math.exp(pow1*math.log(dVolty))
      Kv = math.exp(math.sqrt(pow2)*math.log(len2/(len2+1)))
      bsmax = hprice if del1>0 else hprice - Kv*del1
      bsmin = lprice if del2<0 else lprice - Kv*del2
      rVolty = max(min(math.pow(len1,1/pow1), Volty[i]/avgVolty),1)
      power = math.pow(rVolty,pow1)
      alpha = math.pow(beta, power)
      ma1 = (1 - alpha) * close[i] + alpha * ma1
      det0 = (close[i] - ma1) * (1 - beta) + beta * det0
      ma2 = ma1 + PR * det0 
      det1 = (ma2 - jma[i-1]) * math.pow(1-alpha,2) + math.pow(alpha,2) * det1
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
""" Jurik Moving Average Average (JMA)

Sources:
    Implementation of: https://c.mql5.com/forextsd/forum/164/jurik_1.pdf
    Jurik volatility: https://www.prorealcode.com/prorealtime-indicators/jurik-volatility-bands/

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
