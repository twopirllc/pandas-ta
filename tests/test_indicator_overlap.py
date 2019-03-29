from .config import CORRELATION, CORRELATION_THRESHOLD, error_analysis, sample_data, VERBOSE
from .context import pandas_ta

from unittest import TestCase
import pandas.util.testing as pdt
from pandas import DataFrame, Series

import pandas as pd
import talib as tal



class TestOverlap(TestCase):
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
        self.overlap = pandas_ta.overlap

    def tearDown(self):
        del self.overlap
    

    def test_dema(self):
        result = self.overlap.dema(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'DEMA_10')

        try:
            expected = tal.DEMA(self.close, 10)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_ema(self):
        result = self.overlap.ema(self.close, presma=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'EMA_10')

        try:
            expected = tal.EMA(self.close, 10)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_fwma(self):
        result = self.overlap.fwma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'FWMA_10')

    def test_hl2(self):
        result = self.overlap.hl2(self.high, self.low)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'HL2')

    def test_hlc3(self):
        result = self.overlap.hlc3(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'HLC3')

        try:
            expected = tal.TYPPRICE(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_hma(self):
        result = self.overlap.hma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'HMA_10')

    def test_ichimoku(self):
        ichimoku, span = self.overlap.ichimoku(self.high, self.low, self.close)
        self.assertIsInstance(ichimoku, DataFrame)
        self.assertIsInstance(span, DataFrame)
        self.assertEqual(ichimoku.name, 'ICHIMOKU_9_26_52')
        self.assertEqual(span.name, 'ICHISPAN_9_26')

    def test_linreg(self):
        result = self.overlap.linreg(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'LR_14')

        try:
            expected = tal.LINEARREG(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_linreg_angle(self):
        result = self.overlap.linreg(self.close, angle=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'LRa_14')

        try:
            expected = tal.LINEARREG_ANGLE(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_linreg_intercept(self):
        result = self.overlap.linreg(self.close, intercept=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'LRb_14')

        try:
            expected = tal.LINEARREG_INTERCEPT(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_linreg_r(self):
        result = self.overlap.linreg(self.close, r=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'LRr_14')

    def test_linreg_slope(self):
        result = self.overlap.linreg(self.close, slope=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'LRm_14')

        try:
            expected = tal.LINEARREG_SLOPE(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_midpoint(self):
        result = self.overlap.midpoint(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'MIDPOINT_2')

        try:
            expected = tal.MIDPOINT(self.close, 2)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_midprice(self):
        result = self.overlap.midprice(self.high, self.low)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'MIDPRICE_2')

        try:
            expected = tal.MIDPRICE(self.high, self.low, 2)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_ohlc4(self):
        result = self.overlap.ohlc4(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'OHLC4')

    def test_pwma(self):
        result = self.overlap.pwma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'PWMA_10')

    def test_rma(self):
        result = self.overlap.rma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'RMA_10')

    def test_sma(self):
        result = self.overlap.sma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'SMA_10')

        try:
            expected = tal.SMA(self.close, 10)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_t3(self):
        result = self.overlap.t3(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'T3_10_0.7')

        try:
            expected = tal.T3(self.close, 10)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_tema(self):
        result = self.overlap.tema(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'TEMA_10')

        try:
            expected = tal.TEMA(self.close, 10)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_trima(self):
        result = self.overlap.trima(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'TRIMA_10')

        try:
            expected = tal.TRIMA(self.close, 10)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_vwap(self):
        result = self.overlap.vwap(self.high, self.low, self.close, self.volume)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'VWAP')

    def test_vwma(self):
        result = self.overlap.vwma(self.close, self.volume)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'VWMA_10')

    def test_wma(self):
        result = self.overlap.wma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'WMA_10')

        try:
            expected = tal.WMA(self.close, 10)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_zlma(self):
        result = self.overlap.zlma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'ZLEMA_10')
