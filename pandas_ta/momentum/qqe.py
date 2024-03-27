# -*- coding: utf-8 -*-
from numpy import isnan, maximum, minimum, nan
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.ma import ma
from pandas_ta.utils import (
    v_drift,
    v_mamode,
    v_offset,
    v_pos_default,
    v_scalar,
    v_series
)
from .rsi import rsi



def qqe(
    close: Series, length: Int = None,
    smooth: Int = None, factor: IntFloat = None,
    mamode: str = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Quantitative Qualitative Estimation (QQE)

    The Quantitative Qualitative Estimation (QQE) is similar to SuperTrend
    but uses a Smoothed RSI with an upper and lower bands. The band width
    is a combination of a one period True Range of the Smoothed RSI which
    is double smoothed using Wilder's smoothing length (2 * rsiLength - 1)
    and multiplied by the default factor of 4.236. A Long trend is
    determined when the Smoothed RSI crosses the previous upperband and
    a Short trend when the Smoothed RSI crosses the previous lowerband.

    Based on QQE.mq5 by EarnForex Copyright © 2010
    Based on version by Tim Hyder (2008),
    Based on version by Roman Ignatov (2006)

    Sources:
        https://www.tradingview.com/script/IYfA9R2k-QQE-MT4/
        https://www.tradingpedia.com/forex-trading-indicators/quantitative-qualitative-estimation
        https://www.prorealcode.com/prorealtime-indicators/qqe-quantitative-qualitative-estimation/

    Args:
        close (pd.Series): Series of 'close's
        length (int): RSI period. Default: 14
        smooth (int): RSI smoothing period. Default: 5
        factor (float): QQE Factor. Default: 4.236
        mamode (str): See ``help(ta.ma)``. Default: 'sma'
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: QQE, RSI_MA (basis), QQEl (long), QQEs (short) columns.
    """
    # Validate
    length = v_pos_default(length, 14)
    smooth = v_pos_default(smooth, 5)
    wilders_length = 2 * length - 1
    _length = wilders_length + smooth
    close = v_series(close, _length)

    if close is None:
        return

    factor = v_scalar(factor, 4.236)
    mamode = v_mamode(mamode, "ema")
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    rsi_ = rsi(close, length)
    _mode = mamode.lower()[0] if mamode != "ema" else ""
    rsi_ma = ma(mamode, rsi_, length=smooth)

    # RSI MA True Range
    rsi_ma_tr = rsi_ma.diff(drift).abs()
    if all(isnan(rsi_ma_tr)):
        return

    # Double Smooth the RSI MA True Range using Wilder's Length with a default
    # width of 4.236.
    smoothed_rsi_tr_ma = ma("ema", rsi_ma_tr, length=wilders_length)
    if all(isnan(smoothed_rsi_tr_ma)):
        return  # Emergency Break
    dar = factor * ma("ema", smoothed_rsi_tr_ma, length=wilders_length)
    if all(isnan(dar)):
        return  # Emergency Break

    # Create the Upper and Lower Bands around RSI MA.
    upperband = rsi_ma + dar
    lowerband = rsi_ma - dar

    m = close.size
    long = Series(0, index=close.index)
    short = Series(0, index=close.index)
    trend = Series(1, index=close.index)
    qqe = Series(rsi_ma.iat[0], index=close.index)
    qqe_long = Series(nan, index=close.index)
    qqe_short = Series(nan, index=close.index)

    for i in range(1, m):
        c_rsi, p_rsi = rsi_ma.iat[i], rsi_ma.iat[i - 1]
        c_long, p_long = long.iat[i - 1], long.iat[i - 2]
        c_short, p_short = short.iat[i - 1], short.iat[i - 2]

        # Long Line
        if p_rsi > c_long and c_rsi > c_long:
            long.iat[i] = maximum(c_long, lowerband.iat[i])
        else:
            long.iat[i] = lowerband.iat[i]

        # Short Line
        if p_rsi < c_short and c_rsi < c_short:
            short.iat[i] = minimum(c_short, upperband.iat[i])
        else:
            short.iat[i] = upperband.iat[i]

        # Trend & QQE Calculation
        # Long: Current RSI_MA value Crosses the Prior Short Line Value
        # Short: Current RSI_MA Crosses the Prior Long Line Value
        if (c_rsi > c_short and p_rsi < p_short) or \
            (c_rsi <= c_short and p_rsi >= p_short):
            trend.iat[i] = 1
            qqe.iat[i] = qqe_long.iat[i] = long.iat[i]
        elif (c_rsi > c_long and p_rsi < p_long) or \
            (c_rsi <= c_long and p_rsi >= p_long):
            trend.iat[i] = -1
            qqe.iat[i] = qqe_short.iat[i] = short.iat[i]
        else:
            trend.iat[i] = trend.iat[i - 1]
            if trend.iat[i] == 1:
                qqe.iat[i] = qqe_long.iat[i] = long.iat[i]
            else:
                qqe.iat[i] = qqe_short.iat[i] = short.iat[i]

    # Offset
    if offset != 0:
        rsi_ma = rsi_ma.shift(offset)
        qqe = qqe.shift(offset)
        long = long.shift(offset)
        short = short.shift(offset)

    # Fill
    if "fillna" in kwargs:
        rsi_ma.fillna(kwargs["fillna"], inplace=True)
        qqe.fillna(kwargs["fillna"], inplace=True)
        qqe_long.fillna(kwargs["fillna"], inplace=True)
        qqe_short.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"{_mode}_{length}_{smooth}_{factor}"
    qqe.name = f"QQE{_props}"
    rsi_ma.name = f"QQE{_props}_RSI{_mode.upper()}MA"
    qqe_long.name = f"QQEl{_props}"
    qqe_short.name = f"QQEs{_props}"
    qqe.category = rsi_ma.category = "momentum"
    qqe_long.category = qqe_short.category = qqe.category

    data = {
        qqe.name: qqe,
        rsi_ma.name: rsi_ma,
        # long.name: long,
        # short.name: short
        qqe_long.name: qqe_long,
        qqe_short.name: qqe_short
    }
    df = DataFrame(data, index=close.index)
    df.name = f"QQE{_props}"
    df.category = qqe.category

    return df
