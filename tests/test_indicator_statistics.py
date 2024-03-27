# -*- coding: utf-8 -*-
import pandas.testing as pdt
import talib as tal
import pandas_ta as ta

from pandas import DataFrame, Series
from pytest import mark

from .config import CORRELATION, CORRELATION_THRESHOLD, error_analysis


# TA Lib style Tests
def test_entropy(df):
    result = ta.entropy(df.close)
    assert isinstance(result, Series)
    assert result.name == "ENTP_10"


def test_kurtosis(df):
    result = ta.kurtosis(df.close)
    assert isinstance(result, Series)
    assert result.name == "KURT_30"


def test_mad(df):
    result = ta.mad(df.close)
    assert isinstance(result, Series)
    assert result.name == "MAD_30"


def test_median(df):
    result = ta.median(df.close)
    assert isinstance(result, Series)
    assert result.name == "MEDIAN_30"


def test_quantile(df):
    result = ta.quantile(df.close)
    assert isinstance(result, Series)
    assert result.name == "QTL_30_0.5"


def test_skew(df):
    result = ta.skew(df.close)
    assert isinstance(result, Series)
    assert result.name == "SKEW_30"


def test_stdev(df):
    result = ta.stdev(df.close, talib=False, ddof=0)
    assert isinstance(result, Series)
    assert result.name == "STDEV_30"

    try:
        expected = tal.STDDEV(df.close, 30)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)


@mark.parametrize("length,stds,name,columns", [
    (None, None, "TOS_STDEVALL", 7),
    (30, None, "TOS_STDEVALL_30", 7),
    (30, [1, 2], "TOS_STDEVALL_30", 5),
])
def test_tos_stdevall(df, length, stds, name, columns):
    result = ta.tos_stdevall(df.close, length=length, stds=stds)
    assert isinstance(result, DataFrame)
    assert result.name == name
    assert len(result.columns) == columns


def test_variance(df):
    result = ta.variance(df.close, talib=False, ddof=0)
    assert isinstance(result, Series)
    assert result.name == "VAR_30"

    try:
        expected = tal.VAR(df.close, 30)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.variance(df.close)
    assert isinstance(result, Series)
    assert result.name == "VAR_30"


def test_zscore(df):
    result = ta.zscore(df.close)
    assert isinstance(result, Series)
    assert result.name == "ZS_30"


# DataFrame Extension Tests
def test_ext_entropy(df):
    df.ta.entropy(append=True)
    assert df.columns[-1] == "ENTP_10"


def test_ext_kurtosis(df):
    df.ta.kurtosis(append=True)
    assert df.columns[-1] == "KURT_30"


def test_ext_mad(df):
    df.ta.mad(append=True)
    assert df.columns[-1] == "MAD_30"


def test_ext_median(df):
    df.ta.median(append=True)
    assert df.columns[-1] == "MEDIAN_30"


def test_ext_quantile(df):
    df.ta.quantile(append=True)
    assert df.columns[-1] == "QTL_30_0.5"


def test_ext_skew(df):
    df.ta.skew(append=True)
    assert df.columns[-1] == "SKEW_30"


def test_ext_stdev(df):
    df.ta.stdev(append=True)
    assert df.columns[-1] == "STDEV_30"


def test_ext_tos_stdevall(df):
    df.ta.tos_stdevall(append=True)
    columns = [
        "TOS_STDEVALL_LR",
        "TOS_STDEVALL_L_1", "TOS_STDEVALL_U_1",
        "TOS_STDEVALL_L_2", "TOS_STDEVALL_U_2",
        "TOS_STDEVALL_L_3", "TOS_STDEVALL_U_3"
    ]
    assert list(df.columns[-7:]) == columns


def test_ext_variance(df):
    df.ta.variance(append=True)
    assert df.columns[-1] == "VAR_30"


def test_ext_zscore(df):
    df.ta.zscore(append=True)
    assert df.columns[-1] == "ZS_30"
