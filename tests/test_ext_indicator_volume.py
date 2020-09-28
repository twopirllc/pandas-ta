from .config import sample_data
from .context import pandas_ta

from unittest import TestCase
from pandas import DataFrame



class TestVolumeExtension(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.open = cls.data["open"]

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.open

    def setUp(self): pass
    def tearDown(self): pass


    def test_ad_ext(self):
        self.data.ta.ad(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "AD")

    def test_ad_open_ext(self):
        self.data.ta.ad(open_=self.open, append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "ADo")

    def test_adosc_ext(self):
        self.data.ta.adosc(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "ADOSC_3_10")

    def test_aobv_ext(self):
        self.data.ta.aobv(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-7:]), ["OBV", "OBV_min_2", "OBV_max_2", "OBV_EMA_4", "OBV_EMA_12", "AOBV_LR_2", "AOBV_SR_2"])
        # Remove "OBV" so it does not interfere with test_obv_ext()
        self.data.drop("OBV", axis=1, inplace=True)

    def test_cmf_ext(self):
        self.data.ta.cmf(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "CMF_20")

    def test_efi_ext(self):
        self.data.ta.efi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "EFI_13")

    def test_eom_ext(self):
        self.data.ta.eom(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "EOM_14_100000000")

    def test_mfi_ext(self):
        self.data.ta.mfi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "MFI_14")

    def test_nvi_ext(self):
        self.data.ta.nvi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "NVI_1")
        # print(f"\nNVI: {self.data.columns[-1]}")
        # print(f"NVI: {self.data.columns}")

    def test_obv_ext(self):
        self.data.ta.obv(append=True)
        self.assertIsInstance(self.data, DataFrame)
        # print(f"\nOBV: {self.data.columns[-1]}")
        # print(f"OBV: {self.data.columns}")
        self.assertEqual(self.data.columns[-1], "OBV")

    def test_pvi_ext(self):
        self.data.ta.pvi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "PVI_1")

    def test_pvol_ext(self):
        self.data.ta.pvol(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "PVOL")

    def test_pvt_ext(self):
        self.data.ta.pvt(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "PVT")

    def test_vp_ext(self):
        result = self.data.ta.vp()
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "VP_10")