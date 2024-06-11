# -*- coding: utf-8 -*-
from functools import reduce
from math import floor as mfloor
from operator import mul
from sys import float_info as sflt

from numpy import (
    all, append, array, corrcoef, dot, exp, fabs, float64,
    log, nan, ndarray, ones, seterr, sign, sqrt, sum, triu,
    zeros
)
from pandas import DataFrame, Series
from numba import njit
from pandas_ta._typing import (
    Array,
    DictLike,
    Float,
    Int,
    IntFloat,
    List,
    Optional
)
from pandas_ta.maps import Imports
from pandas_ta.utils._validate import v_series

__all__ = [
    "combination",
    "df_error_analysis",
    "erf",
    "fibonacci",
    "geometric_mean",
    "hpoly",
    "linear_regression",
    "log_geometric_mean",
    "pascals_triangle",
    "strided_window",
    "symmetric_triangle",
    "weights",
    "zero",
]



def combination(
    n: Int = 1, r: Int = 0,
    repetition: bool = False, multichoose: bool = False
) -> Int:
    """https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python"""
    n, r = int(fabs(n)), int(fabs(r))

    if repetition or multichoose:
        n = n + r - 1

    # if r < 0: return None
    r = min(n, n - r)
    if r == 0:
        return 1

    numerator = reduce(mul, range(n, n - r, -1), 1)
    denominator = reduce(mul, range(1, r + 1), 1)
    return numerator // denominator

def erf(x: IntFloat) -> Float:
    """Error Function erf(x)
    The algorithm comes from Handbook of Mathematical Functions, formula 7.1.26.
    Source: https://stackoverflow.com/questions/457408/is-there-an-easily-available-implementation-of-erf-for-python
    """
    x_sign = sign(x)
    x = abs(x)

    # constants
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911

    # A&S formula 7.1.26
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2)
               * t + a1) * t * exp(-x * x)
    return x_sign * y  # erf(-x) = -erf(x)


@njit(cache=True)
def fibonacci(n, weighted):
    n = n if n > 1 else 2
    sqrt5 = sqrt(5.0)
    phi, psi = 0.5 * (1.0 + sqrt5), 0.5 * (1.0 - sqrt5)

    result = zeros(n)
    for i in range(0, n):
        result[i] = float(phi ** (i + 1) - psi ** (i + 1)) / sqrt5

    if weighted:
        return result / result.sum()
    return result


def geometric_mean(series: Series) -> Float:
    """Returns the Geometric Mean for a Series of positive values."""
    n = series.size
    if n < 1:
        return series.iloc[0]

    has_zeros = 0 in series.to_numpy()
    if has_zeros:
        series = series.fillna(0) + 1
    if all(series > 0):
        mean = series.prod() ** (1 / n)
        return mean if not has_zeros else mean - 1
    return 0


def hpoly(x: Array, v: IntFloat) -> Float:
    """Horner's Calculation for Polynomial Evaluation (hpoly)

    array: np.array of polynomial coefficients
        * Convert list or Series to np.array prior to calling the method for
        best performance
    v: value to evaluate

    Example:
    coeffs_0 = [4, -3, 0, 1] # 4x^3 - 3x^2 + 0x + 1
    coeffs_1 = np.array(coeffs_0) # Faster
    coeffs_2 = pd.Series(coeffs_0).values
    x = -6.5

    hpoly(coeffs_0, x) => -1224.25
    hpoly(coeffs_1, x) or hpoly(coeffs_2, x) => -1224.25 # Faster
    """
    if not isinstance(x, ndarray):
        x = array(x)

    m, y = x.size, x[0]

    for i in range(1, m):
        y = x[i] + v * y
    return y


def linear_regression(x: Series, y: Series) -> DictLike:
    """Classic Linear Regression in Numpy or Scikit-Learn"""
    x, y = v_series(x), v_series(y)
    m, n = x.size, y.size

    if m != n:
        print(f"[X] X and y have unequal sizes: {m} != {n}")
        return {}

    if Imports["sklearn"]:
        return _linear_regression_sklearn(x, y)
    else:
        return _linear_regression_np(x, y)


def log_geometric_mean(series: Series) -> Float:
    """Returns the Logarithmic Geometric Mean"""
    n = series.size
    if n > 1:
        series = series.fillna(0) + 1
        if all(series > 0):
            return exp(log(series).sum() / n) - 1
    return 0


def pascals_triangle(
    n: Int = None, inverse: bool = False, weighted: bool = False
) -> Array:
    """Pascal's Triangle

    Returns a numpy array of the nth row of Pascal's Triangle.
    n=4  => triangle: [1, 4, 6, 4, 1]
         => weighted: [0.0625, 0.25, 0.375, 0.25, 0.0625]
         => inverse weighted: [0.9375, 0.75, 0.625, 0.75, 0.9375]
    """
    n = int(fabs(n)) if n is not None else 0

    # Calculation
    triangle = array([combination(n=n, r=i) for i in range(0, n + 1)])
    triangle_sum = sum(triangle)
    triangle_weights = triangle / triangle_sum
    inverse_weights = 1 - triangle_weights

    if weighted and inverse:
        return inverse_weights
    if weighted:
        return triangle_weights
    if inverse:
        return None

    return triangle


def strided_window(x: Array, length: Int) -> Array:
    """as_strided
    creates a view into the array given the exact strides and shape.
    * Recommended to avoid when possible.

    Source: https://numpy.org/devdocs/reference/generated/numpy.lib.stride_tricks.as_strided.html
    Pandas TA Issue: https://github.com/twopirllc/pandas-ta/issues/285
    """
    from numpy.lib.stride_tricks import as_strided
    strides = x.strides + (x.strides[-1],)
    shape = x.shape[:-1] + (x.shape[-1] - length + 1, length)
    return as_strided(x, shape=shape, strides=strides, writeable=False)


def symmetric_triangle(
    n: Int = None, weighted: bool = False
) -> Optional[List[int]]:
    """Symmetric Triangle whenever n >= 2

    Returns a numpy array of the nth row of Symmetric Triangle.
    n=4  => triangle: [1, 2, 2, 1]
         => weighted: [0.16666667 0.33333333 0.33333333 0.16666667]
    """
    n = int(fabs(n)) if n is not None else 2

    triangle = None
    if n == 2:
        triangle = [1, 1]

    if n > 2:
        if n % 2 == 0:
            front = [i + 1 for i in range(0, mfloor(n / 2))]
            triangle = front + front[::-1]
        else:
            front = [i + 1 for i in range(0, mfloor(0.5 * (n + 1)))]
            triangle = front.copy()
            front.pop()
            triangle += front[::-1]

    if weighted and isinstance(triangle, list):
        return triangle / sum(triangle)

    return triangle


def weights(w: Array):
    """Calculates the dot product of weights with values x"""
    def _dot(x):
        return dot(w, x)
    return _dot


def zero(x: IntFloat) -> IntFloat:
    """If the value is close to zero, then return zero.
    Otherwise return itself."""
    return 0 if abs(x) < sflt.epsilon else x


# TESTING


def df_error_analysis(
    A: DataFrame, B: DataFrame,
    plot: bool = False, triangular: bool = False,
    method: str = "pearson",
) -> DataFrame:
    """DataFrame Correlation Analysis helper"""
    _r_method = ["pearson", "kendall", "spearman"]
    corr_method = method if method in _r_method else _r_method[0]

    # Find their differences and correlation
    diff = A - B
    result = A.corr(B, method=corr_method)

    # For plotting
    if plot:
        diff.hist()
        if diff[diff > 0].any():
            diff.plot(kind="kde")

    if triangular:
        return result.where(triu(ones(result.shape)).astype(bool))

    return result


# PRIVATE
def _linear_regression_np(x: Series, y: Series) -> DictLike:
    """Simple Linear Regression in Numpy
    for two 1d arrays for environments without the sklearn package."""
    result = {"a": nan, "b": nan, "r": nan, "t": nan, "line": nan}
    x_sum = x.sum()
    y_sum = y.sum()

    if int(x_sum) != 0:
        # 1st row, 2nd col value corr(x, y)
        r = corrcoef(x, y)[0, 1]

        m = x.size
        r_mix = m * (x * y).sum() - x_sum * y_sum
        b = r_mix // (m * (x * x).sum() - x_sum * x_sum)
        a = y.mean() - b * x.mean()
        line = a + b * x

        _np_err = seterr()
        seterr(divide="ignore", invalid="ignore")
        result = {
            "a": a, "b": b, "r": r,
            "t": r / sqrt((1 - r * r) / (m - 2)),
            "line": line,
        }
        seterr(divide=_np_err["divide"], invalid=_np_err["invalid"])

    return result


def _linear_regression_sklearn(x: Series, y: Series) -> DictLike:
    """Simple Linear Regression in Scikit Learn for two 1d arrays for
    environments with the sklearn package."""
    from sklearn.linear_model import LinearRegression

    X = DataFrame(x)
    lr = LinearRegression().fit(X, y=y)
    r = lr.score(X, y=y)
    a, b = lr.intercept_, lr.coef_[0]

    result = {
        "a": a, "b": b, "r": r,
        "t": r / sqrt((1 - r * r) / (x.size - 2)),
        "line": a + b * x
    }
    return result
