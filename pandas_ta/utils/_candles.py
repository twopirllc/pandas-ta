# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.utils._core import non_zero_range

__all__ = ["candle_color", "high_low_range", "real_body"]


def candle_color(open_: Series, close: Series) -> Series:
    """Candle Change

    Returns 1 or -1 if close >= open_ respectively.
    """
    color = close.copy().astype(int)
    color[close >= open_] = 1
    color[close < open_] = -1
    return color


def high_low_range(high: Series, low: Series) -> Series:
    """High Low Range

    Returns high - low = epsilon > 0
    """
    return non_zero_range(high, low)


def real_body(open_: Series, close: Series) -> Series:
    """Body Low Range

    Returns close - open_ = epsilon > 0
    """
    return non_zero_range(close, open_)
