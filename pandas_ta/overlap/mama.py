# -*- coding: utf-8 -*-
from numpy import arctan, isnan, nan, zeros_like
from numba import njit
from pandas import DataFrame, Series
from pandas_ta._typing import Array, DictLike, Int, IntFloat
from pandas_ta.maps import Imports
from pandas_ta.utils import v_offset, v_pos_default, v_series, v_talib


# Ehler's Mother of Adaptive Moving Averages
# http://traders.com/documentation/feedbk_docs/2014/01/traderstips.html
@njit
def np_mama(x, fastlimit, slowlimit, prenan):
    a1, a2 = 0.0962, 0.5769
    p_w, smp_w, smp_w_c = 0.2, 0.33, 0.67 # smp_w + smp_w_c = 1

    sm = zeros_like(x)
    dt, smp, q1, q2 = sm.copy(), sm.copy(), sm.copy(), sm.copy()
    i1, i2, jI, jQ = sm.copy(), sm.copy(), sm.copy(), sm.copy()
    re, im, alpha = sm.copy(), sm.copy(), sm.copy()
    period, phase, mama, fama = sm.copy(), sm.copy(), sm.copy(), sm.copy()

    # Ehler's starts from 6, TV-LB starts at 3, TALib 32
    n = x.size
    for i in range(3, n):
        w_period = .075 * period[i - 1] + .54

        # Smoother and Detrend the Smoother
        sm[i] = 0.4 * x[i] + 0.3 * x[i - 1] + 0.2 * x[i - 2] + 0.1 * x[i - 3]
        dt[i] = w_period * (a1 * sm[i] + a2 * sm[i - 2] - a2 * sm[i - 4] - a1 * sm[i - 6])

        # Quadrature(Detrender) and In Phase Component
        q1[i] = w_period * (a1 * dt[i] + a2 * dt[i - 2] - a2 * dt[i - 4] - a1 * dt[i - 6])
        i1[i] = dt[i - 3]

        # Phase advance I1 and Q1 by 90 degrees
        jI[i] = w_period * (a1 * i1[i] + a2 * i1[i - 2] - a2 * i1[i - 4] - a1 * i1[i - 6])
        jQ[i] = w_period * (a1 * q1[i] + a2 * q1[i - 2] - a2 * q1[i - 4] - a1 * q1[i - 6])

        # Phasor Addition for 3 Bar Averaging
        i2[i] = i1[i] - jQ[i]
        q2[i] = q1[i] + jI[i]

        # Smooth I and Q components
        i2[i] = p_w * i2[i] + (1 - p_w) * i2[i - 1]
        q2[i] = p_w * q2[i] + (1 - p_w) * q2[i - 1]

        # Homodyne Discriminator
        re[i] = i2[i] * i2[i - 1] + q2[i] * q2[i - 1]
        im[i] = i2[i] * q2[i - 1] + q2[i] * i2[i - 1]

        re[i] = p_w * re[i] + (1 - p_w) * re[i - 1]
        im[i] = p_w * im[i] + (1 - p_w) * im[i - 1]

        if im[i] != 0.0 and re[i] != 0.0:
            period[i] = 360 / arctan(im[i] / re[i])
        else:
            period[i] = 0

        if period[i] > 1.5 * period[i - 1]:
            period[i] = 1.5 * period[i - 1]
        if period[i] < 0.67 * period[i - 1]:
            period[i] = 0.67 * period[i - 1]
        if period[i] < 6:
            period[i] = 6
        if period[i] > 50:
            period[i] = 50

        period[i] = p_w * period[i] + (1 - p_w) * period[i - 1]
        smp[i] = smp_w * period[i] + smp_w_c * smp[i - 1]

        if i1[i] != 0.0:
            phase[i] = arctan(q1[i] / i1[i])

        dphase = phase[i - 1] - phase[i]
        if dphase < 1:
            dphase = 1

        alpha[i] = fastlimit / dphase
        if alpha[i] > fastlimit:
            alpha[i] = fastlimit
        if alpha[i] < slowlimit:
            alpha[i] = slowlimit

        mama[i] = alpha[i] * x[i] + (1 - alpha[i]) * mama[i - 1]
        fama[i] = 0.5 * alpha[i] * mama[i] + (1 - 0.5 * alpha[i]) * fama[i - 1]

    mama[:prenan], fama[:prenan] = nan, nan
    return mama, fama


def mama(
    close: Series, fastlimit: IntFloat = None, slowlimit: IntFloat = None,
    prenan: Int = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Ehler's MESA Adaptive Moving Average (MAMA)

    Ehler's MESA Adaptive Moving Average (MAMA) aka the Mother of All Moving
    Averages attempts to adapt to the source's dynamic nature. The adapation
    is based on the rate change of phase as measured by the Hilbert
    Transform Discriminator. The advantage of this method of adaptation is
    that it features a fast attack average and a slow decay average so that
    the composite average rapidly adjusts to price changes and holds
    the average value until the next change occurs. This indicator also
    includes FAMA.

    Sources:
        Ehler's Mother of Adaptive Moving Averages:
            http://traders.com/documentation/feedbk_docs/2014/01/traderstips.html
        https://www.tradingview.com/script/foQxLbU3-Ehlers-MESA-Adaptive-Moving-Average-LazyBear/

    Args:
        close (pd.Series): Series of 'close's
        fastlimit (float): Fast limit. Default: 0.5
        slowlimit (float): Slow limit. Default: 0.05
        prenan (int): Prenans to apply. TV-LB 3, Ehler's 6, TALib 32
            Default: 3
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: MAMA and FAMA columns.
    """
    # Validate
    close = v_series(close, 1)

    if close is None:
        return

    fastlimit = v_pos_default(fastlimit, 0.5)
    slowlimit = v_pos_default(slowlimit, 0.05)
    prenan = v_pos_default(prenan, 3)
    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    np_close = close.values
    if Imports["talib"] and mode_tal:
        from talib import MAMA
        mama, fama = MAMA(np_close, fastlimit, slowlimit)
    else:
        mama, fama = np_mama(np_close, fastlimit, slowlimit, prenan)

    if all(isnan(mama)) or all(isnan(fama)):
        return  # Emergency Break

    # Name and Category
    _props = f"_{fastlimit}_{slowlimit}"
    data = {f"MAMA{_props}": mama, f"FAMA{_props}": fama}
    df = DataFrame(data, index=close.index)

    df.name = f"MAMA{_props}"
    df.category = "overlap"

    # Offset
    if offset != 0:
        df = df.shift(offset)

    # Fill
    if "fillna" in kwargs:
        df.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        df.fillna(method=kwargs["fill_method"], inplace=True)

    return df
