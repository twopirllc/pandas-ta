# -*- coding: utf-8 -*-
import pandas_ta as ta


# TA Lib style Tests
def test_cube(df):
    result = ta.cube(df.close)
    assert result.name == "CUBE_3.0_-1"


def test_ifisher(df):
    result = ta.ifisher(df.close)
    assert result.name == "INVFISHER_1.0"


def test_remap(df):
    result = ta.remap(df.close)
    assert result.name == "REMAP_0.0_100.0_-1.0_1.0"


# DataFrame Extension Tests
def test_ext_cube(df):
    df.ta.cube(append=True)
    assert list(df.columns[-2:]) == ["CUBE_3.0_-1", "CUBEs_3.0_-1"]


def test_ext_ifisher(df):
    df.ta.ifisher(append=True)
    assert list(df.columns[-2:]) == ["INVFISHER_1.0", "INVFISHERs_1.0"]


def test_ext_remap(df):
    df.ta.remap(append=True)
    assert df.columns[-1] == "REMAP_0.0_100.0_-1.0_1.0"
