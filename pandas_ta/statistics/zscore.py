# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.overlap import sma
from pandas_ta.statistics import stdev
from pandas_ta.utils import get_offset, verify_series


def zscore(
    close: Series, length: int = None, std: float = None,
    offset: int = None, **kwargs
) -> Series:
    """Rolling Z Score

    Calculates the Z Score over a rolling period.

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 30
        std (float): It's period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 1 else 30
    std = float(std) if std and std > 1 else 1
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None:
        return

    # Calculate
    std *= stdev(close=close, length=length, **kwargs)
    mean = sma(close=close, length=length, **kwargs)
    zscore = (close - mean) / std

    # Offset
    if offset != 0:
        zscore = zscore.shift(offset)

    # Fill
    if "fillna" in kwargs:
        zscore.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        zscore.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    zscore.name = f"ZS_{length}"
    zscore.category = "statistics"

    return zscore
