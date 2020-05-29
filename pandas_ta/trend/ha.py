# -*- coding: utf-8 -*-
import numpy as np
from pandas import DataFrame
from pandas_ta.utils import get_offset, verify_series


def ha(open, high, low, close, offset=None, **kwargs):
    # indicator : Heikin Ashi
    # Validate Arguments
    open_ = verify_series(open)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)

    # calculate ha_close
    ha_close = 0.25 * (open_ + high + low + close)

    # Initialization of the ha_open array
    ha_open = np.zeros(shape=(len(close)))

    # ha_open of the first element
    ha_open[0] = 0.5 * (open_[0] + close[0])

    # calculate ha_open. Based on previous ha_open & ha_close
    for i in range(1, len(close)):
        ha_open[i] = 0.5 * (ha_open[i-1] + ha_close[i-1])

    # calculation of ha_high & ha_low
    ha_high = np.maximum.reduce([high, ha_open, ha_close])
    ha_low = np.minimum.reduce([low, ha_open, ha_close])

    # Prepare DataFrame to return
    data = {'ha_open': ha_open, 'ha_high': ha_high, 'ha_low': ha_low, 'ha_close': ha_close}
    hadf = DataFrame(data)
    hadf.name = "Heikin-Ashi"
    hadf.category = 'trend'

    # Apply offset if needed
    if offset != 0:
        hadf = hadf.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        hadf.fillna(kwargs['fillna'], inplace=True)

    if 'fill_method' in kwargs:
        hadf.fillna(method=kwargs['fill_method'], inplace=True)

    return hadf


ha.__doc__ = \
"""Heikin Ashi (HA)

The Heikin-Ashi technique averages price data to create a Japanese candlestick chart that filters out market noise. 
Heikin-Ashi charts, developed by Munehisa Homma in the 1700s, 
share some characteristics with standard candlestick charts but differ based on the values used to create each candle. 
Instead of using the open, high, low, and close like standard candlestick charts, 
the Heikin-Ashi technique uses a modified formula based on two-period averages. 
This gives the chart a smoother appearance, making it easier to spots trends and reversals, 
but also obscures gaps and some price data.

Sources:
    https://www.investopedia.com/terms/h/heikinashi.asp

Calculation:
     The Formula for the Heikin-Ashi technique is:

Heikin-Ashi Close=(Open0+High0+Low0+Close0)/4
Heikin-Ashi Open=(HA Open−1+HA Close−1)/2
Heikin-Ashi High=Max (High0,HA Open0,HA Close0)
Heikin-Ashi Low=Min (Low0,HA Open0,HA Close0)
where:Open0 etc.=Values from the current period
Open−1 etc.=Values from the prior period
HA=Heikin-Ashi

 How to Calculate Heikin-Ashi

    Use one period to create the first Heikin-Ashi (HA) candle, using the formulas. 
    For example use the high, low, open, and close to create the first HA close price. 
    Use the open and close to create the first HA open. 
    The high of the period will be the first HA high, and the low will be the first HA low.
    With the first HA calculated, it is now possible to continue computing the HA candles per the formulas.
​​
Args:
    open_ (pd.Series): Series of 'open's
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: ha_open, ha_high,ha_low, ha_close columns.
"""
