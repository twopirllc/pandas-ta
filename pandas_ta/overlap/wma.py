# -*- coding: utf-8 -*-
from numpy import arange, dot, float64, nan, zeros_like
from numba import njit
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    v_ascending,
    v_offset,
    v_pos_default,
    v_series,
    v_talib
)



@njit(cache=True)
def nb_wma(x, n, asc, prenan):
    m = x.size
    w = arange(1, n + 1, dtype=float64)
    result = zeros_like(x, dtype=float64)

    if not asc:
        w = w[::-1]

    for i in range(n - 1, m):
        result[i] = (w * x[i - n + 1:i + 1]).sum()
    result *= 2 / (n * n + n)

    if prenan:
        result[:n - 1] = nan

    return result


def wma(
    close: Series, length: Int = None,
    asc: bool = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Weighted Moving Average (WMA)

    The Weighted Moving Average where the weights are linearly increasing
    and the most recent data has the heaviest weight.

    Sources:
        https://en.wikipedia.org/wiki/Moving_average#Weighted_moving_average

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        asc (bool): Recent values weigh more. Default: True
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 10)
    close = v_series(close, length)

    if close is None:
        return

    asc = v_ascending(asc)
    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import WMA
        wma = WMA(close, length)
    else:
        np_close = close.to_numpy()
        wma_ = nb_wma(np_close, length, asc, True)
        wma = Series(wma_, index=close.index)

    # Offset
    if offset != 0:
        wma = wma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        wma.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    wma.name = f"WMA_{length}"
    wma.category = "overlap"

    return wma
