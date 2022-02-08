# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.utils import get_offset, symmetric_triangle, verify_series, weights


def swma(
    close: Series, length: int = None, asc: bool = None,
    offset: int = None, **kwargs
) -> Series:
    """Symmetric Weighted Moving Average (SWMA)

    Symmetric Weighted Moving Average where weights are based on a symmetric
    triangle.  For example: n=3 -> [1, 2, 1], n=4 -> [1, 2, 2, 1], etc...
    This moving average has variable length in contrast to TradingView's
    fixed length of 4.

    Source:
        https://www.tradingview.com/study-script-reference/#fun_swma

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
    length = int(length) if length and length > 0 else 10
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None:
        return

    # Calculate
    triangle = symmetric_triangle(length, weighted=True)
    swma = close.rolling(length, min_periods=length) \
        .apply(weights(triangle), raw=True)

    # Offset
    if offset != 0:
        swma = swma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        swma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        swma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    swma.name = f"SWMA_{length}"
    swma.category = "overlap"

    return swma
