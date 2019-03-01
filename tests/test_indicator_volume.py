from .config import error_analysis, sample_data, CORRELATION, CORRELATION_THRESHOLD, VERBOSE
from .context import pandas_ta

from unittest import TestCase, skip
import pandas.util.testing as pdt
from pandas import DataFrame, Series

import talib as tal



class TestVolume(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.open = cls.data['open']
        cls.high = cls.data['high']
        cls.low = cls.data['low']
        cls.close = cls.data['close']
        cls.volume_ = cls.data['volume']

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        del cls.volume_


    def setUp(self):
        self.volume = pandas_ta.volume

    def tearDown(self):
        del self.volume


    def test_ad(self):
        result = self.volume.ad(self.high, self.low, self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'AD')

        try:
            expected = tal.AD(self.high, self.low, self.close, self.volume_)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_adosc(self):
        result = self.volume.adosc(self.high, self.low, self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'ADOSC_12_26')

        try:
            expected = tal.AD(self.high, self.low, self.close, self.volume_)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_cmf(self):
        result = self.volume.cmf(self.high, self.low, self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'CMF_20')

    def test_efi(self):
        result = self.volume.efi(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'EFI_13')

    def test_eom(self):
        result = self.volume.eom(self.high, self.low, self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'EOM_14_100000000')

    def test_mfi(self):
        result = self.volume.mfi(self.high, self.low, self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'MFI_14')

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
        result = self.volume.nvi(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'NVI_1')

    def test_obv(self):
        result = self.volume.obv(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'OBV')

        try:
            expected = tal.OBV(self.close, self.volume_)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError as ae:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected, col=CORRELATION)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

    def test_pvol(self):
        result = self.volume.pvol(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'PVOL')

    def test_pvt(self):
        result = self.volume.pvt(self.close, self.volume_)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'PVT')

    def test_vp(self):
        result = self.volume.vp(self.close, self.volume_)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, 'VP_10')
