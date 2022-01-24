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


    def test_drawdown(self):
        """Performance: Drawdown"""
        result = pandas_ta.drawdown(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "DD")

    def test_log_return(self):
        """Performance: Log Return"""
        result = pandas_ta.log_return(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "LOGRET_1")

    def test_cum_log_return(self):
        """Performance: Cumulative Log Return"""
        result = pandas_ta.log_return(self.close, cumulative=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CUMLOGRET_1")

    def test_percent_return(self):
        """Performance: Percent Return"""
        result = pandas_ta.percent_return(self.close, cumulative=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "PCTRET_1")

    def test_cum_percent_return(self):
        """Performance: Cumulative Percent Return"""
        result = pandas_ta.percent_return(self.close, cumulative=True)
        self.assertEqual(result.name, "CUMPCTRET_1")
