# -*- coding: utf-8 -*-
import math
from ..utils import get_offset, verify_series

def linreg(close, length=None, offset=None, **kwargs):
    """Indicator: Linear Regression"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)
    angle = kwargs.pop('angle', False)
    intercept = kwargs.pop('intercept', False)
    degrees = kwargs.pop('degrees', False)
    r = kwargs.pop('r', False)
    slope = kwargs.pop('slope', False)
    tsf = kwargs.pop('tsf', False)

    # Calculate Result
    x = range(1, length + 1) # [1, 2, ..., n] from 1 to n keeps Sum(xy) low
    x_sum = 0.5 * length * (length + 1)
    x2_sum = x_sum * (2 * length + 1) / 3
    divisor = length * x2_sum - x_sum * x_sum

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
            theta = math.atan(m)
            if degrees:
                theta *= 180 / math.pi
            return theta
        
        if r:
            y2_sum = (series * series).sum()
            rn = length * xy_sum - x_sum * y_sum
            rd = math.sqrt(divisor * (length * y2_sum - y_sum * y_sum))
            return rn / rd

        return m * length + b if tsf else m * (length - 1) + b

    linreg = close.rolling(length, min_periods=length).apply(linear_regression, raw=False)

    # Offset
    if offset != 0:
        linreg = linreg.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        linreg.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        linreg.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    linreg.name = f"LR"
    if slope:
        linreg.name += "m"
    if intercept:
        linreg.name += "b"
    if angle:
        linreg.name += "a"
    if r:
        linreg.name += "r"
    linreg.name += f"_{length}"
    linreg.category = 'overlap'

    return linreg



linreg.__doc__ = \
"""Linear Regression Moving Average (linreg)

Linear Regression Moving Average

Source: TA Lib

Calculation:
    Default Inputs:
        length=14
    x = [1, 2, ..., n]
    x_sum = 0.5 * length * (length + 1)
    x2_sum = length * (length + 1) * (2 * length + 1) / 6
    divisor = length * x2_sum - x_sum * x_sum

    lr(series):
        y_sum = series.sum()
        y2_sum = (series* series).sum()
        xy_sum = (x * series).sum()

        m = (length * xy_sum - x_sum * y_sum) / divisor
        b = (y_sum * x2_sum - x_sum * xy_sum) / divisor
        return m * (length - 1) + b

    linreg = close.rolling(length).apply(lr)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method
    angle (bool, optional): Default: False.  If True, returns the angle of the slope in radians
    degrees (bool, optional): Default: False.  If True, returns the angle of the slope in degrees
    intercept (bool, optional): Default: False.  If True, returns the angle of the slope in radians
    r (bool, optional): Default: False.  If True, returns it's correlation 'r'
    slope (bool, optional): Default: False.  If True, returns the slope
    tsf (bool, optional): Default: False.  If True, returns the Time Series Forecast value.

Returns:
    pd.Series: New feature generated.
"""