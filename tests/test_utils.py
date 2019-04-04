from .context import pandas_ta

from unittest import TestCase
from unittest.mock import patch

import numpy as np
import numpy.testing as npt
from pandas import DataFrame


class TestUtilities(TestCase):
    def setUp(self):
        self.utils = pandas_ta.utils

    def tearDown(self):
        del self.utils


    def test_combination(self):
        self.assertIsNotNone(self.utils.combination())

        self.assertEqual(self.utils.combination(), 1)
        self.assertEqual(self.utils.combination(r=-1), 1)

        self.assertEqual(self.utils.combination(n=10, r=4, repetition=False), 210)
        self.assertEqual(self.utils.combination(n=10, r=4, repetition=True), 715)

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