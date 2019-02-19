# -*- coding: utf-8 -*-
import math
import numpy as np
import pandas as pd

from functools import reduce
from operator import mul
from sys import float_info as sflt



def combination(**kwargs):
    """https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python"""
    n = int(math.fabs(kwargs.pop('n', 1)))
    r = int(math.fabs(kwargs.pop('r', 0)))

    if kwargs.pop('repetition', False) or kwargs.pop('multichoose', False):
        n = n + r - 1

    if r < 0:
        return None
    r = min(n, n - r)
    if r == 0:
        return 1

    numerator   = reduce(mul, range(n, n - r, -1), 1)
    denominator = reduce(mul, range(1, r + 1), 1)
    return numerator // denominator


def dropna(df:pd.DataFrame):
    """Drop rows with 'Nan' values"""
    df = df[df < math.exp(709)] # big number
    df = df[df != 0.0]
    df = df.dropna()
    return df


def fibonacci(**kwargs):
    """Fibonacci Sequence as a numpy array"""
    n = int(math.fabs(kwargs.pop('n', 2)))
    zero = kwargs.pop('zero', True)
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
        return result / fib_sum
    else:
        return result


def get_drift(x:int):
    """Returns an int if not zero, otherwise defaults to one."""
    return int(x) if x and x != 0 else 1


def get_offset(x:int):
    """Returns an int, otherwise defaults to zero."""
    return int(x) if x else 0


def pascals_triangle(**kwargs):
    """Pascal's Triangle

    Returns a numpy array of the nth row of Pascal's Triangle.
    """
    n = kwargs.pop('n', 5)
    weighted = kwargs.pop('weighted', False)

    if n < 0: return None
    sink = kwargs.pop('all', False)

    # Calculation
    triangle = np.array([combination(n=n, r=i) for i in range(0, n + 1)])

    # Variations and Properties
    max_ = np.max(triangle)
    inverted = max_ - triangle
    triangle_sum = np.sum(triangle)
    triangle_avg = np.average(triangle)

    weights = triangle / triangle_sum
    inv_weights = inverted / triangle_sum

    if sink:
        return triangle, triangle_sum, triangle_avg, inverted, weights, inv_weights, triangle_avg
    if weighted:
        return weights
    else:
        return triangle


def signed_series(series:pd.Series, initial:int = None):
    """Returns a Signed Series with or without an initial value"""
    series = verify_series(series)
    sign = series.diff(1)
    sign[sign > 0] = 1
    sign[sign < 0] = -1
    sign.iloc[0] = initial
    return sign


def verify_series(series:pd.Series):
    """If a Pandas Series return it."""
    if series is not None and isinstance(series, pd.core.series.Series):
        return series


def zero(x):
    """If the value is close to zero, then return zero.  Otherwise return the value."""
    return 0 if -sflt.epsilon < x and x < sflt.epsilon else x