from .context import pandas_ta
from .data import sample_data, CORRELATION_THRESHOLD

from unittest import TestCase, skip
import pandas.util.testing as pdt
from pandas import DataFrame, Series

import talib as tal

VERBOSE = False


class TestVolatility(TestCase):
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

    def test_bbands(self):
        bbands = self.volatility.bbands(self.close)
        self.assertIsInstance(bbands, DataFrame)
        self.assertEqual(bbands.name, 'BBANDS_20')

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

    def test_true_range(self):
        true_range = self.volatility.true_range(self.high, self.low, self.close)
        self.assertIsInstance(true_range, Series)
        self.assertEqual(true_range.name, 'TRUERANGE_1')
