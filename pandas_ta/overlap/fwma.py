# -*- coding: utf-8 -*-
import numpy as np
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import (
    fibonacci,
    v_ascending,
    v_offset,
    v_pos_default,
    v_series
)

def fwma(
    close: Series, length: Int = None, asc: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Fibonacci's Weighted Moving Average (FWMA)

    Fibonacci's Weighted Moving Average is similar to a Weighted Moving
    Average (WMA) where the weights are based on the Fibonacci Sequence.

    Source: Kevin Johnson

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        asc (bool): Recent values weigh more. Default: True
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
    offset = v_offset(offset)

    # Calculate
    fibs = fibonacci(n=length, weighted=True)
    # Reverse the weights
    fib_weights = fibs[::-1]
    # Total weight for normalization
    total_weight = fibs.sum()
    fwma_values = np.convolve(close, fib_weights, 'valid') / total_weight
    _fwma = np.concatenate((np.full(length-1, np.nan), fwma_values))
    _fwma = Series(_fwma, index=close.index)

    # Offset
    if offset != 0:
        _fwma = _fwma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        _fwma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        _fwma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _fwma.name = f"FWMA_{length}"
    _fwma.category = "overlap"

    return _fwma
