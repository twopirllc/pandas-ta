from .config import sample_data
from .context import pandas_ta

from unittest import TestCase
from pandas import Series



class TestPerformace(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.close = cls.data['close']

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.close


    def setUp(self):
        self.performance = pandas_ta.performance

    def tearDown(self):
        del self.performance


    def test_log_return(self):
        result = self.performance.log_return(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'LOGRET_1')

    def test_cum_log_return(self):
        result = self.performance.log_return(self.close, cumulative=True)
        self.assertEqual(result.name, 'CUMLOGRET_1')

    def test_percent_return(self):
        result = self.performance.percent_return(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, 'PCTRET_1')

    def test_cum_percent_return(self):
        result = self.performance.percent_return(self.close, cumulative=True)
        self.assertEqual(result.name, 'CUMPCTRET_1')