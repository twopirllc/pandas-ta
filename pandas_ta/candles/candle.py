# -*- coding: utf-8 -*-
from pandas_ta.utils import get_offset, non_zero_range, verify_series

def candle_color(open_, close):
    color = close.copy().astype(int)
    color[close >= open_] = 1
    color[close < open_] = -1
    return color

def real_body(open_, close):
    return non_zero_range(open_, close)

def high_low_range(high, low):
    return non_zero_range(high, low)