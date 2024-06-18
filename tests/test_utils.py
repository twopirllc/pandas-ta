# -*- coding: utf-8 -*-
import numpy as np
import pandas_ta as ta

from sys import platform as sys_platform
from pandas import DataFrame, Series
from pandas.api.types import is_datetime64_ns_dtype
from pytest import mark, param


CROSS_E1 = {
    "zero": [0, 0],
    "a": [0, 1],
    "b": [1, 0],
    "c": [1, 1],
    "crossed": [0, 1],
}
crosseddf = DataFrame(CROSS_E1)


def test_above():
    result = ta.utils.above(crosseddf["a"], crosseddf["zero"])
    assert isinstance(result, Series)
    assert result.name == "a_A_zero"
    np.testing.assert_array_equal(result, crosseddf["c"])

    result = ta.utils.above(crosseddf["zero"], crosseddf["a"])
    assert isinstance(result, Series)
    assert result.name == "zero_A_a"
    np.testing.assert_array_equal(result, crosseddf["b"])


def test_above_value():
    result = ta.utils.above_value(crosseddf["a"], 0)
    assert isinstance(result, Series)
    assert result.name == "a_A_0"
    np.testing.assert_array_equal(result, crosseddf["c"])

    result = ta.utils.above_value(crosseddf["a"], crosseddf["zero"])
    assert result is None


def test_add_df_prefix(df):
    result = df.ta.hl2(prefix="pre")
    assert result.name == "pre_HL2"

    result = df.ta.hl2(suffix="suf")
    assert result.name == "HL2_suf"

    result = df.ta.hl2(prefix="pre", suffix="suf")
    assert result.name == "pre_HL2_suf"

    result = df.ta.hl2(prefix=1, suffix=2)
    assert result.name == "1_HL2_2"

    result = df.ta.macd(prefix="pre", suffix="suf")
    for col in result.columns:
        assert col.startswith("pre_") and col.endswith("_suf")


def test_below():
    result = ta.utils.below(crosseddf["zero"], crosseddf["a"])
    assert isinstance(result, Series)
    assert result.name == "zero_B_a"
    np.testing.assert_array_equal(result, crosseddf["c"])

    result = ta.utils.below(crosseddf["zero"], crosseddf["a"])
    assert isinstance(result, Series)
    assert result.name == "zero_B_a"
    np.testing.assert_array_equal(result, crosseddf["c"])


def test_below_value():
    result = ta.utils.below_value(crosseddf["a"], 0)
    assert isinstance(result, Series)
    assert result.name == "a_B_0"
    np.testing.assert_array_equal(result, crosseddf["b"])

    result = ta.utils.below_value(crosseddf["a"], crosseddf["zero"])
    assert result is None


def test_combination():
    assert ta.utils.combination() != None

    assert ta.utils.combination() == 1
    assert ta.utils.combination(r=-1) == 1

    assert ta.utils.combination(n=10, r=4, repetition=False) == 210
    assert ta.utils.combination(n=10, r=4, repetition=True) == 715


def test_cross_above():
    result = ta.utils.cross(crosseddf["a"], crosseddf["b"])
    assert isinstance(result, Series)
    np.testing.assert_array_equal(result, crosseddf["crossed"])

    result = ta.utils.cross(crosseddf["a"], crosseddf["b"], above=True)
    assert isinstance(result, Series)
    np.testing.assert_array_equal(result, crosseddf["crossed"])

    result = ta.utils.cross(crosseddf["a"], crosseddf["b"], equal=False)
    assert isinstance(result, Series)
    np.testing.assert_array_equal(result, crosseddf["crossed"])


def test_cross_below():
    result = ta.utils.cross(crosseddf["b"], crosseddf["a"], above=False)
    assert isinstance(result, Series)
    np.testing.assert_array_equal(result, crosseddf["crossed"])

    result = ta.utils.cross(crosseddf["b"], crosseddf["a"], above=False, equal=False)
    assert isinstance(result, Series)
    np.testing.assert_array_equal(result, crosseddf["crossed"])

    # result = ta.utils.cross(crosseddf["a"], crosseddf["b"], above=False)
    # assert result[0] == 0


def test_datetime_ordered(df):
    # Test if datetime64 index and ordered
    result = df.ta.datetime_ordered()
    assert result is True

    # Test if not ordered
    original = df.copy()
    reversal = original.ta.reverse()
    result = reversal.ta.datetime_ordered()
    assert result is False

    # Test a non-datetime64 index
    original = df.copy()
    original.reset_index(inplace=True)
    result = original.ta.datetime_ordered()
    assert result is False


def test_reverse(df):
    original = df.copy()
    result = original.ta.reverse()

    # Check if first and last time are reversed
    assert result.index[-1] == original.index[0]
    assert  result.index[0] == original.index[-1]


def test_df_dates(df):
    result = ta.utils.df_dates(df)
    assert result is None


def test_fibonacci():
    np.testing.assert_array_equal(ta.utils.fibonacci(0, False), np.array([1, 1]))
    np.testing.assert_array_equal(ta.utils.fibonacci(5, False), np.array([1, 1, 2, 3, 5]))

    assert isinstance(ta.utils.fibonacci(2, False), np.ndarray)


def test_fibonacci_weighted():
    np.testing.assert_array_equal(ta.utils.fibonacci(0, True), np.array([0.5, 0.5]))
    np.testing.assert_allclose(ta.utils.fibonacci(5, True), np.array([1 / 12, 1 / 12, 1 / 6, 1 / 4, 5 / 12]))

    assert isinstance(ta.utils.fibonacci(2, True), np.ndarray)


def test_geometric_mean(df):
    returns = ta.percent_return(df.close)
    result = ta.utils.geometric_mean(returns)
    assert isinstance(result, (float, int))

    result = ta.utils.geometric_mean(Series([12, 14, 11, 8]))
    assert isinstance(result, float)

    result = ta.utils.geometric_mean(Series([100, 50, 0, 25, 0, 60]))
    assert isinstance(result, float)

    series = Series([0, 1, 2, 3])
    result = ta.utils.geometric_mean(series)
    assert isinstance(result, float)

    result = ta.utils.geometric_mean(-series)
    assert isinstance(result, int)
    assert result == 0


def test_linear_regression():
    x = Series([1, 2, 3, 4, 5])
    y = Series([1.8, 2.1, 2.7, 3.2, 4])

    result = ta.utils.linear_regression(x, y)
    assert isinstance(result, dict)
    assert isinstance(result["a"], float)
    assert isinstance(result["b"], float)
    assert isinstance(result["r"], float)
    assert isinstance(result["t"], float)
    assert isinstance(result["line"], Series)


def test_log_geometric_mean(df):
    returns = ta.percent_return(df.close)
    result = ta.utils.log_geometric_mean(returns)
    assert isinstance(result, float)

    result = ta.utils.log_geometric_mean(Series([12, 14, 11, 8]))
    assert isinstance(result, float)

    result = ta.utils.log_geometric_mean(Series([100, 50, 0, 25, 0, 60]))
    assert isinstance(result, float)

    series = Series([0, 1, 2, 3])
    result = ta.utils.log_geometric_mean(series)
    assert isinstance(result, float)

    result = ta.utils.log_geometric_mean(-series)
    assert isinstance(result, int)
    assert result == 0


def test_pascals_triangle():
    assert ta.utils.pascals_triangle(inverse=True) is None

    array = np.array([1])
    np.testing.assert_array_equal(ta.utils.pascals_triangle(), array)
    np.testing.assert_array_equal(ta.utils.pascals_triangle(weighted=True), array)
    np.testing.assert_array_equal(ta.utils.pascals_triangle(weighted=True, inverse=True), np.array([0]))

@mark.parametrize("value", [-5, -1, 0, 1, 5])
def test_pascals_triangle_n(value):
    array = ta.utils.pascals_triangle(n=value)
    array_w = array / np.sum(array)
    array_iw = 1 - array_w
    np.testing.assert_array_equal(ta.utils.pascals_triangle(n=value), array)
    np.testing.assert_array_equal(ta.utils.pascals_triangle(n=value, weighted=True), array_w)
    np.testing.assert_array_equal(ta.utils.pascals_triangle(n=value, weighted=True, inverse=True), array_iw)


@mark.parametrize("value", [param(None, marks=mark.xfail), "NYSE", "NZSX", "SSE"])
def test_get_time_(value):
    print(f"{value=}")
    result = ta.utils.get_time(value, to_string=True)
    assert isinstance(result, str)
    assert value in result


@mark.parametrize("array,degree,result", [
    ([1], 1, 1), ([1, 1], 1, 2), ([1, 0, -1], 1, 0),
    ([1, 0, 1], 1, 2), ([1, 1, 1], 1, 3)
])
def test_hpoly(array, degree, result):
    assert ta.utils.hpoly(array, degree) == result


@mark.parametrize("value,result", [(-0.01, np.nan), (1.01, np.nan)])
def test_inv_norm_isnan(value, result):
    np.testing.assert_equal(ta.utils.inv_norm(value), result)


@mark.skipif(
    not sys_platform.startswith("darwin"),
    reason="Passes on Mac... yet fails on Ubuntu 3.9 (Github Action)"
)
@mark.parametrize("value,result", [
    (0, -np.inf), (1 - 0.96, -1.7506860712521692),
#    (1 - 0.8646, -1.101222112591979), # FAILs with Python 3.11.7 on Mac
    param(1 - 0.8646, -1.101222112591979, marks=mark.xfail),
    (0.5, 0),
#    (0.8646, 1.101222112591979), # FAILs with Python 3.11.7 on Mac
    param(0.8646, 1.101222112591979, marks=mark.xfail),
    (0.96, 1.7506860712521692), (1, np.inf)
])
def test_inv_norm_value(value, result):
    assert ta.utils.inv_norm(value) == result


def test_symmetric_triangle():
    np.testing.assert_array_equal(ta.utils.symmetric_triangle(), np.array([1,1]))
    np.testing.assert_array_equal(ta.utils.symmetric_triangle(weighted=True), np.array([0.5, 0.5]))


@mark.parametrize("value", [2, 3, 10])
def test_symmetric_triangle_n(value):
    array = ta.utils.symmetric_triangle(n=value)
    array_w = array / np.sum(array)
    np.testing.assert_array_equal(ta.utils.symmetric_triangle(n=value), array)
    np.testing.assert_array_equal(ta.utils.symmetric_triangle(n=value, weighted=True), array_w)


@mark.parametrize("value,result", [
    ("sma", 0), ("Sma", 0), ("ema", 1), ("wma", 2), ("dema", 3), ("tema", 4),
    ("trima", 5), ("kama", 6), ("mama", 7), ("t3", 8)
])
def test_tal_ma(value, result):
    assert ta.utils.tal_ma(value) == result


def test_to_utc(df):
    result = ta.utils.to_utc(df)
    assert is_datetime64_ns_dtype(result.index)
    # assert is_datetime64tz_dtype(result.index) # Depreciation Warning but no mention in 2.2 docs



def test_version():
    assert isinstance(ta.version, str)
    print(f"{ta.version=}")


def test_v_drift_type():
    _instances = [0, None, "", [], {}, np.int8(5), np.int16(5), np.int32(5), np.int64(5)]
    for _ in _instances:
        assert isinstance(ta.utils.v_drift(_), int)


@mark.parametrize("value,result", [
    (-1.1, 1), (0, 1), (1.1, 1), (5, 5),
    (np.int64(-1.1), -1), (np.int64(0), 1),
    (np.int64(1.1), 1), (np.int64(5), 5)
])
def test_v_drift_value(value, result):
    assert ta.utils.v_drift(value) == result


@mark.parametrize("value", [None, "", [], {}, -1.1, -1, 0.0, 0, 0.1, 1.0, 1])
@mark.parametrize("strict", [False, True])
def test_v_lowerbound_type(value, strict):
    assert isinstance(ta.v_lowerbound(value, strict=strict), (float, int))


@mark.parametrize("value,result", [
    (-1.1, 0), (-1, 0), (0.0, 0), (0, 0), (0.1, 0.1), (1.0, 1.0), (1, 1),
])
def test_v_lowerbound_value_strict(value, result):
    assert ta.utils.v_lowerbound(value) == result


@mark.parametrize("value,result", [
    (-1.1, 0), (-1, 0), (0.0, 0), (0, 0), (0.1, 0.1), (1.0, 1), (1, 1),
])
def test_v_lowerbound_value_strict_false(value, result):
    assert ta.utils.v_lowerbound(value, strict=False) == result


@mark.parametrize("value", [
    0, None, "", [], {}, np.int8(5), np.int16(5), np.int32(5), np.int64(5)
])
def test_v_offset_types(value):
    assert isinstance(ta.utils.v_offset(value), int)


@mark.parametrize("value,result", [
    (None, 0), (-1.1, 0), (-1, -1), (0, 0), (1.1, 0), (1, 1), (2, 2),
    (np.int64(-1), -1), (np.int64(0), 0), (np.int64(1.1), 1),
    (np.int64(1), 1), (np.int64(2), 2), (np.int64(-1.1), -1),
    (np.int64(1.1), 1),
])
def test_v_offset_value(value,result):
    assert ta.utils.v_offset(value) == result


@mark.parametrize("value", [None, "", [], {}, -1.1, -1, 0.0, 0, 0.1, 1.0, 1])
@mark.parametrize("strict", [False, True])
def test_v_upperbound_value_strict(value, strict):
    assert isinstance(ta.utils.v_upperbound(value, strict=strict), (float, int))


@mark.parametrize("value,result", [
    (-0.0000000000000001, 0), (0.0000000000000001, 0), (0, 0), (0.0, 0),
    param(-0.000000000000001, 0, marks=mark.xfail), param(1, 0, marks=mark.xfail)
])
def test_zero(value, result):
    assert ta.utils.zero(value) == result


@mark.parametrize("talib", [False, True])
@mark.parametrize("verbose", [False, True])
def test_indicator_speed_talib_verbose(df, talib, verbose):
    resultdf = ta.speed_test(df, talib=talib, verbose=verbose)
    assert isinstance(resultdf, DataFrame)
