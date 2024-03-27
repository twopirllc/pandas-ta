# -*- coding: utf-8 -*-
from numpy import isnan, nan
from pandas import concat, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    non_zero_range,
    v_bool,
    v_drift,
    v_offset,
    v_series,
    v_talib
)



def true_range(
    high: Series, low: Series, close: Series,
    talib: bool = None, prenan: bool = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """True Range

    An method to expand a classical range (high minus low) to include
    possible gap scenarios.

    Sources:
        https://www.macroption.com/true-range/

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        prenan (bool): If True, behave like TA Lib with some initial nan
            based on drift (typically 1). Default: False
        drift (int): The shift period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature
    """
    # Validate
    _length = 1
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return

    mode_tal = v_talib(talib)
    prenan = v_bool(prenan, False)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import TRANGE
        true_range = TRANGE(high, low, close)
    else:
        hl_range = non_zero_range(high, low)
        pc = close.shift(drift)
        ranges = [hl_range, high - pc, pc - low]
        true_range = concat(ranges, axis=1)
        true_range = true_range.abs().max(axis=1)
        if prenan:
            true_range.iloc[:drift] = nan

    if all(isnan(true_range)):
        return  # Emergency Break

    # Offset
    if offset != 0:
        true_range = true_range.shift(offset)

    # Fill
    if "fillna" in kwargs:
        true_range.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    true_range.name = f"TRUERANGE_{drift}"
    true_range.category = "volatility"

    return true_range
