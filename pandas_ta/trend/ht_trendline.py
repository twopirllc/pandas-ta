# -*- coding: utf-8 -*-
from numpy import nan
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import v_offset, v_pos_default, v_series, zero


def ht_trendline(
        close: Series = None, talib: bool = None, offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Hilbert Transform TrendLine (Also known as Instantaneous TrendLine)
    By removing Dominant Cycle (DC) of the time-series from itself, ht_trendline is calculated.

    Sources:
        https://c.mql5.com/forextsd/forum/59/023inst.pdf

    Args:
        close (pd.Series): Series of 'close's.
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: None
        offset (int, optional): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: Hilbert Transformation Instantaneous Trend-line.
    """
    # Validate
    _length = 1
    close = v_series(close, _length)

    if close is None:
        return

    mode_tal = v_talib(talib)
    if Imports["talib"] and mode_tal:
        from talib import HT_TRENDLINE
        trend_line = HT_TRENDLINE(close)
    else:
        # Variables used for the Hilbert Transformation
        a = 0.0962
        b = 0.5769

        # calculate ht_trendline
        trend_line = None

    offset = v_offset(offset)

    # Offset
    if offset != 0:
        trend_line = trend_line.shift(offset)

    # Fill
    if "fillna" in kwargs:
        trend_line.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        trend_line.fillna(method=kwargs["fill_method"], inplace=True)

    data = {
        "ht_trendline": trend_line,
    }
    df = DataFrame(data, index=close.index)
    df.name = "ht_trendline"
    df.category = "trend"

    return df
