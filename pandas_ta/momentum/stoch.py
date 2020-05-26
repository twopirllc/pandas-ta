# -*- coding: utf-8 -*-
from pandas import DataFrame
from ..overlap.sma import sma
from ..utils import get_offset, non_zero_range, verify_series

def stoch(high, low, close, fast_k=None, slow_k=None, slow_d=None, offset=None, **kwargs):
    """Indicator: Stochastic Oscillator (STOCH)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    fast_k = fast_k if fast_k and fast_k > 0 else 14
    slow_k = slow_k if slow_k and slow_k > 0 else 5
    slow_d = slow_d if slow_d and slow_d > 0 else 3
    offset = get_offset(offset)

    # Calculate Result
    lowest_low   =  low.rolling(slow_k).min()
    highest_high = high.rolling(slow_k).max()

    fastk = 100 * (close - lowest_low) / non_zero_range(highest_high, lowest_low)
    fastd = sma(fastk, length=slow_d)

    slowk = sma(fastk, length=slow_k)
    slowd = sma(slowk, length=slow_d)

    # Offset
    if offset != 0:
        fastk = fastk.shift(offset)
        fastd = fastd.shift(offset)
        slowk = slowk.shift(offset)
        slowd = slowd.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        fastk.fillna(kwargs['fillna'], inplace=True)
        fastd.fillna(kwargs['fillna'], inplace=True)
        slowk.fillna(kwargs['fillna'], inplace=True)
        slowd.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        fastk.fillna(method=kwargs['fill_method'], inplace=True)
        fastd.fillna(method=kwargs['fill_method'], inplace=True)
        slowk.fillna(method=kwargs['fill_method'], inplace=True)
        slowd.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    fastk.name = f"STOCHFk_{fast_k}"
    fastd.name = f"STOCHFd_{slow_d}"
    slowk.name = f"STOCHk_{slow_k}"
    slowd.name = f"STOCHd_{slow_d}"
    fastk.category = fastd.category = slowk.category = slowd.category = 'momentum'

    # Prepare DataFrame to return
    _props = f"_{fast_k}_{slow_k}_{slow_d}"
    data = {fastk.name: fastk, fastd.name: fastd, slowk.name: slowk, slowd.name: slowd}
    stochdf = DataFrame(data)
    stochdf.name = f"STOCH{_props}"
    stochdf.category = 'momentum'

    return stochdf



stoch.__doc__ = \
"""Stochastic (STOCH)

Stochastic Oscillator is a range bound momentum indicator.  It displays the location
of the close relative to the high-low range over a period.

Sources:
    https://www.tradingview.com/wiki/Stochastic_(STOCH)

Calculation:
    Default Inputs:
        fast_k=14, slow_k=5, slow_d=3
    SMA = Simple Moving Average
    LL  = low for last fast_k periods
    HH  = high for last fast_k periods

    FASTK = 100 * (close - LL) / (HH - LL)
    FASTD = SMA(FASTK, slow_d)

    SLOWK = SMA(FASTK, slow_k)
    SLOWD = SMA(SLOWK, slow_d)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    fast_k (int): The Fast %K period.  Default: 14
    slow_k (int): The Slow %K period.  Default: 5
    slow_d (int): The Slow %D period.  Default: 3
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: fastk, fastd, slowk, slowd columns.
"""