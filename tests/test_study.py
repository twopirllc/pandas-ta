# -*- coding: utf-8 -*-
# Must run seperately from the rest of the tests
# in order to successfully run
from multiprocessing import cpu_count
from time import perf_counter
from unittest import TestCase, skip, skipUnless
from pandas import DataFrame

from .config import sample_data, VERBOSE
from .context import pandas_ta


# Testing Parameters
cores = cpu_count() - 2 if cpu_count() > 3 else 0
cumulative = False
speed_table = False
timed_test = False
timed = True
verbose = VERBOSE


class TestStudyMethods(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.data.ta.cores = cores
        cls.speed_test = DataFrame()

    @classmethod
    def tearDownClass(cls):
        cls.speed_test = cls.speed_test.T
        cls.speed_test.index.name = "Test"
        cls.speed_test.columns = ["Columns", "Seconds"]
        if cumulative:
            cls.speed_test["Cum. Seconds"] = cls.speed_test["Seconds"].cumsum()
        if speed_table:
            cls.speed_test.to_csv("tests/speed_test.csv")
        if timed:
            tca = cls.speed_test['Columns'].sum()
            tcs = cls.speed_test['Seconds'].sum()
            cps = f"[i] Total Columns / Second for All Tests: { tca / tcs:.5f} "
            _div = "===" + "=" * len(cps)
            print(_div)
            print(cls.speed_test)
            print(f"[i] Cores: {cls.data.ta.cores}")
            print(f"[i] Total Datapoints per run: {cls.data.shape[0]}")
            print(f"[i] Total Columns added: {tca}")
            print(f"[i] Total Seconds for All Tests: {tcs:.5f}")
            print(cps)
            print(_div)
            # tmp = concat([cls.speed_test, cls.speed_test["Columns"].sum(), cls.speed_test["Seconds"].sum()])
            # print(tmp)
        del cls.data

    def setUp(self):
        self.added_cols = 0
        self.category = ""
        self.init_cols = len(self.data.columns)
        self.time_diff = 0
        self.result = None
        if verbose: print()
        if timed: self.stime = perf_counter()

    def tearDown(self):
        if timed:
            self.time_diff = perf_counter() - self.stime
        self.added_cols = len(self.data.columns) - self.init_cols

        if self.added_cols > 0:
            self.result = self.data[self.data.columns[-self.added_cols:]]
            self.assertIsInstance(self.result, DataFrame)
            self.data.drop(columns=self.result.columns, axis=1, inplace=True)

        self.speed_test[self.category] = [self.added_cols, self.time_diff]

    # @skip
    def test_all(self):
        """Study: All with TA Lib"""
        self.category = "All"
        self.data.ta.study(verbose=verbose, timed=timed_test)
        self.category = "All: TA Lib"

    def test_all_no_talib(self):
        """Study: All Sans TA Lib"""
        self.category = "All"
        self.data.ta.study(talib=False, verbose=verbose, timed=timed_test)
        self.category = "All: Sans TA Lib"

    # @skipUnless(verbose, "verbose mode only")
    def test_all_multiparams_study(self):
        """Study: All with Multiparameters"""
        self.category = "All"
        self.data.ta.study(self.category, length=10, verbose=verbose, timed=timed_test)
        self.data.ta.study(self.category, length=50, verbose=verbose, timed=timed_test)
        self.data.ta.study(self.category, fast=5, slow=10, verbose=verbose, timed=timed_test)
        self.category = "All: Multiruns with Multiparameters" # Rename for Speed Table

    @skipUnless(verbose, "verbose mode only")
    def test_all_name_study(self):
        self.category = "All"
        self.data.ta.study(self.category, verbose=verbose, timed=timed_test)

    def test_all_ordered(self):
        """Study: All Ordered"""
        self.category = "All"
        self.data.ta.study(ordered=True, verbose=verbose, timed=timed_test)
        self.category = "All: Ordered" # Rename for Speed Table

    @skipUnless(verbose, "verbose mode only")
    def test_all_study(self):
        """Study: All"""
        self.category = "Candles"
        self.data.ta.study(pandas_ta.AllStudy, verbose=verbose, timed=timed_test)

    @skipUnless(verbose, "verbose mode only")
    def test_all_without_append(self):
        """Study: All sans append"""
        self.category = "All: Sans append"
        self.data.ta.study(append=False, verbose=verbose, timed=timed_test)

    # @skip
    def test_candles_category(self):
        """Candles"""
        self.category = "Candles"
        self.data.ta.study(self.category, verbose=verbose, timed=timed_test)

    # @skip
    def test_common(self):
        """Study: Common"""
        self.category = "Common"
        self.data.ta.study(pandas_ta.CommonStudy, verbose=verbose, timed=timed_test)

    def test_cycles_category(self):
        """Cycles"""
        self.category = "Cycles"
        self.data.ta.study(self.category, verbose=verbose, timed=timed_test)

    # @skip
    def test_custom_a_with_multiprocessing(self):
        """Custom A: Multiprocessing"""
        self.category = "Custom A: Multiprocessing"

        cta = [
            {"kind": "cdl_pattern", "name": "tristar"},  # 1
            {"kind": "rsi"},  # 1
            {"kind": "macd"},  # 3
            {"kind": "sma", "length": 50},  # 1
            {"kind": "trix"},  # 2
            {"kind": "bbands", "length": 20},  # 5
            {"kind": "log_return", "cumulative": True},  # 1
            {"kind": "ema", "close": "CUMLOGRET_1", "length": 5, "suffix": "CLR"} # 1
        ]
        custom = pandas_ta.Study(
            name="Commons with Cumulative Log Return EMA Chain",  # name
            ta=cta,  # ta
            description="Common indicators with specific lengths and a chained indicator",  # description
            cores=cores
        )
        self.data.ta.study(custom, verbose=verbose, timed=timed_test)
        self.assertEqual(len(self.data.columns), 22)

    # @skipUnless(verbose, "verbose mode only")
    def test_custom_a_without_multiprocessing(self):
        """Custom A: Sans Multiprocessing"""
        self.category = "Custom A: Sans Multiprocessing"
        _cores = self.data.ta.cores

        momo_bands_sma_ta = [
            {"kind": "rsi"},  # 1
            {"kind": "macd"},  # 3
            {"kind": "sma", "length": 50},  # 1
            {"kind": "sma", "length": 100, "col_names": "sma100"},  # 1
            {"kind": "sma", "length": 200 },  # 1
            {"kind": "bbands", "length": 20},  # 5
            {"kind": "log_return", "cumulative": True},  # 1
            {"kind": "ema", "close": "CUMLOGRET_1", "length": 5, "suffix": "CLR"} # 1
        ]

        custom = pandas_ta.Study(
            name="Commons with Cumulative Log Return EMA Chain",  # name
            ta=momo_bands_sma_ta,  # ta
            description="Common indicators with specific lengths and a chained indicator",  # description
            cores=0
        )
        # Depreciation warning test
        self.data.ta.strategy(custom, cores=0, verbose=verbose, timed=timed_test)
        self.data.ta.cores = cores

    # @skip
    def test_custom_args_tuple(self):
        """Custom B: Tuple Arguments"""
        self.category = "Custom B: Tuple Arguments"

        custom_args_ta = [
            {"kind": "ema", "params": (5,)},
            {"kind": "fisher", "params": (13, 7)}
        ]

        custom = pandas_ta.Study(
            "Custom Args Tuple",
            custom_args_ta,
            "Allow for easy filling in indicator arguments by argument placement."
        )
        self.data.ta.study(custom, verbose=verbose, timed=timed_test)

    def test_custom_col_names_tuple(self):
        """Custom C: Column Name Tuple"""
        self.category = "Custom C: Column Name Tuple"

        custom_args_ta = [{"kind": "bbands", "col_names": ("LB", "MB", "UB", "BW", "BP")}]

        custom = pandas_ta.Study(
            "Custom Col Numbers Tuple",
            custom_args_ta,
            "Allow for easy renaming of resultant columns",
        )
        self.data.ta.study(custom, verbose=verbose, timed=timed_test)

    # @skip
    def test_custom_col_numbers_tuple(self):
        """Custom D: Column Number Tuple"""
        self.category = "Custom D: Column Number Tuple"

        custom_args_ta = [{"kind": "macd", "col_numbers": (1,)}]

        custom = pandas_ta.Study(
            "Custom Col Numbers Tuple",
            custom_args_ta,
            "Allow for easy selection of resultant columns",
        )
        self.data.ta.study(custom, verbose=verbose, timed=timed_test)

    def test_custom_ohlc(self):
        """Custom E: OHLC"""
        self.category = "Custom E: OHLC"

        self.data.rename(columns={"volume": "_v"}, inplace=True)
        self.data.ta.study(exclude=pandas_ta.Category["volume"], verbose=verbose, timed=timed_test)
        self.data.rename(columns={"_v": "volume"}, inplace=True)

    # @skip
    def test_custom_study_with_signals(self):
        """Custom F: Custom Study with Signals"""
        self.category = "Custom F: Custom Study with Signals"

        amat_logret_ta = [
            {"kind": "amat", "fast": 20, "slow": 50 },  # 2
            {"kind": "log_return", "cumulative": True},  # 1
            {"kind": "ema", "close": "CUMLOGRET_1", "length": 5} # 1
        ]

        custom = pandas_ta.Study(
            "AMAT Log Returns",  # name
            amat_logret_ta,  # ta
            "AMAT Log Returns",  # description
        )
        self.data.ta.study(custom, verbose=verbose, timed=timed_test, ordered=True, cores=0)
        self.data.ta.tsignals(trend=self.data["AMATe_LR_20_50_2"], append=True)

        if "adj close" in self.data.columns or "adj_close" in self.data.columns:
            self.assertEqual(len(self.data.columns), 14)
        else:
            self.assertEqual(len(self.data.columns), 15)

    # @skip
    def test_momentum_category(self):
        """Momentum"""
        self.category = "Momentum"
        self.data.ta.study(self.category, verbose=verbose, timed=timed_test)

    # @skip
    def test_overlap_category(self):
        """Overlap"""
        self.category = "Overlap"
        self.data.ta.study(self.category, verbose=verbose, timed=timed_test)

    # @skip
    def test_performance_category(self):
        """Performance"""
        self.category = "Performance"
        self.data.ta.study(self.category, verbose=verbose, timed=timed_test)

    # @skip
    def test_statistics_category(self):
        """Statistics"""
        self.category = "Statistics"
        self.data.ta.study(self.category, verbose=verbose, timed=timed_test)

    # @skip
    def test_transform_category(self):
        """Transform"""
        self.category = "Transform"
        self.data.ta.study(self.category, verbose=verbose, timed=timed_test)

    # @skip
    def test_trend_category(self):
        """Trend"""
        self.category = "Trend"
        self.data.ta.study(self.category, verbose=verbose, timed=timed_test)

    # @skip
    def test_volatility_category(self):
        """Volatility"""
        self.category = "Volatility"
        self.data.ta.study(self.category, verbose=verbose, timed=timed_test)

    # @skip
    def test_volume_category(self):
        """Volume"""
        self.category = "Volume"
        self.data.ta.study(self.category, verbose=verbose, timed=timed_test)

    # @skipUnless(verbose, "verbose mode only")
    def test_all_without_multiprocessing(self):
        """Study: All sans Multiprocessing"""
        self.category = "Study: All sans Multiprocessing"
        cores = self.data.ta.cores
        self.data.ta.cores = 0
        self.data.ta.study(verbose=verbose, timed=timed_test)
        self.data.ta.cores = cores
