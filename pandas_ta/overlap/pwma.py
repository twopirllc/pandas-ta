# -*- coding: utf-8 -*-
from pandas_ta.utils import get_offset, pascals_triangle, verify_series, weights


def pwma(close, length=None, asc=None, offset=None, **kwargs):
    """Indicator: Pascals Weighted Moving Average (PWMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs["min_periods"]) if "min_periods" in kwargs and kwargs["min_periods"] is not None else length
    asc = asc if asc else True
    offset = get_offset(offset)

    # Calculate Result
    triangle = pascals_triangle(n=length - 1, weighted=True)
    pwma = close.rolling(length, min_periods=length).apply(weights(triangle), raw=True)

    # Offset
    if offset != 0:
        pwma = pwma.shift(offset)

    # Name & Category
    pwma.name = f"PWMA_{length}"
    pwma.category = "overlap"

    return pwma


pwma.__doc__ = \
"""Pascal's Weighted Moving Average (PWMA)

Pascal's Weighted Moving Average is similar to a symmetric triangular window
except PWMA's weights are based on Pascal's Triangle.

Source: Kevin Johnson

Calculation:
    Default Inputs:
        length=10

    def weights(w):
        def _compute(x):
            return np.dot(w * x)
        return _compute

    triangle = utils.pascals_triangle(length + 1)
    PWMA = close.rolling(length)_.apply(weights(triangle), raw=True)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    asc (bool): Recent values weigh more. Default: True
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
