# -*- coding: utf-8 -*-
from unittest import TestCase
from pandas import DataFrame

from .config import sample_data
from .context import pandas_ta


class TestPerformaceExtension(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.islong = cls.data["close"] > pandas_ta.sma(cls.data["close"], length=50)

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.islong

    def setUp(self): pass
    def tearDown(self): pass


    def test_cube_ext(self):
        self.data.ta.cube(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-2:]), ["CUBE_3.0_1", "CUBEs_3.0_1"])

    def test_inverse_fisher_ext(self):
        self.data.ta.ifisher(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(list(self.data.columns[-2:]), ["INVFISHER_1.0", "INVFISHERs_1.0"])

    def test_remap_ext(self):
        self.data.ta.remap(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "REMAP_0.0_100.0_-1.0_1.0")