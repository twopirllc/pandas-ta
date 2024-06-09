# -*- coding: utf-8 -*-
from numba import njit
from pandas import Series
from pandas_ta._typing import Array, DictLike, Int, IntFloat
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    nb_idiff,
    nb_shift,
    v_offset,
    v_pos_default,
    v_scalar,
    v_series,
    v_talib
)
from .mom import mom



@njit(cache=True)
def nb_roc(x, n, k):
    return k * nb_idiff(x, n) / nb_shift(x, n)


def roc(
    close: Series, length: Int = None,
    scalar: IntFloat = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Rate of Change (ROC)

    Rate of Change is an indicator is also referred to as Momentum
    (yeah, confusingly). It is a pure momentum oscillator that measures the
    percent change in price with the previous price 'n' (or length)
    periods ago.

    Sources:
        https://www.tradingview.com/wiki/Rate_of_Change_(ROC)

    Args:
        close (pd.Series): Series of 'close's
        length (int): Its period. Default: 10
        scalar (float): How much to magnify. Default: 100
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
    close = v_series(close, length + 1)

    if close is None:
        return

    scalar = v_scalar(scalar, 100)
    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import ROC
        roc = ROC(close, length)
    else:
        # roc = scalar * mom(close=close, length=length, talib=mode_tal) \
            # / close.shift(length)
        np_close = close.values
        _roc = nb_roc(np_close, length, scalar)
        roc = Series(_roc, index=close.index)

    # Offset
    if offset != 0:
        roc = roc.shift(offset)

    # Fill
    if "fillna" in kwargs:
        roc.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    roc.name = f"ROC_{length}"
    roc.category = "momentum"

    return roc
