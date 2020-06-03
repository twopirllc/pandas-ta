from .config import sample_data
from .context import pandas_ta

from unittest import TestCase
from pandas import DataFrame



class TestMomentumExtension(TestCase):
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


    def test_ao_ext(self):
        self.data.ta.ao(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'AO_5_34')

    def test_apo_ext(self):
        self.data.ta.apo(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'APO_12_26')

    def test_bias_ext(self):
        self.data.ta.bias(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'BIAS_SMA_26')

    def test_bop_ext(self):
        self.data.ta.bop(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'BOP')

    def test_brar_ext(self):
        self.data.ta.brar(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-2:]), ['AR_26', 'BR_26'])

    def test_cci_ext(self):
        self.data.ta.cci(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'CCI_14_0.015')

    def test_cg_ext(self):
        self.data.ta.cg(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'CG_10')

    def test_cmo_ext(self):
        self.data.ta.cmo(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'CMO_14')

    def test_coppock_ext(self):
        self.data.ta.coppock(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'COPC_11_14_10')

    def test_fisher_ext(self):
        self.data.ta.fisher(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'FISHERT_5')

    def test_inertia_ext(self):
        self.data.ta.inertia(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'INERTIA_14_4')

    def test_kdj_ext(self):
        self.data.ta.kdj(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-3:]), ['K_9_3', 'D_9_3', 'J_9_3'])

    def test_kst_ext(self):
        self.data.ta.kst(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-2:]), ['KST_10_15_20_30_10_10_10_15', 'KSTs_9'])

    def test_macd_ext(self):
        self.data.ta.macd(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-3:]), ['MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9'])

    def test_mom_ext(self):
        self.data.ta.mom(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'MOM_10')

    def test_ppo_ext(self):
        self.data.ta.ppo(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-3:]), ['PPO_12_26_9', 'PPOh_12_26_9', 'PPOs_12_26_9'])

    def test_psl_ext(self):
        self.data.ta.psl(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'PSL_12')

    def test_pvo_ext(self):
        self.data.ta.pvo(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-3:]), ['PVO_12_26_9', 'PVOh_12_26_9', 'PVOs_12_26_9'])

    def test_roc_ext(self):
        self.data.ta.roc(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'ROC_10')

    def test_rsi_ext(self):
        self.data.ta.rsi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'RSI_14')

    def test_rvi_ext(self):
        self.data.ta.rvi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-2:]), ['RVI_14_4', 'RVIs_14_4'])

    def test_slope_ext(self):
        self.data.ta.slope(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'SLOPE_1')

        self.data.ta.slope(append=True, as_angle=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'ANGLEr_1')

        self.data.ta.slope(append=True, as_angle=True, to_degrees=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'ANGLEd_1')

    def test_stoch_ext(self):
        self.data.ta.stoch(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-4:]), ['STOCHFk_14', 'STOCHFd_3', 'STOCHk_5', 'STOCHd_3'])

    def test_trix_ext(self):
        self.data.ta.trix(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-2:]), ['TRIX_30_9', 'TRIXs_30_9'])

    def test_tsi_ext(self):
        self.data.ta.tsi(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'TSI_13_25')

    def test_uo_ext(self):
        self.data.ta.uo(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'UO_7_14_28')

    def test_willr_ext(self):
        self.data.ta.willr(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'WILLR_14')
