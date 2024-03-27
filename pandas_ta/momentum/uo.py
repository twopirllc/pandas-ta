# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    v_drift,
    v_offset,
    v_pos_default,
    v_series,
    v_talib
)



def uo(
    high: Series, low: Series, close: Series,
    fast: Int = None, medium: Int = None, slow: Int = None,
    fast_w: IntFloat = None, medium_w: IntFloat = None, slow_w: IntFloat = None,
    talib: bool = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Ultimate Oscillator (UO)

    The Ultimate Oscillator is a momentum indicator over three different
    periods.  It attempts to correct false divergence trading signals.

    Sources:
        https://www.tradingview.com/wiki/Ultimate_Oscillator_(UO)

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        fast (int): The Fast %K period. Default: 7
        medium (int): The Slow %K period. Default: 14
        slow (int): The Slow %D period. Default: 28
        fast_w (float): The Fast %K period. Default: 4.0
        medium_w (float): The Slow %K period. Default: 2.0
        slow_w (float): The Slow %D period. Default: 1.0
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    fast = v_pos_default(fast, 7)
    medium = v_pos_default(medium, 14)
    slow = v_pos_default(slow, 28)
    _length = max(fast, medium, slow) + 1
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return

    fast_w = v_pos_default(fast_w, 4.0)
    medium_w = v_pos_default(medium_w, 2.0)
    slow_w = v_pos_default(slow_w, 1.0)
    mode_tal = v_talib(talib)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import ULTOSC
        uo = ULTOSC(high, low, close, fast, medium, slow)
    else:
        close_drift = close.shift(drift)
        tdf = DataFrame({
            "high": high, "low": low, f"close_{drift}": close_drift
        })
        max_h_or_pc = tdf.loc[:, ["high", f"close_{drift}"]].max(axis=1)
        min_l_or_pc = tdf.loc[:, ["low", f"close_{drift}"]].min(axis=1)
        del tdf

        bp = close - min_l_or_pc
        tr = max_h_or_pc - min_l_or_pc

        fast_avg = bp.rolling(fast).sum() / tr.rolling(fast).sum()
        medium_avg = bp.rolling(medium).sum() / tr.rolling(medium).sum()
        slow_avg = bp.rolling(slow).sum() / tr.rolling(slow).sum()

        total_weight = fast_w + medium_w + slow_w
        weights = (fast_w * fast_avg) + (medium_w * medium_avg) \
            + (slow_w * slow_avg)
        uo = 100 * weights / total_weight

    # Offset
    if offset != 0:
        uo = uo.shift(offset)

    # Fill
    if "fillna" in kwargs:
        uo.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    uo.name = f"UO_{fast}_{medium}_{slow}"
    uo.category = "momentum"

    return uo
