# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import get_offset, verify_series


def quantile(
    close: Series, length: Int = None, q: IntFloat = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Rolling Quantile

    Calculates the Quantile over a rolling period.

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 30
        q (float): The quantile. Default: 0.5
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 30
    if "min_periods" in kwargs and kwargs["min_periods"] is not None:
        min_periods = int(kwargs["min_periods"])
    else:
        min_periods = length
    q = float(q) if q and q > 0 and q < 1 else 0.5
    close = verify_series(close, max(length, min_periods))
    offset = get_offset(offset)

    if close is None:
        return

    # Calculate
    quantile = close.rolling(length, min_periods=min_periods).quantile(q)

    # Offset
    if offset != 0:
        quantile = quantile.shift(offset)

    # Fill
    if "fillna" in kwargs:
        quantile.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        quantile.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    quantile.name = f"QTL_{length}_{q}"
    quantile.category = "statistics"

    return quantile
