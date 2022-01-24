# -*- coding: utf-8 -*-
from unittest import TestCase
from pandas import DataFrame

from .config import sample_data


class TestCylesExtension(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data

    @classmethod
    def tearDownClass(cls):
        del cls.data

    def setUp(self): pass
    def tearDown(self): pass


    def test_ebsw_ext(self):
        self.data.ta.ebsw(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "EBSW_40_10")

    def test_reflex_ext(self):
        self.data.ta.reflex(append=True)
        self.assertIsInstance(self.data, DataFrame)
        self.assertEqual(self.data.columns[-1], "REFLEX_20_20_0.04")
