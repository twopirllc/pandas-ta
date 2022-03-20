# -*- coding: utf-8 -*-
from numpy import nan, uintc, zeros_like
from pandas import Series
from pandas_ta._typing import Array, DictLike, Int, IntFloat
from pandas_ta.ma import ma
from pandas_ta.maps import Imports
from pandas_ta.utils import v_drift, v_mamode, v_offset
from pandas_ta.utils import v_pos_default, v_series, v_talib
from pandas_ta.volatility import atr


try:
    from numba import njit
except ImportError:
    def njit(_): return _


@njit
def np_atrts(x: Array, ma_: Array, atr_: Array, length: Int, ma_length: Int):
    m = x.size
    k = max(length, ma_length)

    result = x.copy()
    up = zeros_like(x, dtype=uintc)
    dn = zeros_like(x, dtype=uintc)

    expn = x > ma_
    up[expn], dn[~expn] = 1, 1
    up[:k], dn[:k] = 0, 0
    result[:k] = nan

    for i in range(k, m):
        pr = result[i - 1]
        if up[i]:
            result[i] = x[i] - atr_[i]
            if result[i] < pr:
                result[i] = pr
        if dn[i]:
            result[i] = x[i] + atr_[i]
            if result[i] > pr:
                result[i] = pr

    long, short = result * up, result * dn
    long[long == 0], short[short == 0] = nan, nan

    return result, long, short


def atrts(
    high: Series, low: Series, close: Series, length: Int = None,
    ma_length: Int = None, multiplier: IntFloat = None,
    mamode: str = None, talib: bool = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """ATR Trailing Stop (ATRTS)

    Attempts to identify exits for long and short positions using both ATR
    and a moving average (MA) to determine the trend.
    The Average True Range (ATR) is multiplied by a user defined factor.
    If the MA is increasing (uptrend), the ATR product is subtracted from
    the price or, if the MA is decreasing (down trend), it is added to the
    price, and along with a few details the ATRTS is formed. The user may
    change the position (long), input (close), method (EMA), period lengths,
    percent factor and show entry option(see trading signals below).

    Sources:
        https://www.motivewave.com/studies/atr_trailing_stops.htm

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): ATR length. Default: 14
        ma_length (int): MA Length. Default: 20
        multiplier (int): ATR multiplier. Default: 3
        mamode (str): See ``help(ta.ma)``. Default: 'ema'
        talib (bool): If TA Lib is installed and talib is True, Returns the
            TA Lib version. Default: True
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        percent (bool, optional): Return as percentage. Default: False
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 14)
    ma_length = v_pos_default(ma_length, 20)
    _length = max(length, ma_length)
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return

    multiplier = v_pos_default(multiplier, 3.0)
    mamode = v_mamode(mamode, "ema")
    mode_tal = v_talib(talib)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import ATR
        atr_ = ATR(high, low, close, length)
    else:
        atr_ = atr(
            high=high, low=low, close=close, length=length,
            mamode=mamode, drift=drift, talib=mode_tal,
            offset=offset, **kwargs
        )

    atr_ *= multiplier
    ma_ = ma(mamode, close, length=ma_length, talib=mode_tal)

    np_close, np_ma, np_atr = close.values, ma_.values, atr_.values
    np_atrts_, _, _ = np_atrts(np_close, np_ma, np_atr, length, ma_length)

    percent = kwargs.pop("percent", False)
    if percent:
        np_atrts_ *= 100 / np_close

    atrts = Series(np_atrts_, index=close.index)

    # Offset
    if offset != 0:
        atrts = atrts.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        atrts.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        atrts.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    _props = f"ATRTS{mamode[0]}{'p' if percent else ''}"
    atrts.name = f"{_props}_{length}_{ma_length}_{multiplier}"
    atrts.category = "volatility"

    return atrts