# -*- coding: utf-8 -*-
import pandas_ta as ta
import pytest

from multiprocessing import cpu_count
from pandas import DataFrame

categories = DataFrame().ta.categories() + \
[pytest.param(ta.CommonStudy, id="common"), pytest.param(ta.AllStudy, id="all")]

# +/- when adding/removing indicators
ALL_COLUMNS = 321


def test_all_study_props(all_study):
    s = all_study
    assert s.name == "All"
    assert isinstance(s.description, str)
    assert s.total_ta() == 0 # Only 'study' that is None
    assert len(s.created) > 0
    assert s.cores == cpu_count()


def test_common_study_props(common_study):
    s = common_study
    assert s.name == "Common Price and Volume SMAs"
    assert isinstance(s.description, str)
    assert s.total_ta() == 5
    assert len(s.created) > 0
    assert s.cores == 0


@pytest.mark.parametrize("category,columns", [
    ("candles", 70), ("cycles", 2), ("momentum", 77), ("overlap", 56),
    ("performance", 2), ("statistics", 16), ("transform", 5), ("trend", 29),
    ("volatility", 36), ("volume", 28),
    pytest.param(ta.AllStudy, ALL_COLUMNS, id=f"all-{ALL_COLUMNS}"),
    pytest.param(ta.CommonStudy, 5, id="common-5"),
])
def test_study_category_columns(df, category, columns):
    initial_columns = df.shape[1]
    df.ta.study(category, cores=0)
    assert df.shape[1] == initial_columns + columns


@pytest.mark.parametrize("talib", [False, True])
@pytest.mark.parametrize("category", categories)
def test_study_category_talib(df, category, talib):
    initial_columns = df.shape[1]
    df.ta.study(category, cores=0, talib=talib)
    assert df.shape[1] > initial_columns


@pytest.mark.parametrize("talib", [False, True])
def test_study_custom_a(df, custom_study_a, talib):
    initial_columns = df.shape[1]
    df.ta.study(custom_study_a, cores=0, talib=talib)
    assert df.shape[1] > initial_columns


@pytest.mark.parametrize("talib", [False, True])
def test_study_custom_b(df, custom_study_b, talib):
    initial_columns = df.shape[1]
    df.ta.study(custom_study_b, cores=0, talib=talib)
    assert df.shape[1] - initial_columns == 3


@pytest.mark.parametrize("talib", [False, True])
def test_study_custom_c(df, custom_study_c, talib):
    initial_columns = df.shape[1]
    df.ta.study(custom_study_c, cores=0, talib=talib)
    assert df.shape[1] - initial_columns == 5


@pytest.mark.parametrize("talib", [False, True])
def test_study_custom_d(df, custom_study_d, talib):
    initial_columns = df.shape[1]
    df.ta.study(custom_study_d, cores=0, talib=talib)
    assert df.shape[1] - initial_columns == 3


@pytest.mark.parametrize("talib", [False, True])
def test_study_custom_e(df, custom_study_e, talib):
    initial_columns = df.shape[1]
    df.ta.study(custom_study_e, cores=0, talib=talib)
    df.ta.tsignals(trend=df["AMATe_LR_20_50_2"], append=True)
    assert df.shape[1] - initial_columns == 8


@pytest.mark.parametrize("talib", [False, True])
def test_study_all_multirun(df, all_study, talib):
    all_columns = 608  # +/- when adding/removing indicators
    initial_columns = df.shape[1]
    df.ta.study(all_study, length=10, cores=0, talib=talib)
    df.ta.study(all_study, length=50, cores=0, talib=talib)
    df.ta.study(all_study, fast=5, slow=10, cores=0, talib=talib)

    assert df.shape[1] - initial_columns == all_columns


@pytest.mark.parametrize("talib", [False, True])
def test_study_all_incremental_rows(df, all_study, talib):
    MAX_ROWS = 90
    df = df.iloc[:MAX_ROWS]   # Trim for this test

    for i in range(0, MAX_ROWS):
        _df = df.iloc[:i]
        _df.ta.study(all_study, cores=0, talib=talib)
        # Break when max columns reached
        if _df.shape[1] - df.shape[1] == ALL_COLUMNS:
            assert _df.shape[1] > df.shape[1]
            break


@pytest.mark.parametrize("talib", [False, True])
@pytest.mark.parametrize("category", categories)
def test_study_mp_category_talib(df, category, talib):
    cores = cpu_count() - 2
    initial_columns = df.shape[1]
    df.ta.study(category, cores=cores, talib=talib)
    assert df.shape[1] > initial_columns
