# -*- coding: utf-8 -*-
from sys import float_info as sflt
from numpy import arctan, nan, pi, zeros_like
from numpy.version import version as np_version
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    strided_window,
    v_offset,
    v_pos_default,
    v_series,
    v_talib,
    zero
)


def linreg(
    close: Series, length: Int = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Linear Regression Moving Average (linreg)

    Linear Regression Moving Average (LINREG). This is a simplified version
    of a Standard Linear Regression. LINREG is a rolling regression of one
    variable. A Standard Linear Regression is between two or more variables.

    Source: TA Lib

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        angle (bool, optional): If True, returns the slope angle in radians.
            Default: False.
        degrees (bool, optional): If True, returns the slope angle in
            degrees. Default: False.
        intercept (bool, optional): If True, returns the intercept.
            Default: False.
        r (bool, optional): If True, returns it's correlation 'r'.
            Default: False.
        slope (bool, optional): If True, returns the slope. Default: False.
        tsf (bool, optional): If True, returns the Time Series Forecast value.
            Default: False.
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 14)
    close = v_series(close, length)

    if close is None:
        return

    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    angle = kwargs.pop("angle", False)
    intercept = kwargs.pop("intercept", False)
    degrees = kwargs.pop("degrees", False)
    r = kwargs.pop("r", False)
    slope = kwargs.pop("slope", False)
    tsf = kwargs.pop("tsf", False)
    stdev = kwargs.pop("stdev", False)

    # Calculate
    np_close = close.values

    if Imports["talib"] and mode_tal and not r:
        from talib import LINEARREG, LINEARREG_ANGLE, LINEARREG_INTERCEPT, LINEARREG_SLOPE, TSF
        if tsf:
            _linreg = TSF(close, timeperiod=length)
        elif slope:
            _linreg = LINEARREG_SLOPE(close, timeperiod=length)
        elif intercept:
            _linreg = LINEARREG_INTERCEPT(close, timeperiod=length)
        elif angle:
            _linreg = LINEARREG_ANGLE(close, timeperiod=length)
        else:
            _linreg = LINEARREG(close, timeperiod=length)
    else:
        linreg_ = zeros_like(np_close)
        # [1, 2, ..., n] from 1 to n keeps Sum(xy) low
        x = range(1, length + 1)
        x_sum = 0.5 * length * (length + 1)
        x2_sum = x_sum * (2 * length + 1) / 3
        divisor = length * x2_sum - x_sum * x_sum

        # Needs to be reworked outside the method
        def linear_regression(series):
            y_sum = series.sum()
            xy_sum = (x * series).sum()

            m = (length * xy_sum - x_sum * y_sum) / divisor
            if slope:
                return m
            b = (y_sum * x2_sum - x_sum * xy_sum) / divisor
            if intercept:
                return b

            if angle:
                theta = arctan(m)
                if degrees:
                    theta *= 180 / pi
                return theta

            if r:
                y2_sum = (series * series).sum()
                rn = length * xy_sum - x_sum * y_sum
                rd = (divisor * (length * y2_sum - y_sum * y_sum)) ** 0.5
                if zero(rd) == 0:
                    rd = sflt.epsilon
                return rn / rd

            return m * length + b if not tsf else m * (length - 1) + b
        
        def stdevlinreg(close, length):
            x_value = close
            stdev = close
            slope = linreg(close=close, length=length, slope=True)
            tsf = linreg(close=close, length=length, tsf=True)
            variance = 0
            for i in range(1, length):
                variance += (x_value.shift(i) - (tsf - i * slope)) ** 2
            stdev = (variance / (length - 1)) ** 0.5
            return stdev

        if np_version >= "1.20.0":
            from numpy.lib.stride_tricks import sliding_window_view
            linreg_ = [
                linear_regression(_) for _ in sliding_window_view(
                    np_close, length)
            ]

        else:
            linreg_ = [
                linear_regression(_) for _ in strided_window(
                    np_close, length)
            ]

        _linreg = Series([nan] * (length - 1) + linreg_, index=close.index)

    # Offset
    if offset != 0:
        _linreg = _linreg.shift(offset)

    # Standard Deviation
    if stdev:
        _linreg = stdevlinreg(close, length)

    # Fill
    if "fillna" in kwargs:
        _linreg.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        _linreg.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _linreg.name = f"LINREG"
    if slope:
        _linreg.name += "m"
    if intercept:
        _linreg.name += "b"
    if angle:
        _linreg.name += "a"
    if r:
        _linreg.name += "r"
    if stdev:
        _linreg.name += "stdev"

    _linreg.name += f"_{length}"
    _linreg.category = "overlap"

    return _linreg
