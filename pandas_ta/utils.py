# -*- coding: utf-8 -*-
import math
import sys

from datetime import datetime
from functools import reduce
# from importlib.util import find_spec
from operator import mul
from pathlib import Path
from sys import float_info as sflt
from time import perf_counter

from numpy import argmax, argmin, dot, ones, triu
from numpy import append as npAppend
from numpy import array as npArray
from numpy import ndarray as npNdArray
from numpy import sum as npSum
# from numpy import std as npStd
from numpy import sqrt as npSqrt
from numpy import corrcoef as npCorrcoef
from numpy import seterr
from pandas import DataFrame, Series
from pandas.api.types import is_datetime64_any_dtype

from pandas_ta import Imports, EXCHANGE_TZ, RATE


seterr(divide="ignore", invalid="ignore")


def _above_below(
        series_a: Series,
        series_b: Series,
        above: bool = True,
        asint: bool = True,
        offset: int = None,
        **kwargs
    ):
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
    current.category = "utility"

    return current


def above(
        series_a: Series,
        series_b: Series,
        asint: bool = True,
        offset: int = None,
        **kwargs
    ):
    return _above_below(series_a, series_b, above=True, asint=asint, offset=offset, **kwargs)


def above_value(
        series_a: Series,
        value: float,
        asint: bool = True,
        offset: int = None,
        **kwargs
    ):
    if not isinstance(value, (int, float, complex)):
        print("[X] value is not a number")
        return
    series_b = Series(value, index=series_a.index, name=f"{value}".replace(".","_"))
    return _above_below(series_a, series_b, above=True, asint=asint, offset=offset, **kwargs)    


def below(
        series_a: Series,
        series_b: Series,
        asint: bool =True,
        offset: int =None
        ,**kwargs
    ):
    return _above_below(series_a, series_b, above=False, asint=asint, offset=offset, **kwargs)


def below_value(
        series_a: Series,
        value: float,
        asint: bool = True,
        offset: int = None,
        **kwargs
    ):
    if not isinstance(value, (int, float, complex)):
        print("[X] value is not a number")
        return
    series_b = Series(value, index=series_a.index, name=f"{value}".replace(".","_"))
    return _above_below(series_a, series_b, above=False, asint=asint, offset=offset, **kwargs)


def category_files(category: str) -> list:
    """Helper function to return all filenames in the category directory."""
    files = [x.stem for x in list(Path(f"pandas_ta/{category}/").glob("*.py")) if x.stem != "__init__"]
    return files


def combination(**kwargs):
    """https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python"""
    n = int(math.fabs(kwargs.pop("n", 1)))
    r = int(math.fabs(kwargs.pop("r", 0)))

    if kwargs.pop("repetition", False) or kwargs.pop("multichoose", False):
        n = n + r - 1

    # if r < 0: return None
    r = min(n, n - r)
    if r == 0:
        return 1

    numerator   = reduce(mul, range(n, n - r, -1), 1)
    denominator = reduce(mul, range(1, r + 1), 1)
    return numerator // denominator


def cross_value(
        series_a: Series,
        value: float,
        above: bool = True,
        asint: bool = True,
        offset: int = None,
        **kwargs
    ):
    series_b = Series(value, index=series_a.index, name=f"{value}".replace(".","_"))
    return cross(series_a, series_b, above, asint, offset, **kwargs)


def cross(
        series_a: Series,
        series_b: Series,
        above: bool = True, 
        asint: bool = True,
        offset: int = None,
        **kwargs
    ):
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
    cross.category = "utility"

    return cross


def is_datetime_ordered(df: DataFrame or Series) -> bool:
    """Returns True if the index is a datetime and ordered."""
    index_is_datetime = is_datetime64_any_dtype(df.index)
    try:
        ordered = df.index[0] < df.index[-1]
    except RuntimeWarning: pass
    finally:
        return True if index_is_datetime and ordered else False


def signals(indicator, xa, xb, cross_values, xserie, xserie_a, xserie_b, cross_series, offset) -> DataFrame:
    df = DataFrame()
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


def df_error_analysis(dfA: DataFrame, dfB: DataFrame, **kwargs) -> DataFrame:
    """DataFrame Correlation Analysis helper"""
    corr_method = kwargs.pop("corr_method", "pearson")

    # Find their differences and correlation
    diff = dfA - dfB
    corr = dfA.corr(dfB, method=corr_method)

    # For plotting
    if kwargs.pop("plot", False):
        diff.hist()
        if diff[diff > 0].any():
            diff.plot(kind="kde")

    if kwargs.pop("triangular", False):
        return corr.where(triu(ones(corr.shape)).astype(bool))

    return corr

def fibonacci(n: int = 2, **kwargs) -> npNdArray:
    """Fibonacci Sequence as a numpy array"""
    n = int(math.fabs(n)) if n >= 0 else 2

    zero = kwargs.pop("zero", False)
    if zero:
        a, b = 0, 1
    else:
        n -= 1
        a, b = 1, 1

    result = npArray([a])
    for i in range(0, n):
        a, b = b, a + b
        result = npAppend(result, a)

    weighted = kwargs.pop("weighted", False)
    if weighted:
        fib_sum = npSum(result)
        if fib_sum > 0:
            return result / fib_sum
        else:
            return result
    else:
        return result


def final_time(stime):
    time_diff = perf_counter() - stime
    return f"{time_diff * 1000:2.4f} ms ({time_diff:2.4f} s)"


def get_drift(x: int) -> int:
    """Returns an int if not zero, otherwise defaults to one."""
    return int(x) if isinstance(x, int) and x != 0 else 1


def get_offset(x: int) -> int:
    """Returns an int, otherwise defaults to zero."""
    return int(x) if isinstance(x, int) else 0


def get_time(exchange: str = "NYSE", to_string:bool = False) -> (None, str):
    tz = EXCHANGE_TZ["NYSE"] # Default is NYSE (Eastern Time Zone)
    if isinstance(exchange, str):
        exchange = exchange.upper()
        tz = EXCHANGE_TZ[exchange]

    day_of_year = datetime.utcnow().timetuple().tm_yday
    today = datetime.utcnow()
    s  = f"Today: {today}, "
    s += f"Day {day_of_year}/365 ({100 * round(day_of_year/365, 2)}%), "
    s += f"{exchange} Time: {(today.timetuple().tm_hour + tz) % 12}:{today.timetuple().tm_min}:{today.timetuple().tm_sec}"
    return s if to_string else print(s)


def _linear_regression_np(x: Series, y: Series) -> dict:
    """Simple Linear Regression in Numpy for two 1d arrays for environments
    without the sklearn package."""
    m = x.size
    x_sum = x.sum()
    y_sum = y.sum()

    # 1st row, 2nd col value corr(x, y)
    r = npCorrcoef(x, y)[0,1]

    r_mixture = m * (x * y).sum() - x_sum * y_sum
    b = r_mixture / (m * (x * x).sum() - x_sum * x_sum)
    a = y.mean() - b * x.mean()
    line = a + b * x

    return {
        "a": a, "b": b, "r": r,
        "t": r / npSqrt((1 - r * r) / (m - 2)),
        "line": line
    }

def _linear_regression_sklearn(x, y):
    """Simple Linear Regression in Scikit Learn for two 1d arrays for
    environments with the sklearn package."""
    from sklearn.linear_model import LinearRegression

    regression = LinearRegression().fit(DataFrame(x), y=y)
    r = regression.score(DataFrame(x), y=y)

    a, b = regression.intercept_, regression.coef_[0]

    return {
        "a": a, "b": b, "r": r,
        "t": r / npSqrt((1 - r * r) / (x.size - 2)),
        "line": a + b * x
    }

def linear_regression(x: Series, y: Series) -> dict:
    """Classic Linear Regression in Numpy or Scikit-Learn"""
    x = verify_series(x)
    y = verify_series(y)

    m, n = x.size, y.size
    if m != n:
        print(f"[X] Linear Regression X and y observations do not match: {m} != {n}")
        return

    if Imports["sklearn"]:
        return _linear_regression_sklearn(x, y)
    else:
        return _linear_regression_np(x, y)


def is_percent(x: int or float) -> bool:
    if isinstance(x, (int, float)):
        return x is not None and x >= 0 and x <= 100
    return False


def non_zero_range(high: Series, low: Series) -> Series:
    """Returns the difference of two series and adds epsilon to any zero values.  This occurs commonly in crypto data when 'high' = 'low'.
    """
    diff = high - low
    if diff.eq(0).any().any():
        diff += sflt.epsilon
    return diff


def pascals_triangle(n: int = None, **kwargs) -> npNdArray:
    """Pascal's Triangle

    Returns a numpy array of the nth row of Pascal's Triangle.
    n=4  => triangle: [1, 4, 6, 4, 1]
         => weighted: [0.0625, 0.25, 0.375, 0.25, 0.0625]
         => inverse weighted: [0.9375, 0.75, 0.625, 0.75, 0.9375]
    """
    n = int(math.fabs(n)) if n is not None else 0

    # Calculation
    triangle = npArray([combination(n=n, r=i) for i in range(0, n + 1)])
    triangle_sum = npSum(triangle)
    triangle_weights = triangle / triangle_sum
    inverse_weights = 1 - triangle_weights

    weighted = kwargs.pop("weighted", False)
    inverse = kwargs.pop("inverse", False)
    if weighted and inverse:
        return inverse_weights
    if weighted:
        return triangle_weights
    if inverse:
        return None

    return triangle


def recent_maximum_index(x):
    return int(argmax(x[::-1]))


def recent_minimum_index(x):
    return int(argmin(x[::-1]))


def signed_series(series: Series, initial: int = None) -> Series:
    """Returns a Signed Series with or without an initial value
    
    Default Example:
    series = Series([3, 2, 2, 1, 1, 5, 6, 6, 7, 5])
    and returns:
    sign = Series([NaN, -1.0, 0.0, -1.0, 0.0, 1.0, 1.0, 0.0, 1.0, -1.0])
    """
    series = verify_series(series)
    sign = series.diff(1)
    sign[sign > 0] = 1
    sign[sign < 0] = -1
    sign.iloc[0] = initial
    return sign


def symmetric_triangle(n: int = None, **kwargs) -> list:
    """Symmetric Triangle with n >= 2

    Returns a numpy array of the nth row of Symmetric Triangle.
    n=4  => triangle: [1, 2, 2, 1]
         => weighted: [0.16666667 0.33333333 0.33333333 0.16666667]
    """
    n = int(math.fabs(n)) if n is not None else 2

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

    if kwargs.pop("weighted", False):
        triangle_sum = npSum(triangle)
        triangle_weights = triangle / triangle_sum
        return triangle_weights

    return triangle


def unsigned_differences(series: Series, amount: int = None, **kwargs) -> Series:
    """Unsigned Differences
    Returns two Series, an unsigned positive and unsigned negative series based
    on the differences of the original series. The positive series are only the
    increases and the negative series is only the decreases.

    Default Example:
    series   = Series([3, 2, 2, 1, 1, 5, 6, 6, 7, 5, 3]) and returns
    postive  = Series([0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0])
    negative = Series([0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1])
    """
    amount = int(amount) if amount is not None else 1
    negative = series.diff(amount)
    negative.fillna(0, inplace=True)
    positive = negative.copy()

    positive[positive <= 0] = 0
    positive[positive > 0] = 1

    negative[negative >= 0] = 0
    negative[negative < 0] = 1

    if kwargs.pop("asint", False):
        positive = positive.astype(int)
        negative = negative.astype(int)

    return positive, negative


def verify_series(series: Series) -> Series:
    """If a Pandas Series return it."""
    if series is not None and isinstance(series, Series):
        return series


def weights(w):
    def _dot(x):
        return dot(w, x)
    return _dot


def zero(x: [int, float]) -> [int, float]:
    """If the value is close to zero, then return zero.
    Otherwise return the value."""
    return 0 if abs(x) < sflt.epsilon else x

# Candle Functions

def candle_color(open_, close):
    color = close.copy().astype(int)
    color[close >= open_] = 1
    color[close < open_] = -1
    return color

def real_body(close, open_):
    return non_zero_range(close, open_)

def high_low_range(high, low):
    return non_zero_range(high, low)
