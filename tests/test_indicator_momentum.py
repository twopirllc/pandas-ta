from .config import error_analysis, sample_data, CORRELATION, CORRELATION_THRESHOLD, VERBOSE
from .context import pandas_ta

from unittest import TestCase, skip
import pandas.util.testing as pdt
from pandas import DataFrame, Series

import talib as tal



class TestMomentum(TestCase):
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


    def setUp(self): pass
    def tearDown(self): pass
    

    def test_ao(self):
        result = pandas_ta.ao(self.high, self.low)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'AO_5_34')

    def test_apo(self):
        result = pandas_ta.apo(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'APO_12_26')

        try:
            expected = tal.APO(self.close, 12, 26)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_bop(self):
        result = pandas_ta.bop(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'BOP')

        try:
            expected = tal.BOP(self.open, self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_cci(self):
        result = pandas_ta.cci(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'CCI_20_0.015')

        try:
            expected = tal.CCI(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_cmo(self):
        result = pandas_ta.cmo(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'CMO_14')

        try:
            expected = tal.CMO(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_coppock(self):
        result = pandas_ta.coppock(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'COPC_11_14_10')

    def test_kst(self):
        result = pandas_ta.kst(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'KST_10_15_20_30_10_10_10_15_9')

    def test_macd(self):
        result = pandas_ta.macd(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'MACD_12_26_9')

        try:
            expected = tal.MACD(self.close)
            expecteddf = DataFrame({'MACD_12_26_9': expected[0], 'MACDH_12_26_9': expected[2], 'MACDS_12_26_9': expected[1]})
            pdt.assert_frame_equal(result, expecteddf)
        except AssertionError as ae:
            try:
                macd_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,0], expecteddf.iloc[:,0], col=CORRELATION)
                self.assertGreater(macd_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,0], CORRELATION, ex)

            try:
                history_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,1], expecteddf.iloc[:,1], col=CORRELATION)
                self.assertGreater(history_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,1], CORRELATION, ex, newline=False)

            try:
                signal_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,2], expecteddf.iloc[:,2], col=CORRELATION)
                self.assertGreater(signal_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,2], CORRELATION, ex, newline=False)

    def test_mom(self):
        result = pandas_ta.mom(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'MOM_10')

        try:
            expected = tal.MOM(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_ppo(self):
        result = pandas_ta.ppo(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'PPO_12_26_9')

        try:
            expected = tal.PPO(self.close)
            pdt.assert_series_equal(result['PPO_12_26_9'], expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result['PPO_12_26_9'], expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result['PPO_12_26_9'], CORRELATION, ex)

    def test_roc(self):
        result = pandas_ta.roc(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'ROC_10')

        try:
            expected = tal.ROC(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_rsi(self):
        result = pandas_ta.rsi(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'RSI_14')

        try:
            expected = tal.RSI(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_slope(self):
        result = pandas_ta.slope(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'SLOPE_1')

    def test_slope_as_angle(self):
        result = pandas_ta.slope(self.close, as_angle=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'ANGLEr_1')

    def test_slope_as_angle_to_degrees(self):
        result = pandas_ta.slope(self.close, as_angle=True, to_degrees=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'ANGLEd_1')

    def test_stoch(self):
        result = pandas_ta.stoch(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'STOCH_14_5_3')

        try:
            tal_stochf = tal.STOCHF(self.high, self.low, self.close)
            tal_stoch = tal.STOCH(self.high, self.low, self.close)
            tal_stochdf = DataFrame({'STOCHF_14': tal_stochf[0], 'STOCHF_3': tal_stochf[1], 'STOCH_5': tal_stoch[0], 'STOCH_3': tal_stoch[1]})
            pdt.assert_frame_equal(result, tal_stochdf)
        except AssertionError as ae:
            try:
                stochfk_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,0], tal_stochdf.iloc[:,0], col=CORRELATION)
                self.assertGreater(stochfk_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,0], CORRELATION, ex)

            try:
                stochfd_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,1], tal_stochdf.iloc[:,1], col=CORRELATION)
                self.assertGreater(stochfd_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,1], CORRELATION, ex, newline=False)

            try:
                stochsk_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,2], tal_stochdf.iloc[:,2], col=CORRELATION)
                self.assertGreater(stochsk_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,2], CORRELATION, ex, newline=False)

            try:
                stochsd_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,3], tal_stochdf.iloc[:,3], col=CORRELATION)
                self.assertGreater(stochsd_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:,3], CORRELATION, ex, newline=False)

    def test_trix(self):
        result = pandas_ta.trix(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'TRIX_30')

    def test_tsi(self):
        result = pandas_ta.tsi(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'TSI_13_25')

    def test_uo(self):
        result = pandas_ta.uo(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'UO_7_14_28')

        try:
            expected = tal.ULTOSC(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_willr(self):
        result = pandas_ta.willr(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'WILLR_14')

        try:
            expected = tal.WILLR(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)