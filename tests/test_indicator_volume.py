from .config import error_analysis, sample_data, CORRELATION, CORRELATION_THRESHOLD, VERBOSE
from .context import pandas_ta

from unittest import TestCase, skip
import pandas.testing as pdt
from pandas import DataFrame, Series

import talib as tal


class TestVolume(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.data.columns = cls.data.columns.str.lower()
        cls.open = cls.data["open"]
        cls.high = cls.data["high"]
        cls.low = cls.data["low"]
        cls.close = cls.data["close"]
        if "volume" in cls.data.columns:
            cls.volume_ = cls.data["volume"]

    @classmethod
    def tearDownClass(cls):
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        if hasattr(cls, "volume"):
            del cls.volume_
        del cls.data

    def setUp(self): pass
    def tearDown(self): pass


    def test_ad(self):
        result = pandas_ta.ad(self.high, self.low, self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "AD")

        try:
            expected = tal.AD(self.high, self.low, self.close, self.volume_)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_ad_open(self):
        result = pandas_ta.ad(self.high, self.low, self.close, self.volume_, self.open)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ADo")

    def test_adosc(self):
        result = pandas_ta.adosc(self.high, self.low, self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ADOSC_3_10")

        try:
            expected = tal.ADOSC(self.high, self.low, self.close, self.volume_)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_aobv(self):
        result = pandas_ta.aobv(self.close, self.volume_)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "AOBVe_4_12_2_2_2")

    def test_cmf(self):
        result = pandas_ta.cmf(self.high, self.low, self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "CMF_20")

    def test_efi(self):
        result = pandas_ta.efi(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "EFI_13")

    def test_eom(self):
        result = pandas_ta.eom(self.high, self.low, self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "EOM_14_100000000")

    def test_mfi(self):
        result = pandas_ta.mfi(self.high, self.low, self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "MFI_14")

        try:
            expected = tal.MFI(self.high, self.low, self.close, self.volume_)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_nvi(self):
        result = pandas_ta.nvi(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "NVI_1")

    def test_obv(self):
        result = pandas_ta.obv(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "OBV")

        try:
            expected = tal.OBV(self.close, self.volume_)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_pvi(self):
        result = pandas_ta.pvi(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "PVI_1")

    def test_pvol(self):
        result = pandas_ta.pvol(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "PVOL")

    def test_pvr(self):
        result = pandas_ta.pvr(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "PVR")
        # sample indicator values from SPY
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 3)
        self.assertEqual(result[4], 2)
        self.assertEqual(result[6], 4)

    def test_pvt(self):
        result = pandas_ta.pvt(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "PVT")

    def test_vp(self):
        result = pandas_ta.vp(self.close, self.volume_)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "VP_10")
