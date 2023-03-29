# -*- coding: utf-8 -*-
from numpy import average as npAverage
from numpy import nan as npNaN
from numpy import log as npLog
from numpy import power as npPower
from numpy import sqrt as npSqrt
from numpy import zeros_like as npZeroslike
from pandas import Series
from pandas_ta.utils import get_offset, verify_series


def jma(close, length=None, phase=None, offset=None, **kwargs):
    """Indicator: Jurik Moving Average (JMA)"""
    # Validate Arguments
    _length = int(length) if length and length > 0 else 7
    phase = float(phase) if phase and phase != 0 else 0
    close = verify_series(close, _length)
    offset = get_offset(offset)
    if close is None: return

    # Calculate
    jma = npZeroslike(close)
    volty_10 = []
    vsum_buff = []

    vsum = kv = det0 = det1 = ma2 = 0.0
    print(type(det1))
    jma[0] = ma1 = uBand = lBand = close[0]

    # Static variables
    pr = 0.5 if phase < -100 else 2.5 if phase > 100 else 1.5 + phase * 0.01
    length1 = max((npLog(npSqrt(_length)) / npLog(2.0)) + 2.0, 0)
    pow1 = max(length1 - 2.0, 0.5)
    beta = 0.45 * (_length - 1) / (0.45 * (_length - 1) + 2.0)

    m = close.shape[0]
    for i in range(1, m):
        price = close[i]

        # Price volatility
        del1 = price - uBand
        del2 = price - lBand
        uBand = price if (del1 > 0) else price - (kv * del1)
        lBand = price if (del2 < 0) else price - (kv * del2)
        volty = max(abs(del1), abs(del2)) if abs(del1) != abs(del2) else 0

        # from volty to avolty
        volty_10.append(volty)
        if len(volty_10) > 10:
            volty_10.pop(0)
        vsum = 0.1 * (volty - volty_10[0]) + vsum
        vsum_buff.append(vsum)
        if len(vsum_buff) > 65:
            vsum_buff.pop(0)
        avolty = sum(vsum_buff) / len(vsum_buff)

        # from avolty to rvolty
        rvolty = volty/avolty if avolty != 0 else 0
        len1 = max(0,(npLog(npSqrt(_length)) / npLog(2.0)) + 2)
        pow1 = max(len1 - 2.0, 0.5)
        rvolty = min(rvolty, pow(len1, 1.0 / pow1))
        rvolty = max(rvolty, 1)

        # from rvolty to second smoothing
        pow2 = npPower(rvolty, pow1)
        beta = 0.45 * (_length - 1) / (0.45 * (_length - 1) + 2)
        Kv =  npPower(beta, sqrt(pow2))
        alpha = npPower(beta, pow2)
        ma1 = (1 - alpha) * price + alpha * ma1
        det0 = (1 - beta) * (price - ma1) + beta * det0
        ma2 = ma1 + pr * det0
        det1 = ((1 - alpha) * (1 - alpha) * (ma2 - jma[i-1])) + (alpha * alpha * det1)
        jma[i] = jma[i - 1] + det1

# Remove initial lookback data and convert to pandas frame
    #jma[0:_length - 1] = npNaN
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
    jma.name = f"JMA_{_length}_{phase}"
    jma.category = "overlap"

    return jma


jma.__doc__ = \
"""Jurik Moving Average Average (JMA)

Mark Jurik's Moving Average (JMA) attempts to eliminate noise to see the "true"
underlying activity. It has extremely low lag, is very smooth and is responsive
to market gaps.

Sources:
    https://c.mql5.com/forextsd/forum/164/jurik_1.pdf
    https://www.prorealcode.com/prorealtime-indicators/jurik-volatility-bands/

Calculation:
    Default Inputs:
        length=7, phase=0

Args:
    close (pd.Series): Series of 'close's
    length (int): Period of calculation. Default: 7
    phase (float): How heavy/light the average is [-100, 100]. Default: 0
    offset (int): How many lengths to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
