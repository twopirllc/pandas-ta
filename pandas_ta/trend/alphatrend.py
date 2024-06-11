# -*- coding: utf-8 -*-
from numpy import isnan, nan, zeros_like
from numba import njit
from pandas import DataFrame, Series
from pandas_ta._typing import Array, DictLike, Int, IntFloat
from pandas_ta.momentum import rsi
from pandas_ta.volatility import atr
from pandas_ta.volume.mfi import mfi
from pandas_ta.utils import (
    v_mamode,
    v_offset,
    v_pos_default,
    v_series,
    v_str,
    v_talib
)



@njit(cache=True)
def nb_alpha(low_atr, high_atr, momo_threshold):
    m = momo_threshold.size
    result = zeros_like(low_atr)

    for i in range(1, m):
        if momo_threshold[i]:
            if low_atr[i] < result[i - 1]:
                result[i] = result[i - 1]
            else:
                result[i] = low_atr[i]
        else:
            if high_atr[i] > result[i - 1]:
                result[i] = result[i - 1]
            else:
                result[i] = high_atr[i]
    result[0] = nan

    return result


def alphatrend(
    open_: Series, high: Series, low: Series, close: Series,
    volume: Series = None, src: str = None,
    length: int = None, multiplier: IntFloat = None,
    threshold: IntFloat = None, lag: Int = None,
    mamode: str = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
):
    """ Alpha Trend (alphatrend)

    Alpha Trend attemps to solve the problems of Magic Trend. For instance, it
    tries to ilter out sideways market conditions and yield more accurate
    BUY/SELL signals

    Sources:
        https://www.tradingview.com/script/o50NYLAZ-AlphaTrend/
        https://github.com/OnlyFibonacci/AlgoSeyri/blob/main/alphaTrendIndicator.py

    Args:
        open (pd.series): series of 'open's
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's. Default: None
        src (str): One of 'open', 'high', 'low' or 'close'. Default: 'close'
        length (int): Length for ATR, MFI, or RSI. Default: 14
        multiplier (float): Trailing ATR value. Default: 1
        threshold (float): Momentum threshold. Default: 50
        lag (int): Lag period of main trend. Default: 2
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: trend, trendlag of all the input.
    """
    # Validate
    length = v_pos_default(length, 14)
    open_ = v_series(open_, length)
    high = v_series(high, length)
    low = v_series(low, length)
    close = v_series(close, length)

    if open_ is None or high is None or low is None or close is None:
        return

    _src = {"open": open_, "high": high, "low": low, "close": close}
    src = v_str(src, "close")
    src = src if src in _src.keys() else "close"

    multiplier = v_pos_default(multiplier, 1)
    threshold = v_pos_default(threshold, 50)
    lag = v_pos_default(lag, 2)

    mamode = v_mamode(mamode, "sma")
    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    if volume is not None:
        volume = v_series(volume)
        if volume is None:
            return

    # Calculate
    atr_ = atr(
        high=high, low=low, close=close, length=length,
        mamode=mamode, talib=mode_tal
    )

    if atr_ is None or all(isnan(atr_)):
        return

    lower_atr = low - atr_ * multiplier
    upper_atr = high + atr_ * multiplier

    momo = None
    if volume is None:
        momo = rsi(close=_src[src], length=length, mamode=mamode, talib=mode_tal)
    else:
        momo = mfi(
            high=high, low=low, close=close, volume=volume,
            length=length, talib=mode_tal
        )

    if momo is None:
        return

    np_upper_atr, np_lower_atr = upper_atr.to_numpy(), lower_atr.to_numpy()

    at = nb_alpha(np_lower_atr, np_upper_atr, momo.to_numpy() >= threshold)
    at = Series(at, index=close.index)

    atl = at.shift(lag)

    if all(isnan(at)) or all(isnan(atl)):
        return  # Emergency Break

    # Offset
    if offset != 0:
        at = at.shift(offset)
        atl = atl.shift(offset)

    # Fill
    if "fillna" in kwargs:
        at.fillna(kwargs["fillna"], inplace=True)
        atl.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"_{length}_{multiplier}_{threshold}"
    at.name = f"ALPHAT{_props}"
    atl.name = f"ALPHATl{_props}_{lag}"
    at.category = atl.category = "trend"

    data = {at.name: at, atl.name: atl}
    df = DataFrame(data, index=close.index)
    df.name = at.name
    df.category = at.category

    return df
