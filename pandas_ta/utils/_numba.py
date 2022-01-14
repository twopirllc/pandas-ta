# -*- coding: utf-8 -*-
from pandas_ta import np

# try:
#     from numba import jit, njit
# except ImportError as e:
#     from pandas_ta.utils._shim import jit, njit

try:
    from numba import njit
except ImportError:
    njit = lambda x: x


# Utilities
@njit
def np_prepend(x: np.ndarray, n: int, value=np.nan):
    """Append array x to an array of values, typically nan."""
    return np.append(np.array([value] * n), x)

@njit
def np_shift(x: np.ndarray, n: int, value=np.nan):
    """np shift
    shift5 - preallocate empty array and assign slice by chrisaycock
    https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
    """
    result = np.empty_like(x)
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
# def np_roofing_filter(x: np.ndarray, n: int, k: int, pi: float, sqrt2: float):
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
