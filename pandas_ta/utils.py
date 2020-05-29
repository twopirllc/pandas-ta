# -*- coding: utf-8 -*-
import math
import numpy as np
import pandas as pd

from functools import reduce
from operator import mul
from sys import float_info as sflt

TRADING_DAYS_IN_YEAR = 250
TRADING_HOURS_IN_DAY = 6.5
MINUTES_IN_HOUR = 60


def _above_below(series_a:pd.Series, series_b:pd.Series, above:bool =True, asint:bool =True, offset:int =None, **kwargs):
    series_a = verify_series(series_a)
    series_b = verify_series(series_b)
    offset = get_offset(offset)

    series_a.apply(zero)
    series_b.apply(zero)

    # Calculate Result
    if above:
        current = series_a >= series_b
    else:
        current = series_a <= series_b

    if asint:
        current = current.astype(int)

    # Offset
    if offset != 0:
        current = current.shift(offset)

    # Name & Category
    current.name = f"{series_a.name}_{'A' if above else 'B'}_{series_b.name}"
    current.category = 'utility'

    return current


def above(series_a:pd.Series, series_b:pd.Series, asint:bool =True, offset:int =None, **kwargs):
    return _above_below(series_a, series_b, above=True, asint=asint, offset=offset, **kwargs)


def above_value(series_a:pd.Series, value:float, asint:bool =True, offset:int =None, **kwargs):
    if not isinstance(value, (int, float, complex)):
        print("[X] value is not a number")
        return
    series_b = pd.Series(value, index=series_a.index, name=f"{value}".replace('.','_'))
    return _above_below(series_a, series_b, above=True, asint=asint, offset=offset, **kwargs)    


def below(series_a:pd.Series, series_b:pd.Series, asint:bool =True, offset:int =None, **kwargs):
    return _above_below(series_a, series_b, above=False, asint=asint, offset=offset, **kwargs)


def below_value(series_a:pd.Series, value:float, asint:bool =True, offset:int =None, **kwargs):
    if not isinstance(value, (int, float, complex)):
        print("[X] value is not a number")
        return
    series_b = pd.Series(value, index=series_a.index, name=f"{value}".replace('.','_'))
    return _above_below(series_a, series_b, above=False, asint=asint, offset=offset, **kwargs)


def combination(**kwargs):
    """https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python"""
    n = int(math.fabs(kwargs.pop('n', 1)))
    r = int(math.fabs(kwargs.pop('r', 0)))

    if kwargs.pop('repetition', False) or kwargs.pop('multichoose', False):
        n = n + r - 1

    # if r < 0: return None
    r = min(n, n - r)
    if r == 0:
        return 1

    numerator   = reduce(mul, range(n, n - r, -1), 1)
    denominator = reduce(mul, range(1, r + 1), 1)
    return numerator // denominator


def cross_value(series_a:pd.Series, value:float, above:bool =True, asint:bool =True, offset:int =None, **kwargs):
    series_b = pd.Series(value, index=series_a.index, name=f"{value}".replace('.','_'))
    return cross(series_a, series_b, above, asint, offset, **kwargs)

def cross(series_a:pd.Series, series_b:pd.Series, above:bool =True, asint:bool =True, offset:int =None, **kwargs):
    series_a = verify_series(series_a)
    series_b = verify_series(series_b)
    offset = get_offset(offset)

    series_a.apply(zero)
    series_b.apply(zero)

    # Calculate Result
    current = series_a > series_b   # current is above
    previous = series_a.shift(1) < series_b.shift(1) # previous is below
    # above if both are true, below if both are false
    cross = current & previous if above else ~current & ~previous

    if asint:
        cross = cross.astype(int)

    # Offset
    if offset != 0:
        cross = cross.shift(offset)

    # Name & Category
    cross.name = f"{series_a.name}_{'XA' if above else 'XB'}_{series_b.name}"
    cross.category = 'utility'

    return cross


def is_datetime_ordered(df: pd.DataFrame or pd.Series) -> bool:
    """Returns True if the index is a datetime and ordered."""
    index_is_datetime = pd.api.types.is_datetime64_any_dtype(df.index)
    try:
        ordered = df.index[0] < df.index[-1]
    except RuntimeWarning: pass
    finally:
        return True if index_is_datetime and ordered else False


def signals(indicator, xa, xb, cross_values, xserie, xserie_a, xserie_b, cross_series, offset):
    df = pd.DataFrame()
    if xa is not None and isinstance(xa, (int, float)):
        if cross_values:
            crossed_above_start = cross_value(indicator, xa, above=True, offset=offset)
            crossed_above_end = cross_value(indicator, xa, above=False, offset=offset)
            df[crossed_above_start.name] = crossed_above_start
            df[crossed_above_end.name] = crossed_above_end
        else:
            crossed_above = above_value(indicator, xa, offset=offset)
            df[crossed_above.name] = crossed_above

    if xb is not None and isinstance(xb, (int, float)):
        if cross_values:
            crossed_below_start = cross_value(indicator, xb, above=True, offset=offset)
            crossed_below_end = cross_value(indicator, xb, above=False, offset=offset)
            df[crossed_below_start.name] = crossed_below_start
            df[crossed_below_end.name] = crossed_below_end
        else:
            crossed_below = below_value(indicator, xb, offset=offset)
            df[crossed_below.name] = crossed_below

    # xseries is the default value for both xserie_a and xserie_b
    if xserie_a is None:
        xserie_a = xserie
    if xserie_b is None:
        xserie_b = xserie

    if xserie_a is not None and verify_series(xserie_a):
        if cross_series:
            cross_serie_above = cross(indicator, xserie_a, above=True, offset=offset)
        else:
            cross_serie_above = above(indicator, xserie_a, offset=offset)

        df[cross_serie_above.name] = cross_serie_above

    if xserie_b is not None and verify_series(xserie_b):
        if cross_series:
            cross_serie_below = cross(indicator, xserie_b, above=False, offset=offset)
        else:
            cross_serie_below = below(indicator, xserie_b, offset=offset)

        df[cross_serie_below.name] = cross_serie_below

    return df


def df_error_analysis(dfA:pd.DataFrame, dfB:pd.DataFrame, **kwargs):
    """ """
    col = kwargs.pop('col', None)
    corr_method = kwargs.pop('corr_method', 'pearson')

    # Find their differences
    diff = dfA - dfB
    df = pd.DataFrame({'diff': diff.describe()})
    extra = pd.DataFrame([diff.var(), diff.mad(), diff.sem(), dfA.corr(dfB, method=corr_method)], index=['var', 'mad', 'sem', 'corr'])

    # Append the differences to the DataFrame
    df = df['diff'].append(extra, ignore_index=False)[0]

    # For plotting
    if kwargs.pop('plot', False):
        diff.hist()
        if diff[diff > 0].any():
            diff.plot(kind='kde')
    
    if col is not None:
        return df[col]
    else:
        return df


def fibonacci(**kwargs):
    """Fibonacci Sequence as a numpy array"""
    n = int(math.fabs(kwargs.pop('n', 2)))
    zero = kwargs.pop('zero', False)
    weighted = kwargs.pop('weighted', False)

    if zero:
        a, b = 0, 1
    else:
        n -= 1
        a, b = 1, 1

    result = np.array([a])
    for i in range(0, n):
        a, b = b, a + b
        result = np.append(result, a)

    if weighted:
        fib_sum = np.sum(result)
        if fib_sum > 0:
            return result / fib_sum
        else:
            return result
    else:
        return result


def get_drift(x:int):
    """Returns an int if not zero, otherwise defaults to one."""
    return int(x) if x and x != 0 else 1


def get_offset(x:int):
    """Returns an int, otherwise defaults to zero."""
    return int(x) if x else 0


def non_zero_range(high:pd.Series, low:pd.Series):
    """Returns the difference of two series and adds epsilon if
    to any zero values.  This occurs commonly in crypto data when
    high = low.
    """
    diff = high - low
    if diff.eq(0).any().any():
        diff += sflt.epsilon
    return diff


def pascals_triangle(n:int =None, **kwargs):
    """Pascal's Triangle

    Returns a numpy array of the nth row of Pascal's Triangle.
    n=4  => triangle: [1, 4, 6, 4, 1]
         => weighted: [0.0625, 0.25, 0.375, 0.25, 0.0625
         => inverse weighted: [0.9375, 0.75, 0.625, 0.75, 0.9375]
    """
    n = int(math.fabs(n)) if n is not None else 0
    weighted = kwargs.pop('weighted', False)
    inverse = kwargs.pop('inverse', False)

    # Calculation
    triangle = np.array([combination(n=n, r=i) for i in range(0, n + 1)])
    triangle_sum = np.sum(triangle)
    triangle_weights = triangle / triangle_sum
    inverse_weights = 1 - triangle_weights

    if weighted and inverse:
        return inverse_weights
    if weighted:
        return triangle_weights
    if inverse:
        return None

    return triangle


def recent_maximum_index(x):
    return int(np.argmax(x[::-1]))


def recent_minimum_index(x):
    return int(np.argmin(x[::-1]))


def signed_series(series:pd.Series, initial:int =None):
    """Returns a Signed Series with or without an initial value"""
    series = verify_series(series)
    sign = series.diff(1)
    sign[sign > 0] = 1
    sign[sign < 0] = -1
    sign.iloc[0] = initial
    return sign


def symmetric_triangle(n:int =None, **kwargs):
    n = int(math.fabs(n)) if n is not None else 2
    weighted = kwargs.pop('weighted', False)

    if n == 2:
        triangle = [1, 1]

    if n > 2:
        if n % 2 == 0:
            front = [i + 1 for i in range(0, math.floor(n/2))]
            triangle = front + front[::-1]
        else:
            front = [i + 1 for i in range(0, math.floor(0.5 * (n + 1)))]
            triangle = front.copy()
            front.pop()
            triangle += front[::-1]

    if weighted:
        triangle_sum = np.sum(triangle)
        triangle_weights = triangle / triangle_sum
        return triangle_weights

    return triangle


def verify_series(series:pd.Series):
    """If a Pandas Series return it."""
    if series is not None and isinstance(series, pd.core.series.Series):
        return series


def weights(w):
    def _dot(x):
        return np.dot(w, x)
    return _dot


def zero(x):
    """If the value is close to zero, then return zero.  Otherwise return the value."""
    return 0 if -sflt.epsilon < x and x < sflt.epsilon else x