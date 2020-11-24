# -*- coding: utf-8 -*-
from pandas_ta.utils import get_offset, verify_series


def kurtosis(close, length=None, offset=None, **kwargs):
    """Indicator: Kurtosis"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 30
    min_periods = int(kwargs["min_periods"]) if "min_periods" in kwargs and kwargs["min_periods"] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    kurtosis = close.rolling(length, min_periods=min_periods).kurt()

    # Offset
    if offset != 0:
        kurtosis = kurtosis.shift(offset)

    # Name & Category
    kurtosis.name = f"KURT_{length}"
    kurtosis.category = "statistics"

    return kurtosis


kurtosis.__doc__ = \
"""Rolling Kurtosis

Sources:

Calculation:
    Default Inputs:
        length=30
    KURTOSIS = close.rolling(length).kurt()

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period. Default: 30
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
