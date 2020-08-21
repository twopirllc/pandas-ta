from .config import sample_data
from .context import pandas_ta

from unittest import skip, TestCase
from pandas import DataFrame

# Must run seperately from the rest of the tests
# in order to successfully run

class TestStrategyMethods(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data

    @classmethod
    def tearDownClass(cls):
        del cls.data


    def setUp(self): pass
    def tearDown(self): pass

    
    def test_all(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy(verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_all_strategy(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy(pandas_ta.AllStrategy, verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_all_name_strategy(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy("All", verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_candles_category(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy("Candles", verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_common(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy(pandas_ta.CommonStrategy, verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_custom_a(self):
        momo_bands_sma_ta = [
            {"kind":"sma", "length": 50}, # 1
            {"kind":"sma", "length": 200}, # 1
            {"kind":"bbands", "length": 20}, # 3
            {"kind":"macd"}, # 3
            {"kind":"rsi"}, # 1
            {"kind":"log_return", "cumulative": True}, # 1
            {"kind":"sma", "close": "CUMLOGRET_1", "length": 5, "suffix": "CUMLOGRET"}, # 1
        ]
        custom = pandas_ta.Strategy(
            "Momo, Bands and SMAs and Cumulative Log Returns", # name
            momo_bands_sma_ta, # ta
            "MACD and RSI Momo with BBANDS and SMAs 50 & 200 and Cumulative Log Returns" # description
        )

        init_cols = len(self.data.columns)
        self.data.ta.strategy(custom, verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertEqual(added_cols, 11)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_momentum_category(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy("Momentum", verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_overlap_category(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy("Overlap", verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_performance_category(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy("Performance", verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_statistics_category(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy("Statistics", verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_trend_category(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy("Trend", verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_volatility_category(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy("Volatility", verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)
    
    def test_volume_category(self):
        init_cols = len(self.data.columns)
        self.data.ta.strategy("Volume", verbose=False)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)