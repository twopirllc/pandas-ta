# -*- coding: utf-8 -*-
from unittest import TestCase, skip
from pandas import DataFrame, Series
import pandas.testing as pdt
import talib as tal

from .config import error_analysis, sample_data, CORRELATION, CORRELATION_THRESHOLD
from .context import pandas_ta


class TestCandle(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.data.columns = cls.data.columns.str.lower()
        cls.open = cls.data["open"]
        cls.high = cls.data["high"]
        cls.low = cls.data["low"]
        cls.close = cls.data["close"]
        if "volume" in cls.data.columns:
            cls.volume = cls.data["volume"]

    @classmethod
    def tearDownClass(cls):
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        if hasattr(cls, "volume"):
            del cls.volume
        del cls.data

    def setUp(self): pass
    def tearDown(self): pass


    def test_cdl_pattern(self):
        """Candle: TA Lib Candle Patterns"""
        result = pandas_ta.cdl_pattern(self.open, self.high, self.low, self.close, name="all")
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(len(result.columns), len(pandas_ta.CDL_PATTERN_NAMES))

        result = pandas_ta.cdl_pattern(self.open, self.high, self.low, self.close, name="doji")
        self.assertIsInstance(result, DataFrame)

        result = pandas_ta.cdl_pattern(self.open, self.high, self.low, self.close, name=["doji", "inside"])
        self.assertIsInstance(result, DataFrame)

    def test_cdl_doji(self):
        """Candle: Doji"""
        result = pandas_ta.cdl_doji(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CDL_DOJI_10_0.1")

        try:
            expected = tal.CDLDOJI(self.open, self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_cdl_inside(self):
        """Candle: Inside"""
        result = pandas_ta.cdl_inside(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CDL_INSIDE")

        result = pandas_ta.cdl_inside(self.open, self.high, self.low, self.close, asbool=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CDL_INSIDE")

    def test_cdl_z(self):
        """Candle: Z Score"""
        result = pandas_ta.cdl_z(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "CDL_Z_30_1")

    def test_ha(self):
        """Candle: Heiken Ashi"""
        result = pandas_ta.ha(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "Heikin-Ashi")
