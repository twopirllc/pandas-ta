from .config import sample_data
from .context import pandas_ta

from unittest import skip, TestCase
from pandas import DataFrame



class TestTrendExtension(TestCase):
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


    def test_adx_ext(self):
        self.data.ta.adx(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-3:]), ['ADX_14', 'DMP_14', 'DMN_14'])

    def test_amat_ext(self):
        self.data.ta.amat(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-2:]), ['AMAT_LR_2', 'AMAT_SR_2'])

    def test_aroon_ext(self):
        self.data.ta.aroon(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-2:]), ['AROOND_14', 'AROONU_14'])

    def test_decreasing_ext(self):
        self.data.ta.decreasing(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'DEC_1')

    def test_dpo_ext(self):
        self.data.ta.dpo(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'DPO_1')

    def test_increasing_ext(self):
        self.data.ta.increasing(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'INC_1')

    def test_long_run_ext(self):
        # Nothing passed, return self
        self.assertEqual(self.data.ta.long_run(append=True).shape, self.data.shape)

        fast = self.data.ta.ema('close', 8)
        slow = self.data.ta.ema('close', 21)
        self.data.ta.long_run(fast, slow, append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'LR_2')

    def test_qstick_ext(self):
        self.data.ta.qstick(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'QS_10')

    def test_short_run_ext(self):
        # Nothing passed, return self
        self.assertEqual(self.data.ta.short_run(append=True).shape, self.data.shape)

        fast = self.data.ta.ema('close', 8)
        slow = self.data.ta.ema('close', 21)
        self.data.ta.short_run(fast, slow, append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], 'SR_2')

    def test_vortext_ext(self):
        self.data.ta.vortex(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-2:]), ['VTXP_14', 'VTXM_14'])
