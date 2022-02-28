# -*- coding: utf-8 -*-
from numpy import arange, dot
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.utils import v_ascending, v_offset, v_pos_default
from pandas_ta.utils import v_series, v_talib


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
        fill_method (value, optional): Type of fill method

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
        total_weight = 0.5 * length * (length + 1)
        weights_ = Series(arange(1, length + 1))
        weights = weights_ if asc else weights_[::-1]

        def linear(w):
            def _compute(x):
                return dot(x, w) / total_weight
            return _compute

        close_ = close.rolling(length, min_periods=length)
        wma = close_.apply(linear(weights), raw=True)

    # Offset
    if offset != 0:
        wma = wma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        wma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        wma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    wma.name = f"WMA_{length}"
    wma.category = "overlap"

    return wma
