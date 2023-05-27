# -*- coding: utf-8 -*-
import pandas_ta as ta


# TA Lib style Tests
def test_drawdown(df):
    result = ta.drawdown(df.close)
    assert result.name == "DD"


def test_log_return(df):
    result = ta.log_return(df.close)
    assert result.name == "LOGRET_1"


def test_cumlog_return(df):
    result = ta.log_return(df.close, cumulative=True)
    assert result.name == "CUMLOGRET_1"


def test_percent_return(df):
    result = ta.percent_return(df.close, cumulative=False)
    assert result.name == "PCTRET_1"


def test_cumpercent_return(df):
    result = ta.percent_return(df.close, cumulative=True)
    assert result.name == "CUMPCTRET_1"


# DataFrame Extension Tests
def test_ext_log_return(df):
    df.ta.log_return(append=True)
    assert df.columns[-1] == "LOGRET_1"


def test_ext_cumlog_return(df):
    df.ta.log_return(cumulative=True, append=True)
    assert df.columns[-1] == "CUMLOGRET_1"


def test_ext_percent_return(df):
    df.ta.percent_return(append=True)
    assert df.columns[-1] == "PCTRET_1"


def test_ext_cumpercent_return(df):
    df.ta.percent_return(cumulative=True, append=True)
    assert df.columns[-1] == "CUMPCTRET_1"
