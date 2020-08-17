# -*- coding: utf-8 -*-
from numpy import log as nplog
from numpy import NaN as npNaN
from pandas import DataFrame, Series
from pandas_ta.overlap import ema, hl2
from pandas_ta.utils import get_offset, verify_series, zero

def fisher(high, low, length=None, signal=None, offset=None, **kwargs):
    """Indicator: Fisher Transform (FISHT)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    length = int(length) if length and length > 0 else 9
    signal = int(signal) if signal and signal > 0 else 5
    offset = get_offset(offset)

    # Calculate Result
    m = high.size
    hl2_ = hl2(high, low)
    max_high = hl2_.rolling(length).max()
    min_low = hl2_.rolling(length).min()
    hl2_range = max_high - min_low
    hl2_range[hl2_range < 1e-5] = 0.001
    position = (hl2_ - min_low) / hl2_range
    
    v = 0
    fish = 0
    result = [npNaN for _ in range(0, length - 1)]
    for i in range(length - 1, m):
        v = 0.66 * (position[i] - 0.5) + 0.67 * v
        if v >  0.99: v =  0.999
        if v < -0.99: v = -0.999
        fish = 0.5 * (fish + nplog((1 + v) / (1 - v)))
        result.append(fish)
        
    fisher = Series(result, index=high.index)
    signalma = ema(fisher, length=signal)

    # Offset
    if offset != 0:
        fisher = fisher.shift(offset)
        signalma = signalma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        fisher.fillna(kwargs["fillna"], inplace=True)
        signalma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        fisher.fillna(method=kwargs["fill_method"], inplace=True)
        signalma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    _props = f"_{length}_{signal}"
    fisher.name = f"FISHERT{_props}"
    signalma.name = f"FISHERTs{_props}"
    fisher.category = signalma.category = "momentum"

    # Prepare DataFrame to return
    data = {fisher.name: fisher, signalma.name: signalma}
    df = DataFrame(data)
    df.name = f"FISHERT{_props}"
    df.category = fisher.category

    return df



fisher.__doc__ = \
"""Fisher Transform (FISHT)

Attempts to identify significant price reversals by normalizing prices over a
user-specified number of periods. A reversal signal is suggested when the the
two lines cross.

Sources:
    https://tulipindicators.org/fisher
    https://library.tradingtechnologies.com/trade/chrt-ti-ehler-fisher-transformation.html
    TradingView

Calculation:
    Default Inputs:
        length=10, signal=5
    EMA = Exponential Moving Average
    HL2 = 0.5 * (high + low)
    Max_HL2 = HL2.rolling(length).max()
    Min_HL2 = HL2.rolling(length).min()
    HL2R = Max_HL2 - Min_HL2
    HL2R[HL2R < 1e-5] = 0.001 # Set small values to 0.001
    position = (HL2 - Min_HL2) / HL2R
    
    FISH = 0.5 * log((1 + position) / (1 - position)) 
    Signal = EMA(FISH, signal)
    
    # Fix 
    position = position > .99 ? .999 : position < -.99 ? -.999 : position

    position := round_(.66 * ((hl2 - low_) / max(high_ - low_, .001) - .5) + .67 * nz(value[1]))

    fish1 = 0.0
    fish1 := .5 * log((1 + value) / max(1 - value, .001)) + .5 * nz(fish1[1])

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    length (int): Fisher period.  Default: 9
    signal (int): Fisher Signal period.  Default: 5
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""