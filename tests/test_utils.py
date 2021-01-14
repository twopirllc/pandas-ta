from .config import sample_data
from .context import pandas_ta

from unittest import skip, TestCase
from unittest.mock import patch

import numpy as np
import numpy.testing as npt
from pandas import DataFrame, Series
from pandas.api.types import is_datetime64_ns_dtype, is_datetime64tz_dtype


data = {
    "zero": [0, 0],
    "a": [0, 1],
    "b": [1, 0],
    "c": [1, 1],
    "crossed": [0, 1],
}


class TestUtilities(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = sample_data

    @classmethod
    def tearDownClass(cls):
        del cls.data

    def setUp(self):
        self.crosseddf = DataFrame(data)
        self.utils = pandas_ta.utils

    def tearDown(self):
        del self.crosseddf
        del self.utils

    def test__add_prefix_suffix(self):
        result = self.data.ta.hl2(append=False, prefix="pre")
        self.assertEqual(result.name, "pre_HL2")

        result = self.data.ta.hl2(append=False, suffix="suf")
        self.assertEqual(result.name, "HL2_suf")

        result = self.data.ta.hl2(append=False, prefix="pre", suffix="suf")
        self.assertEqual(result.name, "pre_HL2_suf")

        result = self.data.ta.hl2(append=False, prefix=1, suffix=2)
        self.assertEqual(result.name, "1_HL2_2")

        result = self.data.ta.macd(append=False, prefix="pre", suffix="suf")
        for col in result.columns:
            self.assertTrue(col.startswith("pre_") and col.endswith("_suf"))

    @skip
    def test__above_below(self):
        result = self.utils._above_below(self.crosseddf["a"], self.crosseddf["zero"], above=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "a_A_zero")
        npt.assert_array_equal(result, self.crosseddf["c"])

        result = self.utils._above_below(self.crosseddf["a"], self.crosseddf["zero"], above=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "a_B_zero")
        npt.assert_array_equal(result, self.crosseddf["b"])

        result = self.utils._above_below(self.crosseddf["c"], self.crosseddf["zero"], above=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "c_A_zero")
        npt.assert_array_equal(result, self.crosseddf["c"])

        result = self.utils._above_below(self.crosseddf["c"], self.crosseddf["zero"], above=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "c_B_zero")
        npt.assert_array_equal(result, self.crosseddf["zero"])

    def test_above(self):
        result = self.utils.above(self.crosseddf["a"], self.crosseddf["zero"])
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "a_A_zero")
        npt.assert_array_equal(result, self.crosseddf["c"])

        result = self.utils.above(self.crosseddf["zero"], self.crosseddf["a"])
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "zero_A_a")
        npt.assert_array_equal(result, self.crosseddf["b"])

    def test_above_value(self):
        result = self.utils.above_value(self.crosseddf["a"], 0)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "a_A_0")
        npt.assert_array_equal(result, self.crosseddf["c"])

        result = self.utils.above_value(self.crosseddf["a"], self.crosseddf["zero"])
        self.assertIsNone(result)

    def test_below(self):
        result = self.utils.below(self.crosseddf["zero"], self.crosseddf["a"])
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "zero_B_a")
        npt.assert_array_equal(result, self.crosseddf["c"])

        result = self.utils.below(self.crosseddf["zero"], self.crosseddf["a"])
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "zero_B_a")
        npt.assert_array_equal(result, self.crosseddf["c"])

    def test_below_value(self):
        result = self.utils.below_value(self.crosseddf["a"], 0)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "a_B_0")
        npt.assert_array_equal(result, self.crosseddf["b"])

        result = self.utils.below_value(self.crosseddf["a"], self.crosseddf["zero"])
        self.assertIsNone(result)

    def test_combination(self):
        self.assertIsNotNone(self.utils.combination())

        self.assertEqual(self.utils.combination(), 1)
        self.assertEqual(self.utils.combination(r=-1), 1)

        self.assertEqual(self.utils.combination(n=10, r=4, repetition=False), 210)
        self.assertEqual(self.utils.combination(n=10, r=4, repetition=True), 715)

    def test_cross_above(self):
        result = self.utils.cross(self.crosseddf["a"], self.crosseddf["b"])
        self.assertIsInstance(result, Series)
        npt.assert_array_equal(result, self.crosseddf["crossed"])

        result = self.utils.cross(self.crosseddf["a"], self.crosseddf["b"], above=True)
        self.assertIsInstance(result, Series)
        npt.assert_array_equal(result, self.crosseddf["crossed"])

    def test_cross_below(self):
        result = self.utils.cross(self.crosseddf["b"], self.crosseddf["a"], above=False)
        self.assertIsInstance(result, Series)
        npt.assert_array_equal(result, self.crosseddf["crossed"])

    def test_df_dates(self):
        result = self.utils.df_dates(self.data)
        self.assertEqual(None, result)

        result = self.utils.df_dates(self.data, "1999-11-01")
        self.assertEqual(1, result.shape[0])

        result = self.utils.df_dates(self.data, ["1999-11-01", "2020-08-15", "2020-08-24", "2020-08-25", "2020-08-26", "2020-08-27"])
        self.assertEqual(5, result.shape[0])

    def test_df_month_to_date(self):
        result = self.utils.df_month_to_date(self.data)

    def test_df_quarter_to_date(self):
        result = self.utils.df_quarter_to_date(self.data)

    def test_df_year_to_date(self):
        result = self.utils.df_year_to_date(self.data)

    def test_fibonacci(self):
        self.assertIs(type(self.utils.fibonacci(zero=True, weighted=False)), np.ndarray)

        npt.assert_array_equal(self.utils.fibonacci(zero=True), np.array([0, 1, 1]))
        npt.assert_array_equal(self.utils.fibonacci(zero=False), np.array([1, 1]))

        npt.assert_array_equal(self.utils.fibonacci(n=0, zero=True, weighted=False), np.array([0]))
        npt.assert_array_equal(self.utils.fibonacci(n=0, zero=False, weighted=False), np.array([1]))

        npt.assert_array_equal(self.utils.fibonacci(n=5, zero=True, weighted=False), np.array([0, 1, 1, 2, 3, 5]))
        npt.assert_array_equal(self.utils.fibonacci(n=5, zero=False, weighted=False), np.array([1, 1, 2, 3, 5]))

    def test_fibonacci_weighted(self):
        self.assertIs(type(self.utils.fibonacci(zero=True, weighted=True)), np.ndarray)
        npt.assert_array_equal(self.utils.fibonacci(n=0, zero=True, weighted=True), np.array([0]))
        npt.assert_array_equal(self.utils.fibonacci(n=0, zero=False, weighted=True), np.array([1]))

        npt.assert_allclose(self.utils.fibonacci(n=5, zero=True, weighted=True), np.array([0, 1 / 12, 1 / 12, 1 / 6, 1 / 4, 5 / 12]))
        npt.assert_allclose(self.utils.fibonacci(n=5, zero=False, weighted=True), np.array([1 / 12, 1 / 12, 1 / 6, 1 / 4, 5 / 12]))


    def test_geometric_mean(self):
        returns = pandas_ta.percent_return(self.data.close)
        result = self.utils.geometric_mean(returns)
        self.assertIsInstance(result, float)

        result = self.utils.geometric_mean(Series([12, 14, 11, 8]))
        self.assertIsInstance(result, float)

        result = self.utils.geometric_mean(Series([100, 50, 0, 25, 0, 60]))
        self.assertIsInstance(result, float)

        series = Series([0, 1, 2, 3])
        result = self.utils.geometric_mean(series)
        self.assertIsInstance(result, float)

        result = self.utils.geometric_mean(-series)
        self.assertIsInstance(result, int)
        self.assertAlmostEqual(result, 0)

    def test_get_time(self):
        result = self.utils.get_time(to_string=True)
        self.assertIsInstance(result, str)

        result = self.utils.get_time("NZSX", to_string=True)
        self.assertTrue("NZSX" in result)
        self.assertIsInstance(result, str)

        result = self.utils.get_time("SSE", to_string=True)
        self.assertIsInstance(result, str)
        self.assertTrue("SSE" in result)

    def test_linear_regression(self):
        x = Series([1, 2, 3, 4, 5])
        y = Series([1.8, 2.1, 2.7, 3.2, 4])

        result = self.utils.linear_regression(x, y)
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["a"], float)
        self.assertIsInstance(result["b"], float)
        self.assertIsInstance(result["r"], float)
        self.assertIsInstance(result["t"], float)
        self.assertIsInstance(result["line"], Series)

    def test_log_geometric_mean(self):
        returns = pandas_ta.percent_return(self.data.close)
        result = self.utils.log_geometric_mean(returns)
        self.assertIsInstance(result, float)

        result = self.utils.log_geometric_mean(Series([12, 14, 11, 8]))
        self.assertIsInstance(result, float)

        result = self.utils.log_geometric_mean(Series([100, 50, 0, 25, 0, 60]))
        self.assertIsInstance(result, float)

        series = Series([0, 1, 2, 3])
        result = self.utils.log_geometric_mean(series)
        self.assertIsInstance(result, float)

        result = self.utils.log_geometric_mean(-series)
        self.assertIsInstance(result, int)
        self.assertAlmostEqual(result, 0)

    def test_pascals_triangle(self):
        self.assertIsNone(self.utils.pascals_triangle(inverse=True), None)

        array_1 = np.array([1])
        npt.assert_array_equal(self.utils.pascals_triangle(), array_1)
        npt.assert_array_equal(self.utils.pascals_triangle(weighted=True), array_1)
        npt.assert_array_equal(self.utils.pascals_triangle(weighted=True, inverse=True), np.array([0]))

        array_5 = self.utils.pascals_triangle(n=5)  # or np.array([1, 5, 10, 10, 5, 1])
        array_5w = array_5 / np.sum(array_5)
        array_5iw = 1 - array_5w
        npt.assert_array_equal(self.utils.pascals_triangle(n=-5), array_5)
        npt.assert_array_equal(self.utils.pascals_triangle(n=-5, weighted=True), array_5w)
        npt.assert_array_equal(self.utils.pascals_triangle(n=-5, weighted=True, inverse=True), array_5iw)

        npt.assert_array_equal(self.utils.pascals_triangle(n=5), array_5)
        npt.assert_array_equal(self.utils.pascals_triangle(n=5, weighted=True), array_5w)
        npt.assert_array_equal(self.utils.pascals_triangle(n=5, weighted=True, inverse=True), array_5iw)

    def test_symmetric_triangle(self):
        npt.assert_array_equal(self.utils.symmetric_triangle(), np.array([1,1]))
        npt.assert_array_equal(self.utils.symmetric_triangle(weighted=True), np.array([0.5, 0.5]))

        array_4 = self.utils.symmetric_triangle(n=4)  # or np.array([1, 2, 2, 1])
        array_4w = array_4 / np.sum(array_4)
        npt.assert_array_equal(self.utils.symmetric_triangle(n=4), array_4)
        npt.assert_array_equal(self.utils.symmetric_triangle(n=4, weighted=True), array_4w)

        array_5 = self.utils.symmetric_triangle(n=5)  # or np.array([1, 2, 3, 2, 1])
        array_5w = array_5 / np.sum(array_5)
        npt.assert_array_equal(self.utils.symmetric_triangle(n=5), array_5)
        npt.assert_array_equal(self.utils.symmetric_triangle(n=5, weighted=True), array_5w)

    def test_zero(self):
        self.assertEqual(self.utils.zero(-0.0000000000000001), 0)
        self.assertEqual(self.utils.zero(0), 0)
        self.assertEqual(self.utils.zero(0.0), 0)
        self.assertEqual(self.utils.zero(0.0000000000000001), 0)

        self.assertNotEqual(self.utils.zero(-0.000000000000001), 0)
        self.assertNotEqual(self.utils.zero(0.000000000000001), 0)
        self.assertNotEqual(self.utils.zero(1), 0)

    def test_get_drift(self):
        for s in [0, None, "", [], {}]:
            self.assertIsInstance(self.utils.get_drift(s), int)

        self.assertEqual(self.utils.get_drift(0), 1)
        self.assertEqual(self.utils.get_drift(1.1), 1)
        self.assertEqual(self.utils.get_drift(-1.1), 1)

    def test_get_offset(self):
        for s in [0, None, "", [], {}]:
            self.assertIsInstance(self.utils.get_offset(s), int)

        self.assertEqual(self.utils.get_offset(0), 0)
        self.assertEqual(self.utils.get_offset(-1.1), 0)
        self.assertEqual(self.utils.get_offset(1), 1)

    def test_to_utc(self):
        result = self.utils.to_utc(self.data.copy())
        self.assertTrue(is_datetime64_ns_dtype(result.index))
        self.assertTrue(is_datetime64tz_dtype(result.index))        

    def test_total_time(self):
        result = self.utils.total_time(self.data)
        self.assertEqual(30.182539682539684, result)

        result = self.utils.total_time(self.data, "months")
        self.assertEqual(250.05753361606995, result)

        result = self.utils.total_time(self.data, "weeks")
        self.assertEqual(1086.5714285714287, result)

        result = self.utils.total_time(self.data, "days")
        self.assertEqual(7606, result)

        result = self.utils.total_time(self.data, "hours")
        self.assertEqual(182544, result)

        result = self.utils.total_time(self.data, "minutes")
        self.assertEqual(10952640.0, result)

        result = self.utils.total_time(self.data, "seconds")
        self.assertEqual(657158400.0, result)
