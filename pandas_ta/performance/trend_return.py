# -*- coding: utf-8 -*-
from pandas import Series
from .log_return import log_return
from .percent_return import percent_return
from ..utils import get_offset, verify_series, zero

def trend_return(close, trend, log=True, cumulative=None, offset=None, trend_reset=0, **kwargs):
    """Indicator: Trend Return"""
    # Validate Arguments
    close = verify_series(close)
    trend = verify_series(trend)
    offset = get_offset(offset)
    trend_reset = int(trend_reset) if trend_reset and isinstance(trend_reset, int) else 0

    # Calculate Result
    returns = log_return(close, cumulative=False) if log else percent_return(close, cumulative=False)
    tsum = 0
    m = trend.size
    trend = trend.astype(int)
    returns = (trend * returns).apply(zero)
    
    result = []
    for i in range(0, m):
        if trend[i] == trend_reset:
            tsum = 0
        else:
            return_ = returns[i]
            if cumulative:
                tsum += return_
            else:
                tsum = return_
        result.append(tsum)

    trend_return = Series(result, index=close.index)

    # Offset
    if offset != 0:
        trend_return = trend_return.shift(offset)

    # Name & Category
    trend_return.name = f"{'C' if cumulative else ''}{'L' if log else 'P'}TR"
    trend_return.category = 'performance'

    return trend_return



trend_return.__doc__ = \
"""Trend Return

Calculates the (Cumulative) Returns of a Trend as defined by some conditional.
By default it calculates log returns but can also use percent change.

Sources: Kevin Johnson

Calculation:
    Default Inputs:
        trend_reset=0, log=True, cumulative=False

    sum = 0
    returns = log_return if log else percent_return # These are not cumulative
    returns = (trend * returns).apply(zero)
    for i, in range(0, trend.size):
        if item == trend_reset:
            sum = 0
        else:
            return_ = returns.iloc[i]
            if cumulative:
                sum += return_
            else:
                sum = return_
        trend_return.append(sum)

    if cumulative and variable:
        trend_return += returns

Args:
    close (pd.Series): Series of 'close's
    trend (pd.Series): Series of 'trend's.  Preferably 0's and 1's.
    trend_reset (value): Value used to identify if a trend has ended.  Default: 0
    log (bool): Calculate logarithmic returns.  Default: True
    cumulative (bool): If True, returns the cumulative returns.  Default: False
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method
    variable (bool, optional): Whether to include if return fluxuations in the cumulative returns.

Returns:
    pd.Series: New feature generated.
"""