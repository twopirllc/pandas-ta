# -*- coding: utf-8 -*-
from numpy import append, arange, array, exp, floor, nan, tensordot
from numpy.version import version as np_version
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas import Series
from pandas_ta.utils import strided_window, v_offset, v_pos_default, v_series



def alma(
    close: Series, length: Int = None,
    sigma: IntFloat = None, dist_offset: IntFloat = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Arnaud Legoux Moving Average (ALMA)

    The ALMA moving average uses the curve of the Normal (Gauss) distribution,
    which can be shifted from 0 to 1. This allows regulating the smoothness
    and high sensitivity of the indicator. Sigma is another parameter that is
    responsible for the shape of the curve coefficients. This moving average
    reduces lag of the data in conjunction with smoothing to reduce noise.

    Sources:
        https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=475&Name=Moving_Average_-_Arnaud_Legoux
        https://www.prorealcode.com/prorealtime-indicators/alma-arnaud-legoux-moving-average/

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period, window size. Default: 9
        sigma (float): Smoothing value. Default 6.0
        dist_offset (float): Value to offset the distribution where
            min 0 (smoother), max 1 (more responsive). Default 0.85
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 9)
    close = v_series(close, length)

    if close is None:
        return

    sigma = v_pos_default(sigma, 6.0)

    if isinstance(dist_offset, float) and 0 <= dist_offset <= 1:
        offset_ = float(dist_offset)
    else:
        offset_ = 0.85

    offset = v_offset(offset)

    # Calculate
    np_close = close.to_numpy()
    x = arange(length)
    k = floor(offset_ * (length - 1))
    weights = exp(-0.5 * ((sigma / length) * (x - k)) ** 2)
    weights /= weights.sum()

    if np_version >= "1.20.0":
        from numpy.lib.stride_tricks import sliding_window_view
        window = sliding_window_view(np_close, length)
    else:
        window = strided_window(np_close, length)
    result = append(array([nan] * (length - 1)),
                    tensordot(window, weights, axes=1))
    alma = Series(result, index=close.index)

    # Offset
    if offset != 0:
        alma = alma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        alma.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    alma.name = f"ALMA_{length}_{sigma}_{offset_}"
    alma.category = "overlap"

    return alma
