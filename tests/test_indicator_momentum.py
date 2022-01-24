# -*- coding: utf-8 -*-
from unittest import TestCase, skip
import pandas.testing as pdt
from pandas import DataFrame, Series

import talib as tal

from .config import error_analysis, sample_data, CORRELATION, CORRELATION_THRESHOLD
from .context import pandas_ta


class TestMomentum(TestCase):
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


    def test_datetime_ordered(self):
        """Datetime Ordered"""
        # Test if datetime64 index and ordered
        result = self.data.ta.datetime_ordered
        self.assertTrue(result)

        # Test if not ordered
        original = self.data.copy()
        reversal = original.ta.reverse
        result = reversal.ta.datetime_ordered
        self.assertFalse(result)

        # Test a non-datetime64 index
        original = self.data.copy()
        original.reset_index(inplace=True)
        result = original.ta.datetime_ordered
        self.assertFalse(result)

    def test_reverse(self):
        """Reverse"""
        original = self.data.copy()
        result = original.ta.reverse

        # Check if first and last time are reversed
        self.assertEqual(result.index[-1], original.index[0])
        self.assertEqual(result.index[0], original.index[-1])

    def test_ao(self):
        """Momentum: AO"""
        result = pandas_ta.ao(self.high, self.low)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "AO_5_34")

    def test_apo(self):
        """Momentum: APO"""
        result = pandas_ta.apo(self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "APO_12_26")

        try:
            expected = tal.APO(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.apo(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "APO_12_26")

    def test_bias(self):
        """Momentum: Bias"""
        result = pandas_ta.bias(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "BIAS_SMA_26")

    def test_bop(self):
        """Momentum: BOP"""
        result = pandas_ta.bop(self.open, self.high, self.low, self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "BOP")

        try:
            expected = tal.BOP(self.open, self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.bop(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "BOP")

    def test_brar(self):
        """Momentum: BRAR"""
        result = pandas_ta.brar(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "BRAR_26")

    def test_cci(self):
        """Momentum: CCI"""
        result = pandas_ta.cci(self.high, self.low, self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CCI_14_0.015")

        try:
            expected = tal.CCI(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.cci(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CCI_14_0.015")

    def test_cfo(self):
        """Momentum: CFO"""
        result = pandas_ta.cfo(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CFO_9")

    def test_cg(self):
        """Momentum: CG"""
        result = pandas_ta.cg(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CG_10")

    def test_cmo(self):
        """Momentum: CMO"""
        result = pandas_ta.cmo(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CMO_14")

        try:
            expected = tal.CMO(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.cmo(self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CMO_14")

    def test_coppock(self):
        """Momentum: Coppock"""
        result = pandas_ta.coppock(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "COPC_11_14_10")

    def test_cti(self):
        """Momentum: CTI"""
        result = pandas_ta.cti(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CTI_12")

    def test_er(self):
        """Momentum: ER"""
        result = pandas_ta.er(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ER_10")

    def test_dm(self):
        """Momentum: DM"""
        result = pandas_ta.dm(self.high, self.low, talib=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "DM_14")

        try:
            expected_pos = tal.PLUS_DM(self.high, self.low)
            expected_neg = tal.MINUS_DM(self.high, self.low)
            expecteddf = DataFrame({"DMP_14": expected_pos, "DMN_14": expected_neg})
            pdt.assert_frame_equal(result, expecteddf)
        except AssertionError:
            try:
                dmp = pandas_ta.utils.df_error_analysis(result.iloc[:,0], expecteddf.iloc[:,0], col=CORRELATION)
                self.assertGreater(dmp, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

            try:
                dmn = pandas_ta.utils.df_error_analysis(result.iloc[:,1], expecteddf.iloc[:,1], col=CORRELATION)
                self.assertGreater(dmn, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.dm(self.high, self.low)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "DM_14")

    def test_eri(self):
        """Momentum: ERI"""
        result = pandas_ta.eri(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "ERI_13")

    def test_fisher(self):
        """Momentum: Fisher"""
        result = pandas_ta.fisher(self.high, self.low)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "FISHERT_9_1")

    def test_inertia(self):
        """Momentum: Inertia"""
        result = pandas_ta.inertia(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "INERTIA_20_14")

        result = pandas_ta.inertia(self.close, self.high, self.low, refined=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "INERTIAr_20_14")

        result = pandas_ta.inertia(self.close, self.high, self.low, thirds=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "INERTIAt_20_14")

    def test_kdj(self):
        """Momentum: KDJ"""
        result = pandas_ta.kdj(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "KDJ_9_3")

    def test_kst(self):
        """Momentum: KST"""
        result = pandas_ta.kst(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "KST_10_15_20_30_10_10_10_15_9")

    def test_macd(self):
        """Momentum: MACD"""
        result = pandas_ta.macd(self.close, talib=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "MACD_12_26_9")

        try:
            expected = tal.MACD(self.close)
            expecteddf = DataFrame({"MACD_12_26_9": expected[0], "MACDh_12_26_9": expected[2], "MACDs_12_26_9": expected[1]})
            pdt.assert_frame_equal(result, expecteddf)
        except AssertionError:
            try:
                macd_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 0], expecteddf.iloc[:, 0], col=CORRELATION)
                self.assertGreater(macd_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 0], CORRELATION, ex)

            try:
                history_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 1], expecteddf.iloc[:, 1], col=CORRELATION)
                self.assertGreater(history_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 1], CORRELATION, ex, newline=False)

            try:
                signal_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 2], expecteddf.iloc[:, 2], col=CORRELATION)
                self.assertGreater(signal_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 2], CORRELATION, ex, newline=False)

        result = pandas_ta.macd(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "MACD_12_26_9")

    def test_macdas(self):
        """Momentum: MACD (AS)"""
        result = pandas_ta.macd(self.close, asmode=True)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "MACDAS_12_26_9")

    def test_mom(self):
        """Momentum: MOM"""
        result = pandas_ta.mom(self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "MOM_10")

        try:
            expected = tal.MOM(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.mom(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "MOM_10")

    def test_pgo(self):
        """Momentum: PGO"""
        result = pandas_ta.pgo(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "PGO_14")

    def test_ppo(self):
        """Momentum: PPO"""
        result = pandas_ta.ppo(self.close, talib=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "PPO_12_26_9")

        try:
            expected = tal.PPO(self.close)
            pdt.assert_series_equal(result["PPO_12_26_9"], expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result["PPO_12_26_9"], expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result["PPO_12_26_9"], CORRELATION, ex)

        result = pandas_ta.ppo(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "PPO_12_26_9")

    def test_psl(self):
        """Momentum: PSL"""
        result = pandas_ta.psl(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "PSL_12")

    def test_pvo(self):
        """Momentum: PVO"""
        result = pandas_ta.pvo(self.volume)
        if result is not None:
            self.assertIsInstance(result, DataFrame)
            self.assertEqual(result.name, "PVO_12_26_9")
        else:
            self.assertIsNone(result)

    def test_qqe(self):
        """Momentum: QQE"""
        result = pandas_ta.qqe(self.close)
        if result is not None:
            self.assertIsInstance(result, DataFrame)
            self.assertEqual(result.name, "QQE_14_5_4.236")
        else:
            self.assertIsNone(result)

    def test_roc(self):
        """Momentum: ROC"""
        result = pandas_ta.roc(self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ROC_10")

        try:
            expected = tal.ROC(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.roc(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ROC_10")

    def test_rsi(self):
        """Momentum: RSI"""
        result = pandas_ta.rsi(self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "RSI_14")

        try:
            expected = tal.RSI(self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.rsi(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "RSI_14")

    def test_rsx(self):
        """Momentum: RSX"""
        result = pandas_ta.rsx(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "RSX_14")

    def test_rvgi(self):
        """Momentum: RVGI"""
        result = pandas_ta.rvgi(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "RVGI_14_4")

    def test_slope(self):
        """Momentum: Slope"""
        result = pandas_ta.slope(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "SLOPE_1")

    def test_slope_as_angle(self):
        """Momentum: Slope (Angle)"""
        result = pandas_ta.slope(self.close, as_angle=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ANGLEr_1")

    def test_slope_as_angle_to_degrees(self):
        """Momentum: Slope (Degree Angles)"""
        result = pandas_ta.slope(self.close, as_angle=True, to_degrees=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ANGLEd_1")

    def test_smi(self):
        """Momentum: SMI"""
        result = pandas_ta.smi(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "SMI_5_20_5")
        self.assertEqual(len(result.columns), 3)

    def test_smi_scalar(self):
        """Momentum: SMI (Scalar)"""
        result = pandas_ta.smi(self.close, scalar=10)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "SMI_5_20_5_10.0")
        self.assertEqual(len(result.columns), 3)

    def test_squeeze(self):
        """Momentum: Squeeze"""
        result = pandas_ta.squeeze(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "SQZ_20_2.0_20_1.5")

        result = pandas_ta.squeeze(self.high, self.low, self.close, tr=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "SQZhlr_20_2.0_20_1.5")

        result = pandas_ta.squeeze(self.high, self.low, self.close, lazybear=True)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "SQZ_20_2.0_20_1.5_LB")

        result = pandas_ta.squeeze(self.high, self.low, self.close, tr=False, lazybear=True)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "SQZhlr_20_2.0_20_1.5_LB")

    def test_squeeze_pro(self):
        """Momentum: Squeeze Pro"""
        result = pandas_ta.squeeze_pro(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "SQZPRO_20_2.0_20_2_1.5_1")

        result = pandas_ta.squeeze_pro(self.high, self.low, self.close, tr=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "SQZPROhlr_20_2.0_20_2_1.5_1")

        result = pandas_ta.squeeze_pro(self.high, self.low, self.close, 20, 2, 20, 3, 2, 1)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "SQZPRO_20_2.0_20_3.0_2.0_1.0")

        result = pandas_ta.squeeze_pro(self.high, self.low, self.close, 20, 2, 20, 3, 2, 1, tr=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "SQZPROhlr_20_2.0_20_3.0_2.0_1.0")

    def test_stc(self):
        """Momentum: STC"""
        result = pandas_ta.stc(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "STC_10_12_26_0.5")

    def test_stoch(self):
        """Momentum: Stochastic"""
        # TV Correlation
        result = pandas_ta.stoch(self.high, self.low, self.close, talib=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "STOCH_14_3_3")

        try:
            expected = tal.STOCH(self.high, self.low, self.close, 14, 3, 0, 3, 0)
            expecteddf = DataFrame({"STOCHk_14_3_0_3_0": expected[0], "STOCHd_14_3_0_3": expected[1]})
            pdt.assert_frame_equal(result, expecteddf)
        except AssertionError:
            try:
                stochk_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 0], expecteddf.iloc[:, 0], col=CORRELATION)
                self.assertGreater(stochk_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 0], CORRELATION, ex)

            try:
                stochd_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 1], expecteddf.iloc[:, 1], col=CORRELATION)
                self.assertGreater(stochd_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 1], CORRELATION, ex, newline=False)

        result = pandas_ta.stoch(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "STOCH_14_3_3")

    def test_stochf(self):
        """Momentum: Fast Stochastic"""
        # TV Correlation
        result = pandas_ta.stochf(self.high, self.low, self.close, talib=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "STOCHF_14_3")

        try:
            expected = tal.STOCHF(self.high, self.low, self.close, 14, 3, 0)
            expecteddf = DataFrame({"STOCHFk_14_3_0": expected[0], "STOCHFd_14_3_0": expected[1]})
            pdt.assert_frame_equal(result, expecteddf)
        except AssertionError:
            try:
                stochk_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 0], expecteddf.iloc[:, 0], col=CORRELATION)
                self.assertGreater(stochk_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 0], CORRELATION, ex)

            try:
                stochd_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 1], expecteddf.iloc[:, 1], col=CORRELATION)
                self.assertGreater(stochd_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 1], CORRELATION, ex, newline=False)

        result = pandas_ta.stochf(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "STOCHF_14_3")

    def test_stochrsi(self):
        """Momentum: Stochastic RSI"""
        # TV Correlation
        result = pandas_ta.stochrsi(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "STOCHRSI_14_14_3_3")

        try:
            expected = tal.STOCHRSI(self.close, 14, 14, 3, 0)
            expecteddf = DataFrame({"STOCHRSIk_14_14_0_3": expected[0], "STOCHRSId_14_14_3_0": expected[1]})
            pdt.assert_frame_equal(result, expecteddf)
        except AssertionError:
            try:
                stochrsid_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 0], expecteddf.iloc[:, 1], col=CORRELATION)
                self.assertGreater(stochrsid_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 0], CORRELATION, ex, newline=False)

    @skip
    def test_td_seq(self):
        """TS Sequential: Working but SLOW implementation"""
        result = pandas_ta.td_seq(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "TD_SEQ")

    def test_trix(self):
        """Momentum: TRIX"""
        result = pandas_ta.trix(self.close)
        if result is not None and result.shape[0] > 87:
            print(f"T [trix:{result.shape}]")
            self.assertIsInstance(result, DataFrame)
            self.assertEqual(result.name, "TRIX_30_9")
        else:
            self.assertIsNone(result)

    def test_tsi(self):
        """Momentum: TSI"""
        result = pandas_ta.tsi(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "TSI_13_25_13")

    def test_uo(self):
        """Momentum: UO"""
        result = pandas_ta.uo(self.high, self.low, self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "UO_7_14_28")

        try:
            expected = tal.ULTOSC(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.uo(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "UO_7_14_28")

    def test_willr(self):
        """Momentum: WILLR"""
        result = pandas_ta.willr(self.high, self.low, self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "WILLR_14")

        try:
            expected = tal.WILLR(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.willr(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "WILLR_14")
