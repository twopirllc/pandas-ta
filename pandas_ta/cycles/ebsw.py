# -*- coding: utf-8 -*-
from numpy import cos as npCos
from numpy import exp as npExp
from numpy import nan as npNaN
from numpy import pi as npPi
from numpy import sin as npSin
from numpy import sqrt as npSqrt
from numpy import zeros as npZeros
from numpy import roll as npRoll
from numpy import mean as npMean
from pandas import Series
from pandas_ta.utils import get_offset, verify_series


def ebsw(close, length=None, bars=None, offset=None, initial_version=False, **kwargs):
    """Even Better SineWave (EBSW)

    This indicator measures market cycles and uses a low pass filter to remove noise.
    Its output is bound signal between -1 and 1 and the maximum length of a detected
    trend is limited by its length input.

    Written by rengel8 for Pandas TA based on a publication at 'prorealcode.com' and
    a book by J.F.Ehlers. According to the suggestion by Squigglez2* and major differences between
    the initial version's output close to the implementation from Ehler's, the default version is now
    more closely related to the code from pro-realcode.

    Remark:
    The default version is now more cycle oriented and tends to be less whipsaw-prune. Thus the older version
    might offer earlier signals at medium and stronger reversals.
    A test against the version at TradingView showed very close results with the advantage to be one bar/candle
    faster, than the corresponding reference value. This might be pre-roll related and was not further investigated.
    * https://github.com/twopirllc/pandas-ta/issues/350


    Sources:
        - https://www.prorealcode.com/prorealtime-indicators/even-better-sinewave/
        - J.F.Ehlers 'Cycle Analytics for Traders', 2014

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's max cycle/trend period. Values between 40-48 work like
            expected with minimum value: 39. Default: 40.
        bars (int): Period of low pass filtering. Default: 10
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate arguments
    length = int(length) if isinstance(length, int) and length > 10 else 40
    bars = int(bars) if isinstance(bars, int) and bars > 0 else 10
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None: return

    # allow initial version to be used (more responsive/caution!)
    initial_version = bool(initial_version) if isinstance(initial_version, bool) else False

    if initial_version:
        # not the default version that is active
        alpha1 = hp = 0 # alpha and HighPass
        a1 = b1 = c1 = c2 = c3 = 0
        filter_ = power_ = wave = 0
        lastClose = lastHP = 0
        filtHist = [0, 0]   # Filter history

        # Calculate Result
        m = close.size
        result = [npNaN for _ in range(0, length - 1)] + [0]
        for i in range(length, m):
            # HighPass filter cyclic components whose periods are shorter than Duration input
            alpha1 = (1 - npSin(360 / length)) / npCos(360 / length)
            hp = 0.5 * (1 + alpha1) * (close[i] - lastClose) + alpha1 * lastHP

            # Smooth with a Super Smoother Filter from equation 3-3
            a1 = npExp(-npSqrt(2) * npPi / bars)
            b1 = 2 * a1 * npCos(npSqrt(2) * 180 / bars)
            c2 = b1
            c3 = -1 * a1 * a1
            c1 = 1 - c2 - c3
            filter_ = 0.5 * c1 * (hp + lastHP) + c2 * filtHist[1] + c3 * filtHist[0]
            # filter_ = float("{:.8f}".format(float(filter_))) # to fix for small scientific notations, the big ones fail

            # 3 Bar average of wave amplitude and power
            wave = (filter_ + filtHist[1] + filtHist[0]) / 3
            power_ = (filter_ * filter_ + filtHist[1] * filtHist[1] + filtHist[0] * filtHist[0]) / 3

            # Normalize the Average Wave to Square Root of the Average Power
            wave = wave / npSqrt(power_)

            # update storage, result
            filtHist.append(filter_)  # append new filter_ value
            filtHist.pop(0)  # remove first element of list (left) -> updating/trim
            lastHP = hp
            lastClose = close[i]
            result.append(wave)

    else:                                       # this version is the default version
        # Instance Variables
        lastHP = lastClose = 0
        filtHist = npZeros(3)
        result = [npNaN] * (length - 1) + [0]

        # Calculate constants
        angle = 2 * npPi / length
        alpha1 = (1 - npSin(angle)) / npCos(angle)
        ang = 2 ** .5 * npPi / bars
        a1 = npExp(-ang)
        c2 = 2 * a1 * npCos(ang)
        c3 = -a1 ** 2
        c1 = 1 - c2 - c3

        for i in range(length, close.size):
            hp = 0.5 * (1 + alpha1) * (close[i] - lastClose) + alpha1 * lastHP

            # Rotate filters to overwrite oldest value
            filtHist = npRoll(filtHist, -1)
            filtHist[-1] = 0.5 * c1 * (hp + lastHP) + c2 * filtHist[1] + c3 * filtHist[0]

            # Wave calculation
            wave = npMean(filtHist)
            rms = npSqrt(npMean(filtHist ** 2))
            wave = wave / rms

            # Update past values
            lastHP = hp
            lastClose = close[i]
            result.append(wave)

    ebsw = Series(result, index=close.index)

    # Offset
    if offset != 0:
        ebsw = ebsw.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        ebsw.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ebsw.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    ebsw.name = f"EBSW_{length}_{bars}"
    ebsw.category = "cycles"

    return ebsw
