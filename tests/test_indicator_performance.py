from unittest import TestCase
import numpy.testing as npt
import pandas.util.testing as pdt
from pandas import DataFrame, read_csv, Series

from pandas_ta import performance


class TestPerformace(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = read_csv('data/sample.csv', index_col=0, parse_dates=True, infer_datetime_format=False, keep_date_col=True)
        cls.close = cls.data['close']

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.close


    def setUp(self):
        self.performance = performance

    def tearDown(self):
        del self.performance


    def test_log_return(self):
        log_return = self.performance.log_return(self.close)
        self.assertIsInstance(log_return, Series)
        self.assertEqual(log_return.name, 'LOGRET_1')

        cumlog_return = self.performance.log_return(self.close, cumulative=True)
        self.assertEqual(cumlog_return.name, 'CUMLOGRET_1')

    def test_percent_return(self):
        percent_return = self.performance.percent_return(self.close)
        self.assertIsInstance(percent_return, Series)
        self.assertEqual(percent_return.name, 'PCTRET_1')

        cumpercent_return = self.performance.percent_return(self.close, cumulative=True)
        self.assertEqual(cumpercent_return.name, 'CUMPCTRET_1')

