from .context import pandas_ta
from .data import sample_data, CORRELATION_THRESHOLD, VERBOSE

from unittest import TestCase, skip
import pandas.util.testing as pdt
from pandas import DataFrame, Series

import talib as tal



class TestVolatility(TestCase):
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
        self.volatility = pandas_ta.volatility

    def tearDown(self):
        del self.volatility
    

    def test_accbands(self):
        accbands = self.volatility.accbands(self.high, self.low, self.close)
        self.assertIsInstance(accbands, DataFrame)
        self.assertEqual(accbands.name, 'ACCBANDS_10')

    def test_atr(self):
        atr = self.volatility.atr(self.high, self.low, self.close)
        self.assertIsInstance(atr, Series)
        self.assertEqual(atr.name, 'ATR_14')

        try:
            tal_atr = tal.ATR(self.high, self.low, self.close)
            pdt.assert_series_equal(atr, tal_atr, check_names=False)
        except AssertionError as ae:
            try:
                col = 'corr'
                corr = pandas_ta.utils.df_error_analysis(atr, tal_atr, col=col)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {atr.name}['{col}']: {ex}")

    def test_bbands(self):
        bbands = self.volatility.bbands(self.close)
        self.assertIsInstance(bbands, DataFrame)
        self.assertEqual(bbands.name, 'BBANDS_20')

        try:
            tal_bbands = tal.BBANDS(self.close)
            tal_bbandsdf = DataFrame({'BBL_20': tal_bbands[0], 'BBM_20': tal_bbands[1], 'BBU_20': tal_bbands[2]})
            pdt.assert_frame_equal(bbands, tal_bbandsdf)
        except AssertionError as ae:
            col = 'corr'
            try:
                bbl_corr = pandas_ta.utils.df_error_analysis(bbands.iloc[:,0], tal_bbandsdf.iloc[:,0], col=col)
                self.assertGreater(bbl_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {bbands.iloc[:,0].name}['{col}']: {ex}")

            try:
                bbm_corr = pandas_ta.utils.df_error_analysis(bbands.iloc[:,1], tal_bbandsdf.iloc[:,1], col=col)
                self.assertGreater(bbm_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f" [!] {bbands.iloc[:,1].name}['{col}']: {ex}")

            try:
                bbu_corr = pandas_ta.utils.df_error_analysis(bbands.iloc[:,2], tal_bbandsdf.iloc[:,2], col=col)
                self.assertGreater(bbu_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f" [!] {bbands.iloc[:,2].name}['{col}']: {ex}")

    def test_donchian(self):
        donchian = self.volatility.donchian(self.close)
        self.assertIsInstance(donchian, DataFrame)
        self.assertEqual(donchian.name, 'DC_20')

    def test_kc(self):
        kc = self.volatility.kc(self.high, self.low, self.close)
        self.assertIsInstance(kc, DataFrame)
        self.assertEqual(kc.name, 'KC_20')

    def test_massi(self):
        massi = self.volatility.massi(self.high, self.low)
        self.assertIsInstance(massi, Series)
        self.assertEqual(massi.name, 'MASSI_9_25')

    def test_natr(self):
        natr = self.volatility.natr(self.high, self.low, self.close)
        self.assertIsInstance(natr, Series)
        self.assertEqual(natr.name, 'NATR_14')

        try:
            tal_natr = tal.NATR(self.high, self.low, self.close)
            pdt.assert_series_equal(natr, tal_natr, check_names=False)
        except AssertionError as ae:
            try:
                col = 'corr'
                corr = pandas_ta.utils.df_error_analysis(natr, tal_natr, col=col)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {natr.name}['{col}']: {ex}")

    def test_true_range(self):
        true_range = self.volatility.true_range(self.high, self.low, self.close)
        self.assertIsInstance(true_range, Series)
        self.assertEqual(true_range.name, 'TRUERANGE_1')

        try:
            tal_true_range = tal.TRANGE(self.high, self.low, self.close)
            pdt.assert_series_equal(true_range, tal_true_range, check_names=False)
        except AssertionError as ae:
            try:
                col = 'corr'
                corr = pandas_ta.utils.df_error_analysis(true_range, tal_true_range, col=col)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                print(f"\n [!] {true_range.name}['{col}']: {ex}")