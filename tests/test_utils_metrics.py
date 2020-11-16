from .config import sample_data
from .context import pandas_ta

from unittest import skip, TestCase

from numpy import nan as npNaN
from pandas import DataFrame



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
        result = pandas_ta.utils.cagr(self.data.close)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_calmar_ratio(self):
        result = pandas_ta.calmar_ratio(self.close)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

    def test_downside_deviation(self):
        result = pandas_ta.downside_deviation(self.pctret)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

        result = pandas_ta.downside_deviation(self.logret)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

    def test_drawdown(self):
        result = pandas_ta.drawdown(self.pctret)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "DD")

        result = pandas_ta.drawdown(self.logret)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "DD")

    def test_jensens_alpha(self):
        bench_return = self.pctret.sample(n=self.close.shape[0], random_state=1)
    
        result = pandas_ta.jensens_alpha(self.close, bench_return)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

    def test_log_max_drawdown(self):
        result = pandas_ta.log_max_drawdown(self.close)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

    def test_max_drawdown(self):
        result = pandas_ta.max_drawdown(self.close)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

        result = pandas_ta.max_drawdown(self.close, method="percent")
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

        result = pandas_ta.max_drawdown(self.close, method="log")
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

        result = pandas_ta.max_drawdown(self.close, all=True)
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["dollar"], float)
        self.assertIsInstance(result["percent"], float)
        self.assertIsInstance(result["log"], float)

    def test_pure_profit_score(self):
        result = pandas_ta.pure_profit_score(self.close)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

    def test_sharpe_ratio(self):
        result = pandas_ta.sharpe_ratio(self.close)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

    def test_sortino_ratio(self):
        result = pandas_ta.sortino_ratio(self.close)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

    def test_volatility(self):
        for tf in ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]:
            result = pandas_ta.utils.volatility(self.close, tf)
            self.assertIsInstance(result, float)
            self.assertGreaterEqual(result, 0)