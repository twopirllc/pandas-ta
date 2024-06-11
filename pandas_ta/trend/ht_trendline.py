# -*- coding: utf-8 -*-
from numpy import arctan, copy, isnan, nan, rad2deg, zeros_like, zeros
from numba import njit
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    v_bool,
    v_offset,
    v_pos_default,
    v_series,
    v_talib
)



@njit(cache=True)
def nb_ht_trendline(x):
    a, b, m = 0.0962, 0.5769, x.size

    wma4, dt = zeros_like(x), zeros_like(x)
    q1, q2 = zeros_like(x), zeros_like(x)
    ji, jq = zeros_like(x), zeros_like(x)
    i1, i2 = zeros_like(x), zeros_like(x)
    re, im = zeros_like(x), zeros_like(x)
    period, smp = zeros_like(x), zeros_like(x)
    i_trend = zeros_like(x)

    result = zeros_like(x)
    result[:13] = x[:13]

    # Ehler's starts from 6, TALib from 63
    for i in range(6, m):
        adj_prev_period = 0.075 * period[i - 1] + 0.54

        wma4[i] = 0.4 * x[i] + 0.3 * x[i - 1] + 0.2 * x[i - 2] + 0.1 * x[i - 3]
        dt[i] = adj_prev_period * (a * wma4[i] + b * wma4[i - 2] - b * wma4[i - 4] - a * wma4[i - 6])

        q1[i] = adj_prev_period * (a * dt[i] + b * dt[i - 2] - b * dt[i - 4] - a * dt[i - 6])
        i1[i] = dt[i - 3]

        ji[i] = adj_prev_period * (a * i1[i] + b * i1[i - 2] - b * i1[i - 4] - a * i1[i - 6])
        jq[i] = adj_prev_period * (a * q1[i] + b * q1[i - 2] - b * q1[i - 4] - a * q1[i - 6])

        i2[i] = i1[i] - jq[i]
        q2[i] = q1[i] + ji[i]

        i2[i] = 0.2 * i2[i] + 0.8 * i2[i - 1]
        q2[i] = 0.2 * q2[i] + 0.8 * q2[i - 1]

        re[i] = i2[i] * i2[i - 1] + q2[i] * q2[i - 1]
        im[i] = i2[i] * q2[i - 1] - q2[i] * i2[i - 1]

        re[i] = 0.2 * re[i] + 0.8 * re[i - 1]
        im[i] = 0.2 * im[i] + 0.8 * im[i - 1]

        if re[i] != 0 and im[i] != 0:
            period[i] = 360.0 / rad2deg(arctan(im[i] / re[i]))
        if period[i] > 1.5 * period[i - 1]:
            period[i] = 1.5 * period[i - 1]
        if period[i] < 0.67 * period[i - 1]:
            period[i] = 0.67 * period[i - 1]
        if period[i] < 6.0:
            period[i] = 6.0
        if period[i] > 50.0:
            period[i] = 50.0
        period[i] = 0.2 * period[i] + 0.8 * period[i - 1]
        smp[i] = 0.33 * period[i] + 0.67 * smp[i - 1]

        dc_period = int(smp[i] + 0.5)
        dcp_avg = 0
        for k in range(dc_period):
            dcp_avg += x[i - k]

        if dc_period > 0:
            dcp_avg /= dc_period

        i_trend[i] = dcp_avg

        if i > 12:
            result[i] = 0.4 * i_trend[i] + 0.3 * i_trend[i - 1] + 0.2 * i_trend[i - 2] + 0.1 * i_trend[i - 3]

    return result


def ht_trendline(
    close: Series = None, talib: bool = None,
    prenan: Int = None, offset: Int = None,
    **kwargs: DictLike
) -> Series:
    """Hilbert Transform TrendLine (HT_TL)

    The Hilbert Transform TrendLine or Instantaneous TrendLine as described
    in Ehler's "Rocket Science for Traders" Book attempts to smooth the
    source by using a bespoke application of the Hilbert Transform.

    Sources:
        https://c.mql5.com/forextsd/forum/59/023inst.pdf
        https://github.com/TA-Lib/ta-lib/blob/main/src/ta_func/ta_HT_TRENDLINE.c

    Args:
        close (pd.Series): Series of 'close's.
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        prenan (int): Prenans to apply. Ehler's 6 or 12, TALib 63
            Default: 63
        offset (int, optional): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: Hilbert Transformation Instantaneous Trend-line.
    """
    # Validate
    prenan = v_pos_default(prenan, 63)
    close = v_series(close, prenan)

    if close is None:
        return

    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    if Imports["talib"] and mode_tal:
        from talib import HT_TRENDLINE
        tl = HT_TRENDLINE(close)
    else:
        np_close = close.to_numpy()
        np_tl = nb_ht_trendline(np_close)

        if prenan > 0:
            np_tl[:prenan] = nan
        tl = Series(np_tl, index=close.index)

    if all(isnan(tl)):
        return  # Emergency Break

    # Offset
    if offset != 0:
        trend_line = tl.shift(offset)

    # Fill
    if "fillna" in kwargs:
        tl.fillna(kwargs["fillna"], inplace=True)

    tl.name = f"HT_TL"
    tl.category = "trend"

    return tl
