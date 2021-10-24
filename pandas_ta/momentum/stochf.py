# -*- coding: utf-8 -*-
from pandas import DataFrame
from pandas_ta.overlap import ma
from pandas_ta.utils import get_offset, non_zero_range, verify_series


def stochf(high, low, close, k=None, d=None, mamode=None, offset=None, **kwargs):
    """Indicator: Stochastic Oscillator Fast(stochf)"""
    # Validate arguments
    k = k if k and k > 0 else 14
    d = d if d and d > 0 else 3
    _length = max(k, d)
    high = verify_series(high, _length)
    low = verify_series(low, _length)
    close = verify_series(close, _length)
    offset = get_offset(offset)
    mamode = mamode if isinstance(mamode, str) else "sma"

    if high is None or low is None or close is None: return

    # Calculate Result
    lowest_low = low.rolling(k).min()
    highest_high = high.rolling(k).max()

    stoch = 100 * (close - lowest_low)
    stoch /= non_zero_range(highest_high, lowest_low)

    stoch_k = ma(mamode, stoch.loc[stoch.first_valid_index():,], length=k)
    stoch_d = ma(mamode, stoch_k.loc[stoch_k.first_valid_index():,], length=d)

    # Offset
    if offset != 0:
        stoch_k = stoch_k.shift(offset)
        stoch_d = stoch_d.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        stoch_k.fillna(kwargs["fillna"], inplace=True)
        stoch_d.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        stoch_k.fillna(method=kwargs["fill_method"], inplace=True)
        stoch_d.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    _name = "stochf"
    _props = f"_{k}_{d}"
    stoch_k.name = f"{_name}k{_props}"
    stoch_d.name = f"{_name}d{_props}"
    stoch_k.category = stoch_d.category = "momentum"

    # Prepare DataFrame to return
    data = {stoch_k.name: stoch_k, stoch_d.name: stoch_d}
    df = DataFrame(data)
    df.name = f"{_name}{_props}"
    df.category = stoch_k.category
    return df


stochf.__doc__ = \
"""stochastic fast (stochf)

The Stochastic Fast (StochF) normalizes price as a percentage between 0 and 100.
Normally two lines are plotted, the %K line and a moving average of the %K which is called %D. 
A fast stochastic is created by not smoothing the %K line with a moving average before it is displayed.

Sources:
    https://www.tradingtechnologies.com/xtrader-help/x-study/technical-indicator-definitions/stochastic-fast-stochf/
    https://tadoc.org/indicator/STOCHF.htm
    
Calculation:
    Default Inputs:
        k=14, d=3
    SMA = Simple Moving Average
    LL  = low for last k periods
    HH  = high for last k periods

    Fast %K = 100 SMA ( ( ( close - LL ) / ( HH - LL ) ), k )
    Fast %D = SMA ( Fast %K )

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    k (int): The Fast %K period. Default: 14
    d (int): The Slow %K period. Default: 3
    mamode (str): See ```help(ta.ma)```. Default: 'sma'
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: %K, %D columns.
"""
