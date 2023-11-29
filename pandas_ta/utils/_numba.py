# -*- coding: utf-8 -*-
from numpy import append, array, empty_like, nan, roll, zeros_like
from numba import njit

from pandas_ta._typing import Array, Int, IntFloat

__all__ = [
    "np_prenan",
    "np_prepend",
    "np_rolling",
    "np_shift",
]


# Prepend n values, typically np.nan, to array x.
@njit
def np_prenan(x, n, value = nan):
    if n > 0:
        x[:n - 1] = value
        return x
    return x


# Prepend n values, typically np.nan, to array x.
@njit
def np_prepend(x, n, value = nan):
    return append(array([value] * n), x)


# Like Pandas Rolling Window. x.rolling(n).fn()
@njit
def np_rolling(x, n, fn = None):
    if fn is None:
        return x
    m = x.size
    result = zeros_like(x, dtype=float)
    if n <= 0:
        return result  # TODO: Handle negative rolling windows

    for i in range(0, m):
        result[i] = fn(x[i:n + i])
    result = roll(result, n - 1)
    result[:n - 1] = nan
    return result


# np shift
# shift5 - preallocate empty array and assign slice by chrisaycock
# https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
@njit
def np_shift(x, n, value = nan):
    result = empty_like(x)
    if n > 0:
        result[:n] = value
        result[n:] = x[:-n]
    elif n < 0:
        result[n:] = value
        result[:n] = x[-n:]
    else:
        result[:] = x
    return result


# Uncategorized
# @njit
# def np_roofing_filter(x: Array, n: Int, k: Int, pi: Float, sqrt2: Float):
#     """Ehler's Roofing Filter (INCOMPLETE)
#     http://traders.com/documentation/feedbk_docs/2014/01/traderstips.html"""
#     m, hp = x.size, np.copy(x)
#     # a = exp(-pi * sqrt(2) / n)
#     # b = 2 * a * cos(180 * sqrt(2) / n)
#     rsqrt2 = 1 / np.sqrt2
#     a  = (np.cos(rsqrt2 * 360 / n) + np.sin(rsqrt2 * 360 / n) - 1)
#     a /= np.cos(rsqrt2 * 360 / n)
#     b, c = 1 - a, (1 - a / 2)

#     for i in range(2, m):
#         hp = c * c * (x[i] - 2 * x[i - 1] + x[i - 2]) \
#             + 2 * b * hp[i - 1] - b * b * hp[i - 2]

#     result = np_ssf(hp, k, pi, rsqrt2)
#     return result
