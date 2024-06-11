# -*- coding: utf-8 -*-
import pandas.testing as pdt
import pandas_ta as ta
import talib as tal

from pandas import DataFrame, Series
from pytest import mark

from .config import CORRELATION, CORRELATION_THRESHOLD, error_analysis


# TA Lib style Tests
def test_ad(df):
    result = ta.ad(df.high, df.low, df.close, df.volume, talib=False)
    assert isinstance(result, Series)
    assert result.name == "AD"

    try:
        expected = tal.AD(df.high, df.low, df.close, df.volume)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.ad(df.high, df.low, df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "AD"


def test_ad_open(df):
    result = ta.ad(df.high, df.low, df.close, df.volume, df.open)
    assert isinstance(result, Series)
    assert result.name == "ADo"


def test_adosc(df):
    result = ta.adosc(df.high, df.low, df.close, df.volume, talib=False)
    assert isinstance(result, Series)
    assert result.name == "ADOSC_3_10"

    try:
        expected = tal.ADOSC(df.high, df.low, df.close, df.volume)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.adosc(df.high, df.low, df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "ADOSC_3_10"


def test_aobv(df):
    result = ta.aobv(df.close, df.volume)
    assert isinstance(result, DataFrame)
    assert result.name == "AOBVe_4_12_2_2_2"


def test_cmf(df):
    result = ta.cmf(df.high, df.low, df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "CMF_20"


def test_efi(df):
    result = ta.efi(df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "EFI_13"


def test_eom(df):
    result = ta.eom(df.high, df.low, df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "EOM_14_100000000"


def test_kvo(df):
    result = ta.kvo(df.high, df.low, df.close, df.volume)
    assert isinstance(result, DataFrame)
    assert result.name == "KVO_34_55_13"


def test_mfi(df):
    result = ta.mfi(df.high, df.low, df.close, df.volume, talib=False)
    assert isinstance(result, Series)
    assert result.name == "MFI_14"

    try:
        expected = tal.MFI(df.high, df.low, df.close, df.volume)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.mfi(df.high, df.low, df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "MFI_14"


def test_nvi(df):
    result = ta.nvi(df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "NVI_1"


def test_obv(df):
    result = ta.obv(df.close, df.volume, talib=False)
    assert isinstance(result, Series)
    assert result.name == "OBV"

    try:
        expected = tal.OBV(df.close, df.volume)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.obv(df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "OBV"


def test_pvi(df):
    result = ta.pvi(df.close, df.volume, length=10)
    assert isinstance(result, DataFrame)
    assert result.name == "PVI"

    result = ta.pvi(df.close, df.volume, length=10, overlay=True)
    assert isinstance(result, DataFrame)
    assert df.close.iloc[0] == result.iloc[0,0]


def test_pvol(df):
    result = ta.pvol(df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "PVOL"


def test_pvr(df):
    result = ta.pvr(df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "PVR"


def test_pvt(df):
    result = ta.pvt(df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "PVT"


def test_vhm(df):
    result = ta.vhm(df.volume, 30, 30)
    assert isinstance(result, Series)
    assert result.name == "VHM_30"

    result = ta.vhm(df.volume, 10, 20)
    assert isinstance(result, Series)
    assert result.name == "VHM_10_20"


def test_vp(df):
    result = ta.vp(df.close, df.volume)
    assert isinstance(result, DataFrame)
    assert result.name == "VP_10"

    result = ta.vp(df.close, df.volume, sort=True)
    assert isinstance(result, DataFrame)
    assert result.name == "VP_10"


@mark.parametrize("bands,dtype", [
    (None, Series), ([1], DataFrame), ([-1, 1], DataFrame),
    ([1, 2, 4, 8], DataFrame), ([1, 2.5, 4.13], DataFrame),
])
def test_vwap(df, bands, dtype):
    result = ta.vwap(df.high, df.low, df.close, df.volume, bands=bands)
    assert isinstance(result, dtype)
    assert result.name == "VWAP_D"


def test_wb_tsv(df):
    result = ta.wb_tsv(df.close, df.volume)
    assert isinstance(result, DataFrame)
    assert result.name == "TSV_18_10"


# DataFrame Extension Tests
def test_ext_ad(df):
    df.ta.ad(talib=False, append=True)
    assert df.columns[-1] == "AD"


def test_ext_ad_open(df):
    df.ta.ad(open_=df.open, append=True)
    assert df.columns[-1] == "ADo"


def test_ext_adosc(df):
    df.ta.adosc(append=True)
    assert df.columns[-1] == "ADOSC_3_10"


def test_ext_aobv(df):
    df.ta.aobv(append=True)
    columns = [
        "OBV", "OBV_min_2", "OBV_max_2", "OBVe_4",
        "OBVe_12", "AOBV_LR_2", "AOBV_SR_2"
    ]
    assert list(df.columns[-7:]) == columns


def test_ext_cmf(df):
    df.ta.cmf(append=True)
    assert df.columns[-1] == "CMF_20"


def test_ext_efi(df):
    df.ta.efi(append=True)
    assert df.columns[-1] == "EFI_13"


def test_ext_eom(df):
    df.ta.eom(append=True)
    assert df.columns[-1] == "EOM_14_100000000"


def test_ext_kvo(df):
    df.ta.kvo(append=True)
    assert list(df.columns[-2:]) == ["KVO_34_55_13", "KVOs_34_55_13"]


def test_ext_mfi(df):
    df.ta.mfi(append=True)
    assert df.columns[-1] == "MFI_14"


def test_ext_nvi(df):
    df.ta.nvi(append=True)
    assert df.columns[-1] == "NVI_1"


# def test_ext_pvi(df):
    df.ta.pvi(length=10, append=True)
    assert list(df.columns[-2:]) == ["PVI", "PVIe_10"]


def test_ext_pvol(df):
    df.ta.pvol(append=True)
    assert df.columns[-1] == "PVOL"


def test_ext_pvr(df):
    df.ta.pvr(append=True)
    assert df.columns[-1] == "PVR"


def test_ext_pvt(df):
    df.ta.pvt(append=True)
    assert df.columns[-1] == "PVT"


def test_ext_vhm(df):
    df.ta.vhm(length=30, slength=30, append=True)
    assert df.columns[-1] == "VHM_30"


def test_ext_wb_tsv(df):
    df.ta.wb_tsv(append=True)
    assert list(df.columns[-3:]) == ["TSV_18_10", "TSVs_18_10", "TSVr_18_10"]
