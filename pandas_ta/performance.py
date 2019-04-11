# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from .utils import get_offset, verify_series, zero



def log_return(close, length=None, cumulative=False, offset=None, **kwargs):
    """Indicator: Log Return"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    log_return = np.log(close).diff(periods=length)

    if cumulative:
        log_return = log_return.cumsum()

    # Offset
    if offset != 0:
        log_return = log_return.shift(offset)

    # Name & Category
    log_return.name = f"{'CUM' if cumulative else ''}LOGRET_{length}"
    log_return.category = 'performance'

    return log_return


def percent_return(close, length=None, cumulative=False, offset=None, **kwargs):
    """Indicator: Percent Return"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    pct_return = close.pct_change(length)

    if cumulative:
        pct_return = pct_return.cumsum()

    # Offset
    if offset != 0:
        pct_return = pct_return.shift(offset)

    # Name & Category
    pct_return.name = f"{'CUM' if cumulative else ''}PCTRET_{length}"
    pct_return.category = 'performance'

    return pct_return


def trend_return(close, trend, trend_reset=0, log=True, cumulative=False, offset=None, **kwargs):
    """Indicator: Trend Return"""
    # Validate Arguments
    close = verify_series(close)
    trend = verify_series(trend)
    offset = get_offset(offset)
    variable = kwargs.pop('variable', False)

    # Calculate Result
    returns = log_return(close, cumulative=False) if log else percent_return(close, cumulative=False)
    m = trend.size
    tsum = 0
    result = []
    returns = (trend * returns).apply(zero)
    # trend = trend.astype(int)
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

    trend_return = pd.Series(result)

    # Experimental: Add the individual return flucuations to the cumulative returns
    if variable and cumulative:
        trend_return += returns

    # Offset
    if offset != 0:
        trend_return = trend_return.shift(offset)

    # Name & Category
    trend_return.name = f"{'C' if cumulative else ''}{'L' if log else 'P'}TR"
    trend_return.category = 'performance'

    return trend_return



log_return.__doc__ = \
"""Log Return

Calculates the logarithmic return of a Series.
See also: help(df.ta.log_return) for additional **kwargs a valid 'df'.

Sources:
    https://stackoverflow.com/questions/31287552/logarithmic-returns-in-pandas-dataframe

Calculation:
    Default Inputs:
        length=1, cumulative=False
    LOGRET = log( close.diff(periods=length) )
    CUMLOGRET = LOGRET.cumsum() if cumulative

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 20
    cumulative (bool): If True, returns the cumulative returns.  Default: False
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


percent_return.__doc__ = \
"""Percent Return

Calculates the percent return of a Series.
See also: help(df.ta.percent_return) for additional **kwargs a valid 'df'.

Sources:
    https://stackoverflow.com/questions/31287552/logarithmic-returns-in-pandas-dataframe

Calculation:
    Default Inputs:
        length=1, cumulative=False
    PCTRET = close.pct_change(length)
    CUMPCTRET = PCTRET.cumsum() if cumulative

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 20
    cumulative (bool): If True, returns the cumulative returns.  Default: False
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


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