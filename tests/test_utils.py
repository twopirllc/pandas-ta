from .config import sample_data
from .context import pandas_ta

from unittest import TestCase
from unittest.mock import patch

import numpy as np
import numpy.testing as npt
from pandas import DataFrame, Series

data = {
    'zero': [0, 0],
    'a': [0, 1],
    'b': [1, 0],
    'c': [1, 1],
    'crossed': [0, 1],
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
        self.assertEqual(result.name, 'pre_HL2')

        result = self.data.ta.hl2(append=False, suffix="suf")
        self.assertEqual(result.name, 'HL2_suf')

        result = self.data.ta.hl2(append=False, prefix="pre", suffix="suf")
        self.assertEqual(result.name, 'pre_HL2_suf')

        result = self.data.ta.hl2(append=False, prefix=1, suffix=2)
        self.assertEqual(result.name, '1_HL2_2')

        result = self.data.ta.macd(append=False, prefix="pre", suffix="suf")
        for col in result.columns:
            self.assertTrue(col.startswith('pre_') and col.endswith('_suf'))

    def test__above_below(self):
        result = self.utils._above_below(self.crosseddf['a'], self.crosseddf['zero'], above=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'a_A_zero')
        npt.assert_array_equal(result, self.crosseddf['c'])

        result = self.utils._above_below(self.crosseddf['a'], self.crosseddf['zero'], above=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'a_B_zero')
        npt.assert_array_equal(result, self.crosseddf['b'])

        result = self.utils._above_below(self.crosseddf['c'], self.crosseddf['zero'], above=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'c_A_zero')
        npt.assert_array_equal(result, self.crosseddf['c'])

        result = self.utils._above_below(self.crosseddf['c'], self.crosseddf['zero'], above=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'c_B_zero')
        npt.assert_array_equal(result, self.crosseddf['zero'])

    def test_above(self):
        result = self.utils.above(self.crosseddf['a'], self.crosseddf['zero'])
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'a_A_zero')
        npt.assert_array_equal(result, self.crosseddf['c'])

        result = self.utils.above(self.crosseddf['zero'], self.crosseddf['a'])
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'zero_A_a')
        npt.assert_array_equal(result, self.crosseddf['b'])

    def test_above_value(self):
        result = self.utils.above_value(self.crosseddf['a'], 0)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'a_A_0')
        npt.assert_array_equal(result, self.crosseddf['c'])

        result = self.utils.above_value(self.crosseddf['a'], self.crosseddf['zero'])
        self.assertIsNone(result)

    def test_below(self):
        result = self.utils.below(self.crosseddf['zero'], self.crosseddf['a'])
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'zero_B_a')
        npt.assert_array_equal(result, self.crosseddf['c'])

        result = self.utils.below(self.crosseddf['zero'], self.crosseddf['a'])
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'zero_B_a')
        npt.assert_array_equal(result, self.crosseddf['c'])

    def test_below_value(self):
        result = self.utils.below_value(self.crosseddf['a'], 0)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'a_B_0')
        npt.assert_array_equal(result, self.crosseddf['b'])

        result = self.utils.below_value(self.crosseddf['a'], self.crosseddf['zero'])
        self.assertIsNone(result)

    def test_combination(self):
        self.assertIsNotNone(self.utils.combination())

        self.assertEqual(self.utils.combination(), 1)
        self.assertEqual(self.utils.combination(r=-1), 1)

        self.assertEqual(self.utils.combination(n=10, r=4, repetition=False), 210)
        self.assertEqual(self.utils.combination(n=10, r=4, repetition=True), 715)
    
    def test_cross_above(self):
        result = self.utils.cross(self.crosseddf['a'], self.crosseddf['b'])
        self.assertIsInstance(result, Series)
        npt.assert_array_equal(result, self.crosseddf['crossed'])

        result = self.utils.cross(self.crosseddf['a'], self.crosseddf['b'], above=True)
        self.assertIsInstance(result, Series)
        npt.assert_array_equal(result, self.crosseddf['crossed'])

    def test_cross_below(self):
        result = self.utils.cross(self.crosseddf['b'], self.crosseddf['a'], above=False)
        self.assertIsInstance(result, Series)
        npt.assert_array_equal(result, self.crosseddf['crossed'])

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

        npt.assert_allclose(self.utils.fibonacci(n=5, zero=True, weighted=True), np.array([0, 1/12, 1/12, 1/6, 1/4, 5/12]))
        npt.assert_allclose(self.utils.fibonacci(n=5, zero=False, weighted=True), np.array([1/12, 1/12, 1/6, 1/4, 5/12]))

    def test_pascals_triangle(self):
        self.assertIsNone(self.utils.pascals_triangle(inverse=True), None)

        array_1 = np.array([1])
        npt.assert_array_equal(self.utils.pascals_triangle(), array_1)
        npt.assert_array_equal(self.utils.pascals_triangle(weighted=True), array_1)
        npt.assert_array_equal(self.utils.pascals_triangle(weighted=True, inverse=True), np.array([0]))

        array_5 = self.utils.pascals_triangle(n=5) #or np.array([1, 5, 10, 10, 5, 1])
        array_5w = array_5 / np.sum(array_5)
        array_5iw = 1 - array_5w
        npt.assert_array_equal(self.utils.pascals_triangle(n=-5), array_5)
        npt.assert_array_equal(self.utils.pascals_triangle(n=-5, weighted=True), array_5w)
        npt.assert_array_equal(self.utils.pascals_triangle(n=-5, weighted=True, inverse=True), array_5iw)

        npt.assert_array_equal(self.utils.pascals_triangle(n=5), array_5)
        npt.assert_array_equal(self.utils.pascals_triangle(n=5, weighted=True), array_5w)
        npt.assert_array_equal(self.utils.pascals_triangle(n=5, weighted=True, inverse=True), array_5iw)

    def test_symmetric_triangle(self):
        npt.assert_array_equal(self.utils.symmetric_triangle(), np.array([1, 1]))
        npt.assert_array_equal(self.utils.symmetric_triangle(weighted=True), np.array([0.5, 0.5]))

        array_4 = self.utils.symmetric_triangle(n=4) #or np.array([1, 2, 2, 1])
        array_4w = array_4 / np.sum(array_4)
        npt.assert_array_equal(self.utils.symmetric_triangle(n=4), array_4)
        npt.assert_array_equal(self.utils.symmetric_triangle(n=4, weighted=True), array_4w)

        array_5 = self.utils.symmetric_triangle(n=5) #or np.array([1, 2, 3, 2, 1])
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
        for s in [0, None, '', [], {}]:
            self.assertIsInstance(self.utils.get_drift(s), int)

        self.assertEqual(self.utils.get_drift(0), 1)
        self.assertEqual(self.utils.get_drift(1.1), 1)
        self.assertEqual(self.utils.get_drift(-1.1), -1)
        self.assertEqual(self.utils.get_drift(1.999999999999999), 1)
        self.assertEqual(self.utils.get_drift(1.9999999999999999), 2)
        self.assertEqual(self.utils.get_drift(-10), -10)

    def test_get_offset(self):
        for s in [0, None, '', [], {}]:
            self.assertIsInstance(self.utils.get_offset(s), int)

        self.assertEqual(self.utils.get_offset(0), 0)
        self.assertEqual(self.utils.get_offset(1.1), 1)
        self.assertEqual(self.utils.get_offset(-1.1), -1)
        self.assertEqual(self.utils.get_offset(1.999999999999999), 1)
        self.assertEqual(self.utils.get_offset(1.9999999999999999), 2)