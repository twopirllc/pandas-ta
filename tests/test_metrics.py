# -*- coding: utf-8 -*-
import pandas_ta as ta

from pytest import mark


def test_cagr(df):
    result = ta.utils.cagr(df.close)
    assert isinstance(result, float)

def test_calmar_ratio(df):
    result = ta.utils.calmar_ratio(df.close)
    assert isinstance(result, float)

@mark.parametrize("year,result", [(-2, None), (0, None)])
def test_calmar_ratio_year(df, year, result):
    assert ta.utils.calmar_ratio(df.close, years=year) is result

def test_downside_deviation(df):
    pctret = df.ta.percent_return()
    result = ta.utils.downside_deviation(pctret)
    assert isinstance(result, float)

    logret = df.ta.percent_return()
    result = ta.utils.downside_deviation(logret)
    assert isinstance(result, float)

def test_jensens_alpha(df):
    bench_return = df.ta.percent_return() \
        .sample(n=df.close.shape[0], random_state=1)
    result = ta.utils.jensens_alpha(df.close, bench_return)
    assert isinstance(result, float)

def test_log_max_drawdown(df):
    result = ta.utils.log_max_drawdown(df.close)
    assert isinstance(result, float)

def test_max_drawdown(df):
    result = ta.utils.max_drawdown(df.close)
    assert isinstance(result, float)

    result = ta.utils.max_drawdown(df.close, method="percent")
    assert isinstance(result, float)

    result = ta.utils.max_drawdown(df.close, method="log")
    assert isinstance(result, float)

    result = ta.utils.max_drawdown(df.close, all=True)
    assert isinstance(result, dict)
    assert isinstance(result["dollar"], float)
    assert isinstance(result["percent"], float)
    assert isinstance(result["log"], float)

def test_optimal_leverage(df):
    result = ta.utils.optimal_leverage(df.close)
    assert isinstance(result, int)

    result = ta.utils.optimal_leverage(df.close, log=True)
    assert isinstance(result, int)

def test_pure_profit_score(df):
    result = ta.utils.pure_profit_score(df.close)
    assert isinstance(result, float)

def test_sharpe_ratio(df):
    result = ta.utils.sharpe_ratio(df.close)
    assert isinstance(result, float)

def test_sortino_ratio(df):
    result = ta.utils.sortino_ratio(df.close)
    assert isinstance(result, float)

def test_volatility(df):
    pctret = df.ta.percent_return()
    result = ta.utils.volatility(pctret, returns=True)
    assert isinstance(result, float)

@mark.parametrize("tf", ["years", "months", "weeks", "days", "hours", "minutes", "seconds"])
def test_volatility_timeframe(df, tf):
    assert isinstance(ta.utils.volatility(df.close, tf), float)