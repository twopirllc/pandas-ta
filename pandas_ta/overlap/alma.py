# -*- coding: utf-8 -*-
from numpy import floor as npFloor
from numpy import append as npAppend
from numpy import arange as npArange
from numpy import array as npArray
from numpy import exp as npExp
from numpy import nan as npNaN
from numpy import tensordot as npTensordot
from numpy.version import version as npVersion
from pandas import Series
from pandas_ta.utils import get_offset, strided_window, verify_series


def alma(close, length=None, sigma=None, dist_offset=None, offset=None, **kwargs):
    """Arnaud Legoux Moving Average (ALMA)

    The ALMA moving average uses the curve of the Normal (Gauss) distribution, which
    can be shifted from 0 to 1. This allows regulating the smoothness and high
    sensitivity of the indicator. Sigma is another parameter that is responsible for
    the shape of the curve coefficients. This moving average reduces lag of the data
    in conjunction with smoothing to reduce noise.

    Sources:
        https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=475&Name=Moving_Average_-_Arnaud_Legoux
        https://www.prorealcode.com/prorealtime-indicators/alma-arnaud-legoux-moving-average/

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period, window size. Default: 9
        sigma (float): Smoothing value. Default 6.0
        dist_offset (float): Value to offset the distribution where min 0 (smoother),
            max 1 (more responsive). Default 0.85
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate Arguments
    length = int(length) if isinstance(length, int) and length > 0 else 9
    sigma = float(sigma) if isinstance(sigma, float) and sigma > 0 else 6.0
    if isinstance(dist_offset, float) and dist_offset >= 0 and dist_offset <= 1:
        offset_ = float(dist_offset)
    else:
        offset_ = 0.85
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None: return

    # Calculate Result
    x = npArange(length)
    k = npFloor(offset_ * (length - 1))
    weights = npExp(-0.5 * ((sigma / length) * (x - k)) ** 2)
    weights /= weights.sum()

    if npVersion >= "1.20.0":
        from numpy.lib.stride_tricks import sliding_window_view
        window = sliding_window_view(npArray(close), length)
    else:
        window = strided_window(npArray(close), length)
    result = npAppend(npArray([npNaN] * (length - 1)), npTensordot(window, weights, axes=1))
    alma = Series(result, index=close.index)

    # Offset
    if offset != 0:
        alma = alma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        alma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        alma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    alma.name = f"ALMA_{length}_{sigma}_{offset_}"
    alma.category = "overlap"

    return alma
