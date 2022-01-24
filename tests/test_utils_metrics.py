# -*- coding: utf-8 -*-
from unittest import TestCase, skip

from .config import sample_data
from .context import pandas_ta


class TestUtilityMetrics(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.close = cls.data["close"]
        cls.pctret = pandas_ta.percent_return(cls.close, cumulative=False)
        cls.logret = pandas_ta.percent_return(cls.close, cumulative=False)

    @classmethod
    def tearDownClass(cls):
        del cls.data
        del cls.pctret
        del cls.logret

    def setUp(self): pass
    def tearDown(self): pass


    def test_cagr(self):
        """Metrics: CAGR"""
        result = pandas_ta.utils.cagr(self.data.close)
        self.assertIsInstance(result, float)

    def test_calmar_ratio(self):
        """Metrics: Calmar Ratio"""
        result = pandas_ta.calmar_ratio(self.close)
        self.assertIsInstance(result, float)

        result = pandas_ta.calmar_ratio(self.close, years=0)
        self.assertIsNone(result)

        result = pandas_ta.calmar_ratio(self.close, years=-2)
        self.assertIsNone(result)

    def test_downside_deviation(self):
        """Metrics: Downside Deviation"""
        result = pandas_ta.downside_deviation(self.pctret)
        self.assertIsInstance(result, float)

        result = pandas_ta.downside_deviation(self.logret)
        self.assertIsInstance(result, float)

    def test_jensens_alpha(self):
        """Metrics: Jensens Alpha"""
        bench_return = self.pctret.sample(n=self.close.shape[0], random_state=1)
        result = pandas_ta.jensens_alpha(self.close, bench_return)
        self.assertIsInstance(result, float)

    def test_log_max_drawdown(self):
        """Metrics: Max Log Drawdown"""
        result = pandas_ta.log_max_drawdown(self.close)
        self.assertIsInstance(result, float)

    def test_max_drawdown(self):
        """Metrics: Max Drawdown"""
        result = pandas_ta.max_drawdown(self.close)
        self.assertIsInstance(result, float)

        result = pandas_ta.max_drawdown(self.close, method="percent")
        self.assertIsInstance(result, float)

        result = pandas_ta.max_drawdown(self.close, method="log")
        self.assertIsInstance(result, float)

        result = pandas_ta.max_drawdown(self.close, all=True)
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["dollar"], float)
        self.assertIsInstance(result["percent"], float)
        self.assertIsInstance(result["log"], float)

    def test_optimal_leverage(self):
        """Metrics: Optimal Leverage"""
        result = pandas_ta.optimal_leverage(self.close)
        self.assertIsInstance(result, int)
        result = pandas_ta.optimal_leverage(self.close, log=True)
        self.assertIsInstance(result, int)

    def test_pure_profit_score(self):
        """Metrics: Pure Profit Score"""
        result = pandas_ta.pure_profit_score(self.close)
        self.assertIsInstance(result, float)

    def test_sharpe_ratio(self):
        """Metrics: Sharpe Ratio"""
        result = pandas_ta.sharpe_ratio(self.close)
        self.assertIsInstance(result, float)

    def test_sortino_ratio(self):
        """Metrics: Sortino Ratio"""
        result = pandas_ta.sortino_ratio(self.close)
        self.assertIsInstance(result, float)

    def test_volatility(self):
        """Metrics: Volatility"""
        returns_ = pandas_ta.percent_return(self.close)
        result = pandas_ta.utils.volatility(returns_, returns=True)
        self.assertIsInstance(result, float)

        for tf in ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]:
            result = pandas_ta.utils.volatility(self.close, tf)
            with self.subTest(tf=tf):
                self.assertIsInstance(result, float)
