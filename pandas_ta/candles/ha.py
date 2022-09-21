# -*- coding: utf-8 -*-
import numpy as np
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, List
from pandas_ta.utils import v_offset, v_series

try:
    from numba import njit
except ImportError:
    def njit(_): return _


@njit
def heiken_ashi_numpy(c_open, c_high, c_low, c_close):
    """fast version using numpy and optionally numba"""
    ha_close = (c_open + c_high + c_low + c_close) / 4
    ha_open = np.empty_like(ha_close)
    ha_open[0] = (c_open[0] + c_close[0]) / 2
    for i in range(1, len(c_close)):
        ha_open[i] = (ha_open[i - 1] + ha_close[i - 1]) / 2
    ha_high = np.maximum(np.maximum(ha_open, ha_close), c_high)
    ha_low = np.minimum(np.minimum(ha_open, ha_close), c_low)
    return ha_open, ha_high, ha_low, ha_close

def heiken_ashi_series(open: Series, high: Series, low: Series, close: Series) -> List[Series]:
    """takes in series, outputs series."""
    inputs = [open, high, low, close]
    outs = heiken_ashi_numpy(open.values, high.values, low.values, close.values)
    outs = [Series(outs[i], index=inputs[i].index) for i in range(len(inputs))]
    return outs

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
    open_ = v_series(open_, 1)
    high = v_series(high, 1)
    low = v_series(low, 1)
    close = v_series(close, 1)
    offset = v_offset(offset)

    if open_ is None or high is None or low is None or close is None:
        return

    # Calculate
    ha_open, ha_high, ha_low, ha_close = heiken_ashi_series(open_, high, low, close)
    m = close.size
    df = DataFrame({
        "HA_open": ha_open,
        "HA_high": ha_high,
        "HA_low": ha_low,
        "HA_close": ha_close,
    })

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
