# -*- coding: utf-8 -*-
from numpy import nan, zeros_like, arctan
from numba import njit
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import v_offset, v_pos_default, v_series, zero


@njit
def np_ht_trendline(x):
    # Variables used for the Hilbert Transformation
    a, b = 0.0962, 0.5769

    m = x.size
    smooth_price = zeros_like(m)
    de_trender = zeros_like(m)
    q1 = zeros_like(m)
    i1 = zeros_like(m)
    i2 = zeros_like(m)
    q2 = zeros_like(m)
    _re = zeros_like(m)
    _im = zeros_like(m)
    i_trend = zeros_like(m)

    period, _prev_i2, _prev_q2, _re, _im, smooth_period = 0, 0, 0, 0, 0, 0

    for i in range(x.size):
        if i > 50:
            smooth_price[i] = (4 * x[i] + 3 * x[i - 1] + 2 * x[i - 2] + x[i - 3]) / 10
        else:
            smooth_price[i] = 0

    for i in range(x.size):
        adjusted_prev_period = 0.075 * period + 0.54

        de_trender = (a * smooth_price[i] + b * smooth_price[i - 2] -
                      b * smooth_price[i - 4] - a * smooth_price[i - 6]) * adjusted_prev_period

        q1[i] = (a * de_trender[i] + b * de_trender[i-2] -
                 b * de_trender[i-4] - a * de_trender[i-6]) * adjusted_prev_period
        i1[i] = de_trender[i-3]
        ji = (a * i1[i] + b * i1[i-2] - b * i1[i-4] - a * i1[i-6]) * adjusted_prev_period
        jq = (a * q1[i] + b * q1[i-2] - b * q1[i-4] - a * q1[i-6]) * adjusted_prev_period

        i2[i] = i1[i] - jq
        q2[i] = q1[i] + ji

        i2 = 0.2 * i2[i] + 0.8 * i2[i-1]
        q2 = 0.2 * q2[i] + 0.8 * q2[i-1]

        _re[i] = i2[i] * i2[i-1] + q2[i] * q2[i-1]
        _im[i] = i2[i] * q2[i-1] - q2[i] * i2[i-1]

        _re[i] = 0.2 * _re[i] + 0.8 * _re[i-1]
        _im[i] = 0.2 * _im[i] + 0.8 * _im[i-1]

        new_period = 0
        if _re[i] and _im[i]:
            new_period = 360 / arctan(_re[i]/_im[i])
        if new_period > 1.5 * period:
            new_period = 1.5 * period
        if new_period < 0.67 * period:
            new_period = 0.67 * period
        if new_period < 6:
            new_period = 6
        if new_period > 50:
            new_period = 50
        period = 0.2 * new_period + 0.8 * period
        smooth_period = 0.33 * period + 0.67 * smooth_period

        dc_period = int(smooth_period + 0.5)
        temp_real = 0
        for k in range(dc_period):
            temp_real += x[i-k]

        if dc_period > 0:
            temp_real /= dc_period

        i_trend[i] = temp_real
        trend_line = (4 * i_trend[i] + 3 * i_trend[i-1] + 2 * i_trend[i-2] + i_trend[i-3]) / 10.0

    return trend_line


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
        # calculate ht_trendline using numba
        np_close = close.values
        trend_line = np_ht_trendline(np_close)

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
