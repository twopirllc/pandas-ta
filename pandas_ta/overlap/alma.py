# -*- coding: utf-8 -*-
from numpy import exp as npExp
from numpy import nan as npNaN
from numpy import power as npPow
from numpy import dot as npDot
from numpy import empty as npEmpty
from numpy import array as npArray
from pandas import Series
from pandas_ta.utils import get_offset, verify_series


def alma(close, length=None, sigma=None, distribution_offset=None, offset=None, **kwargs):
    """Indicator: Arnaud Legoux Moving Average (ALMA)"""
    # Validate Arguments
    length = int(length) if length and length > 0 else 10
    sigma = float(sigma) if sigma and sigma > 0 else 6.0
    distribution_offset = float(distribution_offset) if distribution_offset and distribution_offset > 0 else 0.85
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None:
        return

    # Compute filter weights
    m = distribution_offset * (length - 1)
    s = length / sigma
    filter_index = npArray(range(length))
    weights = npExp(-npPow(filter_index - m, 2) / (2 * npPow(s, 2)))
    norm = weights.sum()

    result = npEmpty(close.shape)
    result[:] = npNaN
    valid_rng = range(length - 1, close.size)
    for j in valid_rng:
        subset = close[j - length + 1:j + 1]
        result[j] = npDot(subset, weights) / norm
    alma = Series(result, index=close.index)

    # Apply offset
    if offset != 0:
        alma = alma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    alma.name = f"ALMA_{length}_{sigma}_{distribution_offset}"
    alma.category = "overlap"

    return alma


alma.__doc__ = \
"""Arnaud Legoux Moving Average (ALMA)

The ALMA moving average uses the curve of the Normal (Gauss) distribution, which
can be shifted from 0 to 1. This allows regulating the smoothness and high
sensitivity of the indicator. Sigma is another parameter that is responsible for
the shape of the curve coefficients. This moving average reduces lag of the data
in conjunction with smoothing to reduce noise.

Implemented for Pandas TA by rengel8 based on the source provided below.

Sources:
    https://www.prorealcode.com/prorealtime-indicators/alma-arnaud-legoux-moving-average/

Calculation:
    refer to provided source

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period, window size. Default: 10
    sigma (float): Smoothing value. Default 6.0
    distribution_offset (float): Value to offset the distribution min 0
        (smoother), max 1 (more responsive). Default 0.85
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
