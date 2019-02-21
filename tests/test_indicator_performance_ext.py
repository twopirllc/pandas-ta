from unittest import TestCase
import numpy.testing as npt
import pandas.util.testing as pdt
from pandas import DataFrame, read_csv, Series

import pandas_ta as ta


class TestPerformaceExtension(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = read_csv('data/sample.csv', index_col=0, parse_dates=True, infer_datetime_format=False, keep_date_col=True)
        cls.close = cls.data['close']

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.close


    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_log_return_ext(self):
        self.data.ta.log_return(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'LOGRET_1')

        self.data.ta.log_return(append=True, cumulative=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'CUMLOGRET_1')

    def test_percent_return_ext(self):
        self.data.ta.percent_return(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'PCTRET_1')

        self.data.ta.percent_return(append=True, cumulative=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'CUMPCTRET_1')

        # Example
        # pta_sma = self.data[self.data.columns[-1]]
        # tal_sma = tal.SMA(self.close)        
        # pdt.assert_series_equal(pta_sma, tal_sma)