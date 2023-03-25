# -*- coding: utf-8 -*-
from unittest import TestCase, skip
import numpy as np
import pandas.testing as pdt
from pandas import DataFrame, Series

import talib as tal

from .config import error_analysis, sample_data, sample_adx_data, CORRELATION, CORRELATION_THRESHOLD
from .context import pandas_ta


class TestTrend(TestCase):
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


    def test_adx(self):
        """Trend: ADX"""
        result = pandas_ta.adx(self.high, self.low, self.close, talib=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "ADX_14")

        try:
            expected = tal.ADX(self.high, self.low, self.close)
            pdt.assert_series_equal(result.iloc[:, 0], expected)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 0], expected)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.adx(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "ADX_14")

    def test_adx_result_should_sync_with_trading_view(self):
        data = sample_adx_data
        high, low, close = data["high"], data["low"], data["close"]
        result = pandas_ta.adx(high, low, close, tvmode=True)

        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "ADX_14")

        result = result.iloc[13:]
        result.reset_index(drop=True, inplace=True)

        expected = DataFrame(
            {
                "ADX_14":
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    9.874338,
                    10.408195,
                    10.799274,
                ],
                "DMP_14": [
                    None,
                    13.686598,
                    14.247809,
                    13.436449,
                    17.946530,
                    17.193874,
                    19.214901,
                    17.860325,
                    16.899406,
                    16.207983,
                    15.998908,
                    15.202702,
                    14.621306,
                    14.303707,
                    13.451093,
                    12.932243,
                    12.840198,
                ],
                "DMN_14": [
                    None,
                    21.954010,
                    21.055379,
                    23.102292,
                    21.120552,
                    20.234781,
                    18.827331,
                    19.298744,
                    19.029033,
                    18.250478,
                    17.414460,
                    16.772558,
                    16.131126,
                    15.780731,
                    19.097781,
                    18.361121,
                    17.689287,
                ],
            }
        )
        print(f"\nADX result:\n{result}")
        print(f"\nADX expected:\n{expected}\n")
        pdt.assert_frame_equal(result, expected)

    def test_amat(self):
        """Trend: AMAT"""
        result = pandas_ta.amat(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "AMATe_8_21_2")

    def test_aroon(self):
        """Trend: AROON"""
        result = pandas_ta.aroon(self.high, self.low, talib=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "AROON_14")

        try:
            expected = tal.AROON(self.high, self.low)
            expecteddf = DataFrame({"AROOND_14": expected[0], "AROONU_14": expected[1]})
            pdt.assert_frame_equal(result, expecteddf)
        except AssertionError:
            try:
                aroond_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 0], expecteddf.iloc[:, 0])
                self.assertGreater(aroond_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 0], CORRELATION, ex)

            try:
                aroonu_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 1], expecteddf.iloc[:, 1])
                self.assertGreater(aroonu_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 1], CORRELATION, ex, newline=False)

        result = pandas_ta.aroon(self.high, self.low)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "AROON_14")

    def test_aroon_osc(self):
        """Trend: AROON OSC"""
        result = pandas_ta.aroon(self.high, self.low)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "AROON_14")

        try:
            expected = tal.AROONOSC(self.high, self.low)
            pdt.assert_series_equal(result.iloc[:, 2], expected)
        except AssertionError:
            try:
                aroond_corr = pandas_ta.utils.df_error_analysis(result.iloc[:,2], expected)
                self.assertGreater(aroond_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 0], CORRELATION, ex)

    def test_chop(self):
        """Trend: Chop"""
        result = pandas_ta.chop(self.high, self.low, self.close, ln=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CHOP_14_1_100.0")

        result = pandas_ta.chop(self.high, self.low, self.close, ln=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CHOPln_14_1_100.0")

    def test_cksp(self):
        """Trend: CKSP"""
        result = pandas_ta.cksp(self.high, self.low, self.close, tvmode=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "CKSP_10_3_20")

    def test_cksp_tv(self):
        """Trend: CKSP (TV)"""
        result = pandas_ta.cksp(self.high, self.low, self.close, tvmode=True)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "CKSP_10_1_9")

    def test_decay(self):
        """Trend: DECAY"""
        result = pandas_ta.decay(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "LDECAY_1")

        result = pandas_ta.decay(self.close, mode="exp")
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "EXPDECAY_1")

    def test_decreasing(self):
        """Trend: Decreasing"""
        result = pandas_ta.decreasing(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "DEC_1")

        result = pandas_ta.decreasing(self.close, length=3, strict=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "SDEC_3")

    def test_dpo(self):
        """Trend: DPO"""
        result = pandas_ta.dpo(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "DPO_20")

    def test_increasing(self):
        """Trend: Increasing"""
        result = pandas_ta.increasing(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "INC_1")

        result = pandas_ta.increasing(self.close, length=3, strict=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "SINC_3")

    def test_long_run(self):
        """Trend: Long Run"""
        result = pandas_ta.long_run(self.close, self.open)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "LR_2")

    def test_psar(self):
        """Trend: PSAR"""
        result = pandas_ta.psar(self.high, self.low)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "PSAR_0.02_0.2")

        # Combine Long and Short SAR"s into one SAR value
        psar = result[result.columns[:2]].fillna(0)
        psar = psar[psar.columns[0]] + psar[psar.columns[1]]
        psar.iloc[0] = np.nan
        psar.name = result.name

        try:
            expected = tal.SAR(self.high, self.low)
            psar_corr = pandas_ta.utils.df_error_analysis(psar, expected)
            pdt.assert_series_equal(psar, expected)
        except AssertionError:
            try:
                psar_corr = pandas_ta.utils.df_error_analysis(psar, expected)
                self.assertGreater(psar_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(psar, CORRELATION, ex)

    def test_qstick(self):
        """Trend: QSTICK"""
        result = pandas_ta.qstick(self.open, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "QS_10")

    def test_short_run(self):
        """Trend: Short Run"""
        result = pandas_ta.short_run(self.close, self.open)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "SR_2")

    def test_trendflex(self):
        """Trend: Trendflex"""
        result = pandas_ta.trendflex(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "TRENDFLEX_20_20_0.04")

    def test_ttm_trend(self):
        """Trend: TTM Trend"""
        result = pandas_ta.ttm_trend(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "TTMTREND_6")

    def test_vhf(self):
        """Trend: VHF"""
        result = pandas_ta.vhf(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "VHF_28")

    def test_vortex(self):
        """Trend: VORTEX"""
        result = pandas_ta.vortex(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "VTX_14")
