from .context import pandas_ta
from .data import sample_data

from unittest import skip, TestCase
from pandas import DataFrame



class TestVolumeExtension(TestCase):
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


    def test_ad_ext(self):
        self.data.ta.ad(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'AD')

    def test_adosc_ext(self):
        self.data.ta.adosc(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'ADOSC_12_26')

    def test_cmf_ext(self):
        self.data.ta.cmf(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'CMF_20')

    def test_efi_ext(self):
        self.data.ta.efi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'EFI_13')

    def test_eom_ext(self):
        self.data.ta.eom(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'EOM_14_100000000')

    def test_mfi_ext(self):
        self.data.ta.mfi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'MFI_14')

    def test_nvi_ext(self):
        self.data.ta.nvi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'NVI_1')

    def test_obv_ext(self):
        self.data.ta.obv(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'OBV')

    def test_pvol_ext(self):
        self.data.ta.pvol(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'PVOL')

    def test_pvt_ext(self):
        self.data.ta.pvt(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'PVT')

    @skip('Standalone and does not need to be added to the DataFrame')
    def test_vp_ext(self):
        pass