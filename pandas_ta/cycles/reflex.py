# -*- coding: utf-8 -*-
from numpy import nan as npNaN
from numpy import cos as npCos
from numpy import exp as npExp
from numpy import full as npFull
from numpy import pi as npPI
from numpy import sqrt as npSqrt
from pandas import Series
from pandas_ta.utils import get_offset, verify_series


def reflex(close, length=None, smooth=None, alpha=None, offset=None, **kwargs):
    """Reflex (reflex)

    John F. Ehlers introduced two indicators within the article
    "Reflex: A New Zero-Lag Indicator” in February 2020, TASC magazine. One of which
    is the Reflex, a lag reduced cycle indicator. Both indicators (Reflex/Trendflex)
    are oscillators and complement each other with the focus for  cycle and trend.

    Written for Pandas TA by rengel8 (2021-08-11) based on the implementation on
    ProRealCode (see Sources). Beyond the mentioned source, this implementation has
    a separate control parameter for the internal applied SuperSmoother.

    Sources:
        https://www.prorealcode.com/prorealtime-indicators/reflex-and-trendflex-indicators-john-f-ehlers/

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 20
        smooth (int): Period of internal SuperSmoother. Default: 20
        alpha (float: Alpha weight of Difference Sums. Default: 0.04
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate arguments
    close = verify_series(close, length)
    length = int(length) if isinstance(length, int) and length > 0 else 20
    smooth = int(smooth) if isinstance(smooth, int) and smooth > 0 else 20
    alpha = float(alpha) if isinstance(alpha, float) and alpha > 0 else 0.04
    offset = get_offset(offset)

    # Precalculations
    sqrt2 = npSqrt(2)
    m = close.size
    a1 = npExp(-sqrt2 * npPI / smooth)
    b1 = 2 * a1 * npCos(sqrt2 * 180 / smooth)
    c2 = b1
    c3 = -a1 * a1
    c1 = 1 - c2 - c3
    filter_ = npFull(m, 0)
    ms = npFull(m, 0)
    reflex = npFull(m, npNaN)

    # Calculation
    for i in range(2, m):
        # Gently smooth the data in a SuperSmoother
        filter_[i] = 0.5 * c1 * (close[i] + close[i - 1]) + c2 * filter_[i - 1] + c3 * filter_[i - 2]

        # Length is assumed cycle period
        slope = (filter_[i - length] - filter_[i]) / length

        # Sum the differences
        sum_ = 0
        for count in range(1, length):
            sum_ = sum_ + (filter_[i] + count * slope) - filter_[i - count]
        sum_ = sum_ / length

        # Normalize in terms of Standard Deviations
        ms[i] = alpha * sum_ * sum_ + (1 - alpha) * ms[i - 1]
        if ms[i] != 0:
            reflex[i] = sum_ / npSqrt(ms[i])
        else:
            reflex[i] = sum_ / 0.00001

    result = Series(reflex, index=close.index)

    # Neutralize pre-roll phase
    result.iloc[0:length] = npNaN

    # Offset
    if offset != 0:
        result = result.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        result.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        result.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    result.name = f"REFLEX_{length}_{smooth}_{alpha}"
    result.category = "cycles"

    return result
