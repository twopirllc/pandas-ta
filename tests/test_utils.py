from pandas_ta import utils as utils

from unittest import TestCase
from unittest.mock import patch

import numpy as np
import numpy.testing as npt
from pandas import DataFrame

class TestUtilities(TestCase):
    def setUp(self):
        self.utils = utils

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
        self.assertIs(type(self.utils.pascals_triangle(weighted=False)), np.ndarray)
        npt.assert_array_equal(self.utils.pascals_triangle(weighted=False), np.array([1]))
        npt.assert_array_equal(self.utils.pascals_triangle(n=3, weighted=False), np.array([1, 3, 3, 1]))


    def test_pascals_triangle_all(self):
        all_ = self.utils.pascals_triangle(all=True)
        self.assertIs(type(all_), tuple)
        self.assertEqual(len(all_), 7)

        self.assertEqual(all_[1], 1)
        self.assertEqual(all_[2], 1.0)
        self.assertEqual(all_[6], 1.0)

        self.assertIs(type(all_[0]), np.ndarray)
        npt.assert_array_equal(all_[0], np.array([1]))

        self.assertIs(type(all_[3]), np.ndarray)
        npt.assert_array_equal(all_[3], np.array([0]))

        self.assertIs(type(all_[4]), np.ndarray)
        npt.assert_array_equal(all_[4], np.array([1.]))

        self.assertIs(type(all_[5]), np.ndarray)
        npt.assert_array_equal(all_[5], np.array([0.]))


    def test_pascals_triangle_weighted(self):
        self.assertIs(type(self.utils.pascals_triangle(weighted=True)), np.ndarray)
        npt.assert_array_equal(self.utils.pascals_triangle(weighted=True), np.array([1]))
        npt.assert_array_equal(self.utils.pascals_triangle(n=3, weighted=True), np.array([1/8, 3/8, 3/8, 1/8]))


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