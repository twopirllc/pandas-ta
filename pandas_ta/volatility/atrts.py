# -*- coding: utf-8 -*-
from .true_range import true_range
from pandas_ta import Imports
from pandas_ta.overlap import ma
from pandas_ta.volatility import atr
from pandas_ta.utils import get_drift, get_offset, verify_series
from pandas import DataFrame, Series
from functools import partial

try:
    from numba import njit
except ImportError:
    def njit(_): return _

@njit
def calculateFunc(upTrend, dnTrend, prevP, atr, factor):
    if upTrend:
        return prevP - atr * factor
    elif dnTrend:
        return prevP + atr * factor

@njit
def tailingStopFunc(upTrend, dnTrend, prevA, atrts):
    if upTrend:
        if atrts < prevA: return prevA
    elif dnTrend:
        if atrts > prevA: return prevA

def atrts(high, low, close, length=None, factor=None, mamode=None, talib=None, drift=None, offset=None, **kwargs):
    """ATR Trailing Stops (ATRTS) 
    identifies exit points for long and short positions. 
    First, an exponential moving average (EMA) of the input is taken to determine the current trend. 
    Then, the Average True Range (ATR) is calculated and multiplied by a user defined factor. 
    If the EMA is increasing (uptrend), the ATR product is subtracted from the price or, 
    if the EMA is decreasing (down trend), it is added to the price, and along with a few details the ATRTS is formed. 
    The user may change the position (long), input (close), method (EMA), period lengths, 
    percent factor and show entry option(see trading signals below). 
    This indicator’s definition is further expressed in the condensed code given in the calculation below.

    Sources:
        https://www.motivewave.com/studies/atr_trailing_stops.htm

    Calculation:
        //position = pos, user defined, default is long
        //input = price, user defined, default is close
        //method = moving average (ma), user defined, default is EMA
        //period1 = maP, user defined, default is 63
        //period2 = artP, user defined, default is 21
        //factor = fac, user defined, default is 3
        //show entrys = showE, user defined, default is false
        //index = current bar number, prev = previous
        //LOE = less or equal, MOE = more or equal
        //shortP = short position, longP = long position
        //index = current bar number

        longP = pos == "Long";
        shortP = pos == "Short";
        atrts = 0, atr = 0;
        ma = ma(method, maP, input);
        prevP = price[index-1];
        prevA = ifNull(price, atrts[index]); //current atrts is plotted at index+1
        upTrend = price moreThan ma;
        dnTrend = price LOE ma;
        atr = atr(index, atrP);
        if (upTrend)
            atrts = price - fac * atr;
            if (atrts lessThan prevA) atrts = prevA;
        endIf
        if (dnTrend)
            atrts = price + fac * atr;
            if (atrts moreThan prevA) atrts = prevA;
        endIf
        Plot: atrts[index+1];
        //Signals
        sell = false, buy = false;
        if (atrts != 0)
            if (longP AND upTrend)
                sell = price lessThan atrts;   //sell to exit
                buy = prevP lessThan atrts AND price moreThan atrts AND showE;  //buy (enter)
            endIf
            if (shortP AND dnTrend)
                sell = prevP moreThan atrts AND price lessThan atrts  AND showE;   //sell short (enter)
                buy = price moreThan atrts;  //buy to cover
            endIf
        endIf

    Args: 
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        factor (int): the multiplyer. Default: 3
        mamode (str): See ```help(ta.ma)```. Default: 'rma'
        talib (bool): If TA Lib is installed and talib is True, Returns the TA Lib
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs: 
        percent (bool, optional): Return as percentage. Default: False
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 21
    factor = int(factor) if factor and factor > 0 else 3
    mamode = mamode.lower() if mamode and isinstance(mamode, str) else "rma"
    high = verify_series(high, length)
    low = verify_series(low, length)
    close = verify_series(close, length)
    drift = get_drift(drift)
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if high is None or low is None or close is None: return

    # Calculate - start
    atr_ = atr(high=high, low=low, close=close, length=length)
    ma_ = ma(mamode, close, length=length*3)
    upTrend = close > ma_
    dnTrend = close <= ma_
    prevP = close.shift(1)

    func_p = partial(calculateFunc, factor=factor)
    atrts_ = [func_p(a,b,c,d) for a,b,c,d in zip(upTrend, dnTrend, prevP, atr_)]
    atrts_ = Series(atrts_, index=close.index)

    #prevA = atrts_.shift(1)
    #atrts = [tailingStopFunc(a,b,c,d) for a,b,c,d in zip(upTrend, dnTrend, prevA, atrts_)]

    #atrts = Series(atrts, index=close.index)
    atrts = atrts_.shift(-1)
    # Calculate - end

    percentage = kwargs.pop("percent", False)
    if percentage:
        atrts *= 100 / close

    # Offset
    if offset != 0:
        atrts = atrts.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        atrts.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        atrts.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    atrts.name = f"ATRTS{mamode[0]}_{length}{'p' if percentage else ''}"
    atrts.category = "volatility"

    return atrts