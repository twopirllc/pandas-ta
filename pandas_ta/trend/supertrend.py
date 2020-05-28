# -*- coding: utf-8 -*-
import numpy as np
from pandas import DataFrame
from ..utils import get_offset, verify_series
from ..volatility import atr

def supertrend(high, low, close, period=None, multiplier=None, mamode=None, drift=None, offset=None, **kwargs):
    # indicator : supertrend
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)
    period = int(period) if period and period > 0 else 10
    multiplier = float(multiplier) if multiplier and multiplier > 0 else 1.5
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs[
        'min_periods'] is not None else period

    st_updown = np.zeros(shape=(len(close)))
    strend = np.zeros(shape=(len(close)))

    # Bands initial calculation
    midrange = 0.5 * (high + low)
    distance = multiplier * atr(high, low, close, period, mamode, drift, offset, min_periods=min_periods)
    lowerband = midrange - distance
    upperband = midrange + distance

    # final calculation loop
    for i in range(1, len(close)):
        if close[i] > upperband[i-1]:
            st_updown[i] = 1
        elif close[i] < lowerband[i-1]:
            st_updown[i] = -1
        else:
            st_updown[i] = st_updown[i-1]
        if st_updown[i] > 0 and lowerband[i] < lowerband[i-1]:
            lowerband[i] = lowerband[i-1]
        if st_updown[i] < 0 and upperband[i] > upperband[i-1]:
            upperband[i] = upperband[i-1]
        if st_updown[i] < 0 and st_updown[i-1] > 0:
            upperband = midrange + distance
        if st_updown[i] > 0 and st_updown[i-1] < 0:
            lowerband = midrange - distance
        if st_updown[i] < 0 :
            strend[i] = upperband[i]
        else:
            strend[i] = lowerband[i]


    # Prepare DataFrame to return
    data = {f"supertrend_{period}_{multiplier}": strend, f"st_updown_{period}_{multiplier}": st_updown}
    supertrend_df = DataFrame(data)
    supertrend_df.name = f"supertrend_{period}_{multiplier}"
    supertrend_df.category = 'trend'



    # Apply offset if needed
    if offset != 0:
        supertrend_df = supertrend_df.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        supertrend_df.fillna(kwargs['fillna'], inplace=True)

    if 'fill_method' in kwargs:
        supertrend_df.fillna(method=kwargs['fill_method'], inplace=True)



    return supertrend_df

supertrend.__doc__ = \
"""Supertrend (supertrend)

Supertrend is a trend indicator. It was created by Olivier Seban

Sources: 
https://www.abcbourse.com/apprendre/11_le_supertrend.html
(in french, but many other can be found using a search engine)

Calculation:
    Default Inputs:
        period = 10
        multiplier = 1.5


Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: supertrend, st_updown, slowk, slowd columns.
"""