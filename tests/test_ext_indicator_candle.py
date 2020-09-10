from .config import sample_data
from .context import pandas_ta

from unittest import TestCase
from pandas import DataFrame



class TestCandleExtension(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data

    @classmethod
    def tearDownClass(cls):
        del cls.data

    def setUp(self): pass
    def tearDown(self): pass


    def test_cdl_doji_ext(self):
        self.data.ta.cdl_doji(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "CDL_DOJI_10_0.1")

    def test_cdl_inside_ext(self):
        self.data.ta.cdl_inside(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "CDL_INSIDE")

    def test_ha_ext(self):
        self.data.ta.ha(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-4:]), ["HA_open", "HA_high", "HA_low", "HA_close"])