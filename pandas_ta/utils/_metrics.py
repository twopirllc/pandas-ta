# -*- coding: utf-8 -*-
from pandas import DataFrame, Series

from ._core import verify_series
from ._time import total_time

def cagr(close: Series) -> float:
    """Compounded Annual Growth Rate"""
    close = verify_series(close)
    start, end = close.iloc[0], close.iloc[-1]
    return ((end / start) ** (1 / total_time(close))) - 1