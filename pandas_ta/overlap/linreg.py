# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    v_offset,
    v_pos_default,
    v_series,
    v_talib
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
        np_close = close.to_numpy()
        x = np.arange(1, length + 1)
        x_sum = 0.5 * length * (length + 1)
        x2_sum = x_sum * (2 * length + 1) / 3
        divisor = length * x2_sum - x_sum ** 2

        if np.__version__ >= "1.20.0":
            from numpy.lib.stride_tricks import sliding_window_view
            windows = sliding_window_view(np_close, window_shape=length)
        else:
            windows = np.array([np_close[i:i+length] for i in range(len(np_close)-length+1)])

        y_sums = windows.sum(axis=1)
        xy_sums = (x * windows).sum(axis=1)
        m_values = (length * xy_sums - x_sum * y_sums) / divisor
        b_values = (y_sums * x2_sum - x_sum * xy_sums) / divisor

        if slope:
            result = m_values
        elif intercept:
            result = b_values
        elif angle:
            theta = np.arctan(m_values)
            if degrees:
                theta *= 180 / np.pi
            result = theta
        elif r:
            y2_sums = (windows ** 2).sum(axis=1)
            rn = length * xy_sums - x_sum * y_sums
            rd = np.sqrt(divisor * (length * y2_sums - y_sums ** 2))
            rd[rd == 0] = np.finfo(float).eps  # Prevent division by zero
            result = rn / rd
        else:
            result = m_values * length + b_values

        # Match the length of the input series
        _linreg = np.concatenate((np.full(length - 1, np.nan), result))

        _linreg = pd.Series(_linreg, index=close.index)

    # Offset
    if offset != 0:
        _linreg = _linreg.shift(offset)

    # Fill
    if "fillna" in kwargs:
        _linreg.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        _linreg.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _linreg.name = "LINREG"
    if slope:
        _linreg.name += "m"
    if intercept:
        _linreg.name += "b"
    if angle:
        _linreg.name += "a"
    if r:
        _linreg.name += "r"

    _linreg.name += f"_{length}"
    _linreg.category = "overlap"

    return _linreg
