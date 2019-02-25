from .context import pandas_ta
from .data import sample_data, CORRELATION_THRESHOLD

from unittest import TestCase, skip
import pandas.util.testing as pdt
from pandas import DataFrame, Series

import talib as tal

VERBOSE = False


class TestStatistics(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.open = cls.data['open']
        cls.high = cls.data['high']
        cls.low = cls.data['low']
        cls.close = cls.data['close']
        cls.volume = cls.data['volume']
        cls.correlation_threshold = CORRELATION_THRESHOLD

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        del cls.volume


    def setUp(self):
        self.stats = pandas_ta.statistics

    def tearDown(self):
        del self.stats
    

    def test_kurtosis(self):
        kurtosis = self.stats.kurtosis(self.close)
        self.assertIsInstance(kurtosis, Series)
        self.assertEqual(kurtosis.name, 'KURT_30')

    def test_mad(self):
        mad = self.stats.mad(self.close)
        self.assertIsInstance(mad, Series)
        self.assertEqual(mad.name, 'MAD_30')

    def test_median(self):
        median = self.stats.median(self.close)
        self.assertIsInstance(median, Series)
        self.assertEqual(median.name, 'MEDIAN_30')

    def test_quantile(self):
        quantile = self.stats.quantile(self.close)
        self.assertIsInstance(quantile, Series)
        self.assertEqual(quantile.name, 'QTL_30_0.5')

    def test_skew(self):
        skew = self.stats.skew(self.close)
        self.assertIsInstance(skew, Series)
        self.assertEqual(skew.name, 'SKEW_30')

    def test_stdev(self):
        stdev = self.stats.stdev(self.close)
        self.assertIsInstance(stdev, Series)
        self.assertEqual(stdev.name, 'STDEV_30')

        try:
            tal_stdev = tal.STDDEV(self.close, 30)
            pdt.assert_series_equal(stdev, tal_stdev, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(stdev, tal_stdev)
            print(f"\n >> analysis['corr']: {analysis['corr']}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"stdev has low correlation: {analysis['corr']}")

    def test_variance(self):
        variance = self.stats.variance(self.close)
        self.assertIsInstance(variance, Series)
        self.assertEqual(variance.name, 'VAR_30')

        try:
            tal_variance = tal.VAR(self.close, 30)
            pdt.assert_series_equal(variance, tal_variance, check_names=False)
        except AssertionError as ae:
            analysis = pandas_ta.utils.df_error_analysis(variance, tal_variance)
            print(f"\n >> analysis['corr']: {analysis['corr']}") if VERBOSE else None
            if analysis['corr'] < self.correlation_threshold:
                raise AssertionError(f"variance has low correlation: {analysis['corr']}")


    def test_zscore(self):
        zscore = self.stats.zscore(self.close)
        self.assertIsInstance(zscore, Series)
        self.assertEqual(zscore.name, 'Z_30')