# -*- coding: utf-8 -*-
from unittest import TestCase, skip
from pandas import Series

from .config import sample_data
from .context import pandas_ta


class TestCycles(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.data.columns = cls.data.columns.str.lower()
        cls.open = cls.data["open"]
        cls.high = cls.data["high"]
        cls.low = cls.data["low"]
        cls.close = cls.data["close"]
        if "volume" in cls.data.columns:
            cls.volume = cls.data["volume"]

    @classmethod
    def tearDownClass(cls):
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        if hasattr(cls, "volume"):
            del cls.volume
        del cls.data

    def setUp(self): pass
    def tearDown(self): pass


    def test_ebsw(self):
        """Cycle: EBSW"""
        result = pandas_ta.ebsw(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "EBSW_40_10")


    def test_reflex(self):
        """Cycle: Reflex"""
        result = pandas_ta.reflex(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "REFLEX_20_20_0.04")
