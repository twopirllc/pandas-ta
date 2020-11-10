from .config import sample_data
from .context import pandas_ta

from unittest import skip, TestCase
from pandas import DataFrame


class TestOverlapExtension(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data

    @classmethod
    def tearDownClass(cls):
        del cls.data

    def setUp(self): pass
    def tearDown(self): pass


    def test_dema_ext(self):
        self.data.ta.dema(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "DEMA_10")

    def test_ema_ext(self):
        self.data.ta.ema(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "EMA_10")

    def test_fwma_ext(self):
        self.data.ta.fwma(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "FWMA_10")

    def test_hilo_ext(self):
        self.data.ta.hilo(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-3:]), ["HILO_13_21", "HILOl_13_21", "HILOs_13_21"])

    def test_hl2_ext(self):
        self.data.ta.hl2(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "HL2")

    def test_hlc3_ext(self):
        self.data.ta.hlc3(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "HLC3")

    def test_hma_ext(self):
        self.data.ta.hma(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "HMA_10")

    def test_kama_ext(self):
        self.data.ta.kama(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "KAMA_10_2_30")

    def test_ichimoku_ext(self):
        self.data.ta.ichimoku(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-5:]), ["ISA_9", "ISB_26", "ITS_9", "IKS_26", "ICS_26"])

    def test_linreg_ext(self):
        self.data.ta.linreg(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "LR_14")

    def test_midpoint_ext(self):
        self.data.ta.midpoint(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "MIDPOINT_2")

    def test_midprice_ext(self):
        self.data.ta.midprice(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "MIDPRICE_2")

    def test_ohlc4_ext(self):
        self.data.ta.ohlc4(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "OHLC4")

    def test_pwma_ext(self):
        self.data.ta.pwma(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "PWMA_10")

    def test_rma_ext(self):
        self.data.ta.rma(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "RMA_10")

    def test_sinwma_ext(self):
        self.data.ta.sinwma(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "SINWMA_14")

    def test_sma_ext(self):
        self.data.ta.sma(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "SMA_10")

    def test_ssf_ext(self):
        self.data.ta.ssf(append=True, poles=2)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "SSF_10_2")

        self.data.ta.ssf(append=True, poles=3)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "SSF_10_3")

    def test_swma_ext(self):
        self.data.ta.swma(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "SWMA_10")

    def test_supertrend_ext(self):
        self.data.ta.supertrend(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-4:]), ["SUPERT_7_3.0", "SUPERTd_7_3.0", "SUPERTl_7_3.0", "SUPERTs_7_3.0"])

    def test_t3_ext(self):
        self.data.ta.t3(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "T3_10_0.7")

    def test_tema_ext(self):
        self.data.ta.tema(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "TEMA_10")

    def test_trima_ext(self):
        self.data.ta.trima(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "TRIMA_10")

    def test_vwap_ext(self):
        self.data.ta.vwap(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "VWAP")

    def test_vwma_ext(self):
        self.data.ta.vwma(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "VWMA_10")

    def test_wcp_ext(self):
        self.data.ta.wcp(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "WCP")

    def test_wma_ext(self):
        self.data.ta.wma(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "WMA_10")

    def test_zlma_ext(self):
        self.data.ta.zlma(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "ZL_EMA_10")
