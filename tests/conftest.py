# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True

from os import system as os_system

import pytest
import pandas_ta as ta

from pandas import read_csv

TEST_ROWS = 200
TEST_CSV = f"data/SPY_D.csv"

BEEP = False
PLAY_BEEP = f"osascript -e beep"

@pytest.fixture(name="df", scope="function")
def testdf():
    """Yields a truncated df from TEST_CSV file"""
    df = read_csv(TEST_CSV, index_col=0, parse_dates=True)
    df.drop(columns=["dividends", "stock splits"], inplace=True)
    yield df.iloc[:TEST_ROWS]

    del df
    if BEEP: os_system(PLAY_BEEP)


@pytest.fixture(scope="function")
def all_study():
    """Returns the All Study"""
    return ta.AllStudy


@pytest.fixture(scope="function")
def common_study():
    """Returns the Common Study"""
    return ta.CommonStudy


@pytest.fixture(scope="function")
def custom_study_a():
    """Returns a Custom Study with a chained/composed indicator: 'ema(CUMLOGRET_1, 5)'.
    This Study only works when cores=0. When using mulptiprocessing (cores > 0),
    the multiprocesser might miss the results of the indicator
    'CUMLOGRET_1 = log_return(cumulative=True)'
    """
    _ta = [
        {"kind": "cdl_pattern", "name": "tristar"},  # 1
        {"kind": "rsi"},  # 1
        {"kind": "macd"},  # 3
        {"kind": "sma", "length": 50},  # 1
        {"kind": "trix"},  # 2
        {"kind": "bbands", "length": 20},  # 5
        {"kind": "log_return", "cumulative": True},  # 1
        {"kind": "ema", "close": "CUMLOGRET_1", "length": 5, "suffix": "CLR"} # 1
    ]
    return ta.Study(
        name="Commons with Cumulative Log Return EMA Chain",
        ta=_ta,
        # cores=0,
        description="Common indicators with specific lengths and a chained indicator"
    )


@pytest.fixture(scope="function")
def custom_study_b():
    """Returns a Custom Study that allows setting indicator values by
    parameter index as a tuple instead of using a named parameter"""
    _ta = [
        {"kind": "ema", "params": (5,)},  # 1
        {"kind": "fisher", "params": (13, 7)}  # 2
    ]
    return ta.Study(
        name="Custom Args Tuple",
        ta=_ta,
        description="Allow for easy filling in indicator arguments by argument placement"
    )


@pytest.fixture(scope="function")
def custom_study_c():
    """Returns a Custom Study that makes it easy to rename individual
    indicator resultant column names"""
    return ta.Study(
        name="Custom Col Numbers Tuple",
        ta=[{"kind": "bbands", "col_names": ("LB", "MB", "UB", "BW", "BP")}],
        description="Allow for easy renaming of resultant columns"
    )


@pytest.fixture(scope="function")
def custom_study_d():
    """Returns a Custom Study that makes it easily return individual
    indicator resultant columns by column number (col_numbers) as a tuple"""
    return ta.Study(
        name="Custom Col Numbers Tuple",
        ta=[
            {"kind": "macd", "col_numbers": (1,)},    # macd histogram
            {"kind": "bbands", "col_numbers": (0,2)}  # bbands lower and upper
        ],
        description="Allow for easy selection of resultant columns"
    )


@pytest.fixture(scope="function")
def custom_study_e():
    """Returns a Custom Study that has non default indicator parameters and
    an example of indicator composition/chaining: 'ema(CUMLOGRET_1, 5)'"""
    _ta = [
        {"kind": "amat", "fast": 20, "slow": 50 },  # 2
        {"kind": "log_return", "cumulative": True},  # 1
        {"kind": "ema", "close": "CUMLOGRET_1", "length": 5} # 1
    ]

    return ta.Study(
        name="AMAT Log Returns",
        ta=_ta,
        cores=0,
        description="AMAT Log Returns"
    )
