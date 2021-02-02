# -*- coding: utf-8 -*-
from numpy import fabs as npfabs
from pandas_ta.utils import get_offset, verify_series


def mad(close, length=None, offset=None, **kwargs):
    """Indicator: Mean Absolute Deviation"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 30
    min_periods = int(kwargs["min_periods"]) if "min_periods" in kwargs and kwargs["min_periods"] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    def mad_(series):
        """Mean Absolute Deviation"""
        return npfabs(series - series.mean()).mean()

    mad = close.rolling(length, min_periods=min_periods).apply(mad_, raw=True)

    # Offset
    if offset != 0:
        mad = mad.shift(offset)

    # Name & Category
    mad.name = f"MAD_{length}"
    mad.category = "statistics"

    return mad


mad.__doc__ = \
"""Rolling Mean Absolute Deviation

Sources:

Calculation:
    Default Inputs:
        length=30
    mad = close.rolling(length).mad()

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
