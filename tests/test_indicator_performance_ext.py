from .config import sample_data
from .context import pandas_ta

from unittest import TestCase
# import numpy.testing as npt
# import pandas.util.testing as pdt
from pandas import DataFrame#, Series



class TestPerformaceExtension(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data

    @classmethod
    def tearDownClass(cls):
        del cls.data


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