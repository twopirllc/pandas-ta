# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.overlap import hl2
from pandas_ta.utils import v_offset, v_pos_default, v_series



def ttm_trend(
    high: Series, low: Series, close: Series, length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """TTM Trend (TTM_TRND)

    This indicator is from John Carters book “Mastering the Trade” and
    plots the bars green or red. It checks if the price is above or under
    the average price of the previous 5 bars. The indicator should hep you
    stay in a trade until the colors chance. Two bars of the opposite color
    is the signal to get in or out.

    Sources:
        https://www.prorealcode.com/prorealtime-indicators/ttm-trend-price/

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 6
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: ttm_trend.
    """
    # Validate
    length = v_pos_default(length, 6)
    high = v_series(high, length)
    low = v_series(low, length)
    close = v_series(close, length)

    if high is None or low is None or close is None:
        return

    offset = v_offset(offset)

    # Calculate
    trend_avg = hl2(high, low)
    for i in range(1, length):
        trend_avg = trend_avg + hl2(high.shift(i), low.shift(i))

    trend_avg = trend_avg / length

    tm_trend = (close > trend_avg).astype(int)
    tm_trend.replace(0, -1, inplace=True)

    # Offset
    if offset != 0:
        tm_trend = tm_trend.shift(offset)

    # Fill
    if "fillna" in kwargs:
        tm_trend.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    tm_trend.name = f"TTM_TRND_{length}"
    tm_trend.category = "momentum"

    df = DataFrame({tm_trend.name: tm_trend}, index=close.index)
    df.name = f"TTMTREND_{length}"
    df.category = tm_trend.category

    return df
