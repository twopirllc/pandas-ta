# -*- coding: utf-8 -*-
from numpy import convolve, ones
from numba import njit
from pandas import Series
from pandas_ta._typing import Array, DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    nb_prepend,
    v_offset,
    v_pos_default,
    v_series,
    v_talib
)



# Fast SMA Options: https://github.com/numba/numba/issues/4119
@njit(cache=True)
def nb_sma(x, n):
    result = convolve(ones(n) / n, x)[n - 1:1 - n]
    return nb_prepend(result, n - 1)


def sma(
    close: Series, length: Int = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Simple Moving Average (SMA)

    The Simple Moving Average is the classic moving average that is the
    equally weighted average over its length.

    Sources:
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/simple-moving-average-sma/

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        adjust (bool): Default: True
        presma (bool, optional): If True, uses SMA for initial value.
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 10)
    if "min_periods" in kwargs and kwargs["min_periods"] is not None:
        min_periods = int(kwargs["min_periods"])
    else:
        min_periods = length
    close = v_series(close, max(length, min_periods))

    if close is None:
        return

    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal and length > 1:
        from talib import SMA
        sma = SMA(close, length)
    else:
        np_close = close.to_numpy()
        sma = nb_sma(np_close, length)
        sma = Series(sma, index=close.index)

    # Offset
    if offset != 0:
        sma = sma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        sma.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    sma.name = f"SMA_{length}"
    sma.category = "overlap"

    return sma
