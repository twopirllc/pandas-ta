from .config import sample_data
from .context import pandas_ta

from unittest import skip, TestCase
from unittest.mock import patch

# import numpy as np
# import numpy.testing as npt
# from pandas import DataFrame, Series

class TestUtilityMetrics(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data

    @classmethod
    def tearDownClass(cls):
        del cls.data

    def setUp(self):
        self.utils = pandas_ta.utils

    def tearDown(self):
        del self.utils

    def test_cagr(self):
        result = pandas_ta.utils.cagr(self.data.close)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)