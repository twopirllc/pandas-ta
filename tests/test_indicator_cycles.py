# -*- coding: utf-8 -*-
import pandas_ta as ta

from pandas import Series


# TA Lib style Tests
def test_ebsw(df):
    result = ta.ebsw(df.close)
    assert isinstance(result, Series)
    assert result.name == "EBSW_40_10"


def test_reflex(df):
    result = ta.reflex(df.close)
    assert isinstance(result, Series)
    assert result.name == "REFLEX_20_20_0.04"


# DataFrame Extension Tests
def test_ext_ebsw(df):
    df.ta.ebsw(append=True)
    assert df.columns[-1] == "EBSW_40_10"


def test_ext_reflex(df):
    df.ta.reflex(append=True)
    assert df.columns[-1] == "REFLEX_20_20_0.04"
