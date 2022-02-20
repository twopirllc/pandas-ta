# -*- coding: utf-8 -*-
from unittest import TestCase
from pandas import DataFrame, Series

from .config import sample_data
from .context import pandas_ta


class TestPerformace(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.close = cls.data["close"]
        cls.islong = (cls.close > pandas_ta.sma(cls.close, length=8)).astype(int)
        cls.pctret = pandas_ta.percent_return(cls.close, cumulative=False)
        cls.logret = pandas_ta.percent_return(cls.close, cumulative=False)


    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.close
        del cls.islong
        del cls.pctret
        del cls.logret

    def setUp(self): pass
    def tearDown(self): pass


    def test_cube(self):
        """Transform: Cube"""
        result = pandas_ta.cube(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "CUBE_3.0_-1")

    def test_inverse_fisher(self):
        """Transform: Inverse Fisher"""
        result = pandas_ta.ifisher(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "INVFISHER_1.0")

    def test_remap(self):
        """Transform: Remap"""
        result = pandas_ta.remap(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "REMAP_0.0_100.0_-1.0_1.0")