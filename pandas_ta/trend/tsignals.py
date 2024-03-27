# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_bool, v_drift, v_int, v_offset, v_series



def tsignals(
    trend: Series, asbool: bool = None,
    trend_reset: Int = None, trade_offset: Int = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Trend Signals

    Given a Trend, Trend Signals returns the Trend, Trades, Entries and
    Exits as boolean integers. When 'asbool=True', it returns Trends, Entries
    and Exits as boolean values which is helpful when combined with the
    vectorbt backtesting package.

    A Trend can be a simple as: 'close' > 'moving average' or something more
    complex whose values are boolean or integers (0 or 1).

    Examples:
        ta.tsignals(close > ta.sma(close, 50), asbool=False)

        ta.tsignals(ta.ema(close, 8) > ta.ema(close, 21), asbool=True)

    Source:
        Kevin Johnson

    Args:
        trend (pd.Series): Series of 'trend's. The trend can be either a
            boolean or integer series of '0's and '1's
        asbool (bool): If True, it converts the Trends, Entries and Exits
            columns to booleans. When boolean, it is also useful for
            backtesting with vectorbt's
            Portfolio.from_signal(close, entries, exits) Default: False
        trend_reset (value): Value used to identify if a trend has ended.
            Default: 0
        trade_offset (value): Value used shift the trade entries/exits
            use 1 for backtesting and 0 for live. Default: 0
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame with columns:
        Trends (trend: 1, no trend: 0),
        Trades (Enter: 1, Exit: -1, Otherwise: 0),
        Entries (entry: 1, nothing: 0),
        Exits (exit: 1, nothing: 0)
    """
    # Validate
    trend = v_series(trend)
    asbool = v_bool(asbool, False)
    trend_reset = v_int(trend_reset, 0)
    trade_offset = v_int(trade_offset, 0)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    trends = trend.astype(int)
    trades = trends.diff(drift).shift(trade_offset).fillna(0).astype(int)
    entries = (trades > 0).astype(int)
    exits = (trades < 0).abs().astype(int)

    if asbool:
        trends = trends.astype(bool)
        entries = entries.astype(bool)
        exits = exits.astype(bool)

    data = {
        f"TS_Trends": trends,
        f"TS_Trades": trades,
        f"TS_Entries": entries,
        f"TS_Exits": exits,
    }
    df = DataFrame(data, index=trends.index)

    # Offset
    if offset != 0:
        df = df.shift(offset)

    # Fill
    if "fillna" in kwargs:
        df.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    df.name = f"TS"
    df.category = "trend"

    return df
