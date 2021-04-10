from .config import sample_data
from .context import pandas_ta

from unittest import TestCase
from pandas import DataFrame


class TestPerformaceExtension(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.islong = cls.data["close"] > pandas_ta.sma(cls.data["close"], length=50)

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.islong

    def setUp(self): pass
    def tearDown(self): pass


    def test_log_return_ext(self):
        self.data.ta.log_return(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "LOGRET_1")

    def test_cum_log_return_ext(self):
        self.data.ta.log_return(append=True, cumulative=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "CUMLOGRET_1")

    def test_percent_return_ext(self):
        self.data.ta.percent_return(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "PCTRET_1")

    def test_cum_percent_return_ext(self):
        self.data.ta.percent_return(append=True, cumulative=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "CUMPCTRET_1")

    def test_log_trend_return_ext(self):
        tr = self.data.ta.trend_return(trend=self.islong, log=True, append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-6:]), list(tr.columns))
        self.data.drop(columns=tr.columns, inplace=True, errors="ignore")

    def test_pct_trend_return_ext(self):
        tr = self.data.ta.trend_return(trend=self.islong, log=False, append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-6:]), list(tr.columns))
        self.data.drop(columns=tr.columns, inplace=True, errors="ignore")