# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_series


def ha(
    open_: Series, high: Series, low: Series, close: Series,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Heikin Ashi Candles (HA)

    The Heikin-Ashi technique averages price data to create a Japanese
    candlestick chart that filters out market noise. Heikin-Ashi charts,
    developed by Munehisa Homma in the 1700s, share some characteristics
    with standard candlestick charts but differ based on the values used
    to create each candle. Instead of using the open, high, low, and close
    like standard candlestick charts, the Heikin-Ashi technique uses a
    modified formula based on two-period averages. This gives the chart a
    smoother appearance, making it easier to spots trends and reversals,
    but also obscures gaps and some price data.

    Sources:
        https://www.investopedia.com/terms/h/heikinashi.asp

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
    # Validate
    open_ = v_series(open_)
    high = v_series(high)
    low = v_series(low)
    close = v_series(close)
    offset = v_offset(offset)

    # Calculate
    m = close.size
    df = DataFrame({
        "HA_open": 0.5 * (open_.iloc[0] + close.iloc[0]),
        "HA_high": high,
        "HA_low": low,
        "HA_close": 0.25 * (open_ + high + low + close),
    })

    for i in range(1, m):
        df["HA_open"].iloc[i] = 0.5 * (df["HA_open"].iloc[i - 1] \
            + df["HA_close"].iloc[i - 1])

    df["HA_high"] = df[["HA_open", "HA_high", "HA_close"]].max(axis=1)
    df["HA_low"] = df[["HA_open", "HA_low", "HA_close"]].min(axis=1)

    # Offset
    if offset != 0:
        df = df.shift(offset)

    # Fill
    if "fillna" in kwargs:
        df.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        df.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    df.name = "Heikin-Ashi"
    df.category = "candles"

    return df
