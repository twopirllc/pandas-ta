# -*- coding: utf-8 -*-
from numpy import sqrt
from pandas import Series
from pandas_ta.utils import get_offset, verify_series
from .wma import wma


def hma(
    close: Series, length: int = None,
    offset: int = None, **kwargs
) -> Series:
    """Hull Moving Average (HMA)

    The Hull Exponential Moving Average attempts to reduce or remove lag in moving
    averages.

    Sources:
        https://alanhull.com/hull-moving-average

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 10
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None:
        return

    # Calculate
    half_length = int(length / 2)
    sqrt_length = int(sqrt(length))

    wmaf = wma(close=close, length=half_length)
    wmas = wma(close=close, length=length)
    hma = wma(close=2 * wmaf - wmas, length=sqrt_length)

    # Offset
    if offset != 0:
        hma = hma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        hma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        hma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    hma.name = f"HMA_{length}"
    hma.category = "overlap"

    return hma
