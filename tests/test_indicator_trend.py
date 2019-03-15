from .config import error_analysis, sample_data, CORRELATION, CORRELATION_THRESHOLD, VERBOSE
from .context import pandas_ta

from unittest import TestCase, skip
import pandas.util.testing as pdt
from pandas import DataFrame, Series

import talib as tal



class TestTrend(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.open = cls.data['open']
        cls.high = cls.data['high']
        cls.low = cls.data['low']
        cls.close = cls.data['close']
        cls.volume = cls.data['volume']

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        del cls.volume


    def setUp(self):
        self.trend = pandas_ta.trend

    def tearDown(self):
        del self.trend
    

    def test_adx(self):
        result = self.trend.adx(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'ADX_14')

        try:
            expected = tal.ADX(self.high, self.low, self.close)
            pdt.assert_series_equal(result.iloc[:,0], expected)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result.iloc[:,0], expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_aroon(self):
        result = self.trend.aroon(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'AROON_14')

        try:
            expected = tal.AROON(self.high, self.low)
            expecteddf = DataFrame({'AROOND_14': expected[0], 'AROONU_14': expected[1]})
            pdt.assert_frame_equal(result, expecteddf)
        except AssertionError as ae:
            try:
                aroond_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,0], expecteddf.iloc[:,0], col=CORRELATION)
                self.assertGreater(aroond_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,0], CORRELATION, ex)

            try:
                aroonu_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,1], expecteddf.iloc[:,1], col=CORRELATION)
                self.assertGreater(aroonu_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,1], CORRELATION, ex, newline=False)

    def test_decreasing(self):
        result = self.trend.decreasing(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'DEC_1')

    def test_dpo(self):
        result = self.trend.dpo(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'DPO_1')

    def test_increasing(self):
        result = self.trend.increasing(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'INC_1')

    def test_qstick(self):
        result = self.trend.qstick(self.open, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'QS_10')

    def test_vortex(self):
        result = self.trend.vortex(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'VTX_14')