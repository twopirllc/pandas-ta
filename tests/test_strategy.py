# Must run seperately from the rest of the tests
# in order to successfully run
from time import perf_counter

from .config import sample_data
from .context import pandas_ta

from unittest import skip, TestCase
from pandas import DataFrame

from pandas_ta.utils import final_time

_verbose = False
_timed = True
speed_table = False

class TestStrategyMethods(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.speed_test = DataFrame()

    @classmethod
    def tearDownClass(cls):
        del cls.data
        cls.speed_test = cls.speed_test.T
        cls.speed_test.index.name = "Test"
        cls.speed_test.columns = ["secs"]
        cls.speed_test["Cumsecs"] = cls.speed_test["secs"].cumsum()
        if speed_table: cls.speed_test.to_csv("tests/speed_test.csv")
        print(cls.speed_test)


    def setUp(self): pass
    def tearDown(self): pass


    def test_all(self):
        if _verbose: print()
        category = "All"
        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

        self.speed_test[category] = [time_diff]

    def test_all_strategy(self):
        if _verbose: print()
        init_cols = len(self.data.columns)
        self.data.ta.strategy(pandas_ta.AllStrategy, verbose=_verbose)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

    def test_all_name_strategy(self):
        if _verbose: print()
        init_cols = len(self.data.columns)
        self.data.ta.strategy("All", verbose=_verbose)
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

    def test_candles_category(self):
        if _verbose: print()
        category = "Candles"
        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(category, verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

        self.speed_test[category] = [time_diff]

    def test_common(self):
        if _verbose: print()
        category = "Common"
        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(pandas_ta.CommonStrategy, verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

    def test_custom_a(self):
        if _verbose: print()
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

        category = "Custom A"

        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(custom, verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols
        self.assertEqual(added_cols, 11)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

        self.speed_test[category] = [time_diff]

    def test_custom_args_tuple(self):
        if _verbose: print()
        custom_args_ta = [
            {"kind":"fisher", "params": (13, 7)},
            {"kind":"macd", "params": (9, 19, 7)},
            {"kind":"ema", "params": (5,)},
            {"kind":"linreg", "close": "EMA_5", "length": 8, "prefix": "EMA_5"}
        ]

        custom = pandas_ta.Strategy(
            "Custom Args Tuple", custom_args_ta,
            "Allow for easy filling in indicator arguments without naming them"
        )

        category = "Custom B"

        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(custom, verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

        self.speed_test[category] = [time_diff]

    def test_momentum_category(self):
        if _verbose: print()
        category = "Momentum"
        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(category, verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

        self.speed_test[category] = [time_diff]

    def test_overlap_category(self):
        if _verbose: print()
        category = "Overlap"
        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(category, verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

        self.speed_test[category] = [time_diff]

    def test_performance_category(self):
        if _verbose: print()
        category = "Performance"
        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(category, verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

        self.speed_test[category] = [time_diff]

    def test_statistics_category(self):
        if _verbose: print()
        category = "Statistics"
        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(category, verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

        self.speed_test[category] = [time_diff]

    def test_trend_category(self):
        if _verbose: print()
        category = "Trend"
        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(category, verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

        self.speed_test[category] = [time_diff]

    def test_volatility_category(self):
        if _verbose: print()
        category = "Volatility"
        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(category, verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

        self.speed_test[category] = [time_diff]

    def test_volume_category(self):
        if _verbose: print()
        category = "Volume"
        init_cols = len(self.data.columns)
        if _timed: stime = perf_counter()
        self.data.ta.strategy(category, verbose=_verbose)
        if _timed: time_diff = perf_counter() - stime
        added_cols = len(self.data.columns) - init_cols
        self.assertGreaterEqual(added_cols, 1)

        result = self.data[self.data.columns[-added_cols:]]
        self.assertIsInstance(result, DataFrame)
        self.data.drop(columns=result.columns, axis=1, inplace=True)

        self.speed_test[category] = [time_diff]