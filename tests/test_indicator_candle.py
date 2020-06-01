from .config import error_analysis, sample_data, CORRELATION, CORRELATION_THRESHOLD, VERBOSE
from .context import pandas_ta

from unittest import TestCase, skip
import pandas.testing as pdt
from pandas import DataFrame, Series

import talib as tal



class TestCandle(TestCase):
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


    def test_ha(self):
        result = pandas_ta.ha(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "Heikin-Ashi")