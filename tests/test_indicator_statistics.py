from .config import error_analysis, sample_data, CORRELATION, CORRELATION_THRESHOLD, VERBOSE
from .context import pandas_ta

from unittest import TestCase, skip
import pandas.util.testing as pdt
from pandas import DataFrame, Series

import talib as tal



class TestStatistics(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.data.columns = cls.data.columns.str.lower()
        cls.open = cls.data['open']
        cls.high = cls.data['high']
        cls.low = cls.data['low']
        cls.close = cls.data['close']
        if 'volume' in cls.data.columns: cls.volume = cls.data['volume']

    @classmethod
    def tearDownClass(cls):
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        if hasattr(cls, 'volume'): del cls.volume
        del cls.data


    def setUp(self):
        self.stats = pandas_ta.statistics

    def tearDown(self):
        del self.stats
    

    def test_kurtosis(self):
        result = self.stats.kurtosis(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'KURT_30')

    def test_mad(self):
        result = self.stats.mad(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'MAD_30')

    def test_median(self):
        result = self.stats.median(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'MEDIAN_30')

    def test_quantile(self):
        result = self.stats.quantile(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'QTL_30_0.5')

    def test_skew(self):
        result = self.stats.skew(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'SKEW_30')

    def test_stdev(self):
        result = self.stats.stdev(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'STDEV_30')

        try:
            expected = tal.STDDEV(self.close, 30)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_variance(self):
        result = self.stats.variance(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'VAR_30')

        try:
            expected = tal.VAR(self.close, 30)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_zscore(self):
        result = self.stats.zscore(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'Z_30')