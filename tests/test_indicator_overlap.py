from .config import CORRELATION, CORRELATION_THRESHOLD, error_analysis, sample_data, VERBOSE
from .context import pandas_ta

from unittest import TestCase
import pandas.testing as pdt
from pandas import DataFrame, Series

import pandas as pd
import talib as tal


class TestOverlap(TestCase):
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


    def test_dema(self):
        result = pandas_ta.dema(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "DEMA_10")

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
        result = pandas_ta.ema(self.close, presma=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "EMA_10")

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
        result = pandas_ta.fwma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "FWMA_10")

    def test_hilo(self):
        result = pandas_ta.hilo(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "HILO_13_21")

    def test_hl2(self):
        result = pandas_ta.hl2(self.high, self.low)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "HL2")

    def test_hlc3(self):
        result = pandas_ta.hlc3(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "HLC3")

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
        result = pandas_ta.hma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "HMA_10")

    def test_kama(self):
        result = pandas_ta.kama(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "KAMA_10_2_30")

    def test_ichimoku(self):
        ichimoku, span = pandas_ta.ichimoku(self.high, self.low, self.close)
        self.assertIsInstance(ichimoku, DataFrame)
        self.assertIsInstance(span, DataFrame)
        self.assertEqual(ichimoku.name, "ICHIMOKU_9_26_52")
        self.assertEqual(span.name, "ICHISPAN_9_26")

    def test_linreg(self):
        result = pandas_ta.linreg(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "LR_14")

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
        result = pandas_ta.linreg(self.close, angle=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "LRa_14")

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
        result = pandas_ta.linreg(self.close, intercept=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "LRb_14")

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
        result = pandas_ta.linreg(self.close, r=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "LRr_14")

    def test_linreg_slope(self):
        result = pandas_ta.linreg(self.close, slope=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "LRm_14")

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
        result = pandas_ta.midpoint(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "MIDPOINT_2")

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
        result = pandas_ta.midprice(self.high, self.low)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "MIDPRICE_2")

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
        result = pandas_ta.ohlc4(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "OHLC4")

    def test_pwma(self):
        result = pandas_ta.pwma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "PWMA_10")

    def test_rma(self):
        result = pandas_ta.rma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "RMA_10")

    def test_sinwma(self):
        result = pandas_ta.sinwma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "SINWMA_14")

    def test_sma(self):
        result = pandas_ta.sma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "SMA_10")

        try:
            expected = tal.SMA(self.close, 10)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_ssf(self):
        result = pandas_ta.ssf(self.close, poles=2)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "SSF_10_2")

        result = pandas_ta.ssf(self.close, poles=3)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "SSF_10_3")

    def test_swma(self):
        result = pandas_ta.swma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "SWMA_10")

    def test_supertrend(self):
        result = pandas_ta.supertrend(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "SUPERT_7_3.0")

    def test_t3(self):
        result = pandas_ta.t3(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "T3_10_0.7")

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
        result = pandas_ta.tema(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "TEMA_10")

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
        result = pandas_ta.trima(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "TRIMA_10")

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
        result = pandas_ta.vwap(self.high, self.low, self.close, self.volume)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "VWAP")

    def test_vwma(self):
        result = pandas_ta.vwma(self.close, self.volume)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "VWMA_10")

    def test_wcp(self):
        result = pandas_ta.wcp(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "WCP")

        try:
            expected = tal.WCLPRICE(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_wma(self):
        result = pandas_ta.wma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "WMA_10")

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
        result = pandas_ta.zlma(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ZL_EMA_10")
