from .config import sample_data
from .context import pandas_ta

from unittest import skip, TestCase
from pandas import DataFrame


class TestStatisticsExtension(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data

    @classmethod
    def tearDownClass(cls):
        del cls.data

    def setUp(self): pass
    def tearDown(self): pass


    def test_entropy_ext(self):
        self.data.ta.entropy(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "ENTP_10")

    def test_kurtosis_ext(self):
        self.data.ta.kurtosis(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "KURT_30")

    def test_mad_ext(self):
        self.data.ta.mad(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "MAD_30")

    def test_median_ext(self):
        self.data.ta.median(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "MEDIAN_30")

    def test_quantile_ext(self):
        self.data.ta.quantile(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "QTL_30_0.5")

    def test_skew_ext(self):
        self.data.ta.skew(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "SKEW_30")

    def test_stdev_ext(self):
        self.data.ta.stdev(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "STDEV_30")

    @skip
    def test_tos_stdevall_ext(self):
        self.data.ta.tos_stdevall(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-7:]), [
            "STDEVALL_LR",
            "STDEVALL_L_1", "STDEVALL_U_1",
            "STDEVALL_L_2", "STDEVALL_U_2",
            "STDEVALL_L_3", "STDEVALL_U_3"
        ])

    def test_variance_ext(self):
        self.data.ta.variance(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "VAR_30")
