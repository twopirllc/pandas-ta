from .context import pandas_ta
from .data import sample_data

from unittest import TestCase
from pandas import DataFrame



class TestVolatilityExtension(TestCase):
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


    def test_accbands_ext(self):
        self.data.ta.accbands(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-3], 'ACCBL_10')
        self.assertEqual(self.data.columns[-2], 'ACCBM_10')
        self.assertEqual(self.data.columns[-1], 'ACCBU_10')

    def test_atr_ext(self):
        self.data.ta.atr(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'ATR_14')

    def test_bbands_ext(self):
        self.data.ta.bbands(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-3], 'BBL_20')
        self.assertEqual(self.data.columns[-2], 'BBM_20')
        self.assertEqual(self.data.columns[-1], 'BBU_20')

    def test_donchian_ext(self):
        self.data.ta.donchian(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-3], 'DCL_20')
        self.assertEqual(self.data.columns[-2], 'DCM_20')
        self.assertEqual(self.data.columns[-1], 'DCU_20')

    def test_kc_ext(self):
        self.data.ta.kc(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-3], 'KCL_20')
        self.assertEqual(self.data.columns[-2], 'KCB_20')
        self.assertEqual(self.data.columns[-1], 'KCU_20')

    def test_massi_ext(self):
        self.data.ta.massi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'MASSI_9_25')

    def test_natr_ext(self):
        self.data.ta.natr(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'NATR_14')

    def test_true_range_ext(self):
        self.data.ta.true_range(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'TRUERANGE_1')