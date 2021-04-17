# -*- coding: utf-8 -*-
from pandas import DataFrame
from .log_return import log_return
from .percent_return import percent_return
from pandas_ta.utils import get_offset, verify_series, zero


def trend_return(close, trend, log=True, asbool=None, trend_reset=0, trade_offset=None, offset=None, **kwargs):
    """Indicator: Trend Return"""
    # Validate Arguments
    close = verify_series(close)
    trend = verify_series(trend)
    asbool = bool(asbool) if isinstance(asbool, bool) else False
    log = bool(log) if isinstance(log, bool) else True
    trend_reset = int(trend_reset) if trend_reset and isinstance(trend_reset, int) else 0
    if trade_offset !=0:
        trade_offset = int(trade_offset) if trade_offset and isinstance(trade_offset, int) else -1
    offset = get_offset(offset)

    # Calculate Result
    returns = log_return(close) if log else percent_return(close)
    _return_name = returns.name

    trends = trend.astype(int)
    active_returns = (trends * returns).apply(zero)

    tsum = 0
    m = trends.size
    csum = []
    for i in range(0, m):
        if trends[i] == trend_reset:
            tsum = 0
        else:
            tsum += active_returns[i]
        csum.append(tsum)

    trades = trends.diff().shift(trade_offset).fillna(0).astype(int)
    entries = (trades > 0).astype(int)
    exits = (trades < 0).abs().astype(int)

    if asbool:
        trends = trends.astype(bool)
        entries = entries.astype(bool)
        exits = exits.astype(bool)

    data = {
        f"TR_{_return_name}": active_returns,
        f"TR_CUM{_return_name}": csum,
        f"TR_Trends": trends,
        f"TR_Trades": trades,
        f"TR_Entries": entries,
        f"TR_Exits": exits,
    }
    df = DataFrame(data, index=close.index)

    # Offset
    if offset != 0:
        df = df.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        df.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        df.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    df.name = f"TR{'l' if log else 'p'}"
    df.category = "performance"

    return df


trend_return.__doc__ = \
"""Trend Return

Calculates the Returns and Cumulative Returns of a Trend as defined by a
sequence of booleans called a 'trend'. One popular example in TA literature is
to be long when the 'close' > 'moving average'. For example, if the trend is
long when close is above sma(close, 50), then set trend= close > sma(close, 50).
Trend Return will calculate the returns and cumulative returns as well as the
Trends, Trades, Entries and Exits. By default, Trends, Entries and Exits return
integers. When 'asbool=True', Trends, Entries and Exits will return as boolean
which is helpful when combined with the vectorbt backtesting package.
Additionally, returns are log returns by default.

Examples:
ta.trend_return(close, trend= close > ta.sma(close, 50))
ta.trend_return(close, trend= ta.ema(close, 8) > ta.ema(close, 21))

Sources: Kevin Johnson

Calculation:
    Default Inputs:
        log=True, asbool=False, trend_reset=0

    sum = 0
    returns = log_return if log else percent_return # These are not cumulative
    returns = (trend * returns).apply(zero)
    for i, in range(0, trend.size):
        if item == trend_reset:
            sum = 0
        else:
            returns += returns.iloc[i]
        trend_return.append(sum)

Args:
    close (pd.Series): Series of 'close's
    trend (pd.Series): Series of 'trend's. The trend can be either a boolean or
        integer series of '0's and '1's
    log (bool): Calculate logarithmic returns. Default: True
    asbool (bool): If True, it converts the Trends, Entries and Exits columns to
        booleans. When boolean, it is also useful for backtesting with
        vectorbt's Portfolio.from_signal(close, entries, exits) Default: False
    trend_reset (value): Value used to identify if a trend has ended. Default: 0
    trade_offset (value): Value used shift the trade entries/exits. Default: -1
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: Returns columns: Returns, Cumulative Returns,
    Trends (trend: 1, no trend: 0), Trades (Enter: 1, Exit: -1, Otherwise: 0),
    Entries (entry: 1, nothing: 0), Exits (exit: 1, nothing: 0)
"""
