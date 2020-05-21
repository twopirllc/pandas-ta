from .config import sample_data
from .context import pandas_ta

from unittest import TestCase
from pandas import DataFrame



class TestVolatilityExtension(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data

    @classmethod
    def tearDownClass(cls):
        del cls.data


    def setUp(self): pass
    def tearDown(self): pass


    def test_aberration_ext(self):
        self.data.ta.aberration(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-4:]), ['ABER_ZG_5_15', 'ABER_SG_5_15', 'ABER_XG_5_15', 'ABER_ATR_5_15'])

    def test_accbands_ext(self):
        self.data.ta.accbands(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-3:]), ['ACCBL_20', 'ACCBM_20', 'ACCBU_20'])

    def test_atr_ext(self):
        self.data.ta.atr(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'ATR_14')

    def test_bbands_ext(self):
        self.data.ta.bbands(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-3:]), ['BBL_5', 'BBM_5', 'BBU_5'])

    def test_donchian_ext(self):
        self.data.ta.donchian(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-3:]), ['DCL_10_20', 'DCM_10_20', 'DCU_10_20'])

    def test_kc_ext(self):
        self.data.ta.kc(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-3:]), ['KCL_20', 'KCB_20', 'KCU_20'])

    def test_massi_ext(self):
        self.data.ta.massi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'MASSI_9_25')

    def test_natr_ext(self):
        self.data.ta.natr(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'NATR_14')

    def test_pdist_ext(self):
        self.data.ta.pdist(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'PDIST')

    def test_true_range_ext(self):
        self.data.ta.true_range(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'TRUERANGE_1')