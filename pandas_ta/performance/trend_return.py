# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from .log_return import log_return
from .percent_return import percent_return
from pandas_ta.utils import get_offset, verify_series, zero


def trend_return(close, trend, log=True, cumulative=None, trend_reset=0, trade_offset=None, offset=None, **kwargs):
    """Indicator: Trend Return"""
    # Validate Arguments
    close = verify_series(close)
    trend = verify_series(trend)
    cumulative = cumulative if cumulative is not None and isinstance(cumulative, bool) else False
    trend_reset = int(trend_reset) if trend_reset and isinstance(trend_reset, int) else 0
    trade_offset = int(trade_offset) if trade_offset and isinstance(trade_offset, int) else -1
    offset = get_offset(offset)

    # Calculate Result
    if log:
        returns = log_return(close, cumulative=False)
    else:
        returns = percent_return(close, cumulative=False)
    trends = trend.astype(int)
    returns = (trends * returns).apply(zero)

    tsum = 0
    m = trends.size
    result = []
    for i in range(0, m):
        if trends[i] == trend_reset:
            tsum = 0
        else:
            return_ = returns[i]
            if cumulative:
                tsum += return_
            else:
                tsum = return_
        result.append(tsum)

    _cumulative = "C" if cumulative else ""
    _log = "L" if log else "P"
    _returns = "LOGRET" if log else "PCTRET"
    _props = f"{_cumulative}{_log}TR"
    data = {
        _props: result,
        f"TR_{_returns}": returns,
        f"{_props}_Trends": trends,
        f"{_props}_Trades": trends.diff().shift(trade_offset).fillna(0).astype(int)
    }
    df = DataFrame(data, index=close.index)

    # Offset
    if offset != 0:
        df = df.shift(offset)

    # Name & Category
    df.name = _props
    df.category = "performance"

    return df


trend_return.__doc__ = \
"""Trend Return

Calculates the (Cumulative) Returns of a Trend as defined by a sequence of
booleans called a 'trend'. One popular example in TA literature is to be long
when the 'close' > 'moving average'. In which case, the
trend= close > sma(close, 50). By default it calculates log returns but can also
use percent change.

Examples:
ta.trend_return(close, trend= close > ta.sma(close, 50))
ta.trend_return(close, trend= ta.ema(close, 8) > ta.ema(close, 21))

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
    trend (pd.Series): Series of 'trend's. Preferably 0's and 1's.
    trade_offset (value): Value used shift the trade entries/exits. Default: -1
    trend_reset (value): Value used to identify if a trend has ended. Default: 0
    log (bool): Calculate logarithmic returns. Default: True
    cumulative (bool): If True, returns the cumulative returns. Default: False
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method
    variable (bool, optional): Whether to include if return fluxuations in the
        cumulative returns.

Returns:
    pd.DataFrame: Returns columns: Trend Return, Close Return, Trends (trend: 1,
        no trend: 0), and Trades (Enter: 1, Exit: -1, Otherwise: 0).
"""
