# -*- coding: utf-8 -*-
import numpy as np
import pandas_ta as ta

from pytest import mark


@mark.parametrize("array,n,result", [
    (np.ones(5), 2, np.array([np.nan, 1.0, 1.0, 1.0, 1.0])),
    (np.ones(5), -2, np.ones(5))
])
def test_np_prenan(array, n, result):
    np.testing.assert_array_equal(ta.np_prenan(array, n), result)


@mark.parametrize("array,n,result", [
    (np.ones(5), 2, np.array([np.nan, np.nan, 1.0, 1.0, 1.0, 1.0, 1.0])),
    (np.ones(5), -2, np.ones(5))
])
def test_np_prepend(array, n, result):
    np.testing.assert_array_equal(ta.np_prepend(array, n), result)


@mark.parametrize("array,n,fn,result", [(np.ones(5), 2, None, np.ones(5))])
def test_np_rolling(array, n, fn, result):
    np.testing.assert_array_equal(ta.np_rolling(array, n, fn), result)


@mark.parametrize("array,n,result", [
    (np.ones(5), 2, np.array([np.nan, np.nan, 1.0, 1.0, 1.0])),
    (np.ones(5), -2, np.array([1.0, 1.0, 1.0, np.nan, np.nan]))
])
def test_np_shift(array, n, result):
    np.testing.assert_array_equal(ta.np_shift(array, n), result)
