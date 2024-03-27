# -*- coding: utf-8 -*-
import pandas.testing as pdt
import pandas_ta as ta
import talib as tal

from pandas import DataFrame, Series

from .config import CORRELATION, CORRELATION_THRESHOLD, error_analysis


# TA Lib style Tests
def test_aberration(df):
    result = ta.aberration(df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "ABER_5_15"


def test_accbands(df):
    result = ta.accbands(df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "ACCBANDS_20"


def test_atr(df):
    result = ta.atr(df.high, df.low, df.close, talib=False, prenan=True)
    assert isinstance(result, Series)
    assert result.name == "ATRr_14"

    try:
        expected = tal.ATR(df.high, df.low, df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.atr(df.high, df.low, df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "ATRr_14"


def test_atrts(df):
    result = ta.atrts(df.high, df.low, df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "ATRTSe_14_20_3.0"


def test_bbands(df):
    result = ta.bbands(df.close, talib=False)
    assert isinstance(result, DataFrame)
    assert result.name == "BBANDS_5_2.0"

    try:
        expected = tal.BBANDS(df.close)
        expecteddf = DataFrame({
            "BBL_5_2.0": expected[2],
            "BBM_5_2.0": expected[1],
            "BBU_5_2.0": expected[0]
        })
        pdt.assert_frame_equal(result, expecteddf)
    except AssertionError:
        try:
            bbl_corr = ta.utils.df_error_analysis(result, expected)
            print(f"{bbl_corr=}")
            assert bbl_corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result.iloc[:, 0], CORRELATION, ex)

        try:
            bbm_corr = ta.utils.df_error_analysis(result, expected)
            print(f"{bbm_corr=}")
            assert bbm_corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result.iloc[:, 1], CORRELATION, ex)

        try:
            bbu_corr = ta.utils.df_error_analysis(result, expected)
            print(f"{bbu_corr=}")
            assert bbu_corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result.iloc[:, 2], CORRELATION, ex)

    result = ta.bbands(df.close, ddof=0)
    assert isinstance(result, DataFrame)
    assert result.name == "BBANDS_5_2.0"

    result = ta.bbands(df.close, ddof=1)
    assert isinstance(result, DataFrame)
    assert result.name == "BBANDS_5_2.0"


def test_chandelier_exit(df):
    result = ta.chandelier_exit(df.high, df.low, df.close, talib=False)
    assert isinstance(result, DataFrame)
    assert result.name == "CHDLREXT_22_22_14_2.0"


def test_donchian(df):
    result = ta.donchian(df.high, df.low)
    assert isinstance(result, DataFrame)
    assert result.name == "DC_20_20"

    result = ta.donchian(df.high, df.low, lower_length=10, upper_length=5)
    assert isinstance(result, DataFrame)
    assert result.name == "DC_10_5"


def test_hwc(df):
    result = ta.hwc(df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "HWC_1"

    result = ta.hwc(df.close, channels=True)
    assert isinstance(result, DataFrame)
    assert result.name == "HWC_1"


def test_kc(df):
    result = ta.kc(df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "KCe_20_2"

    result = ta.kc(df.high, df.low, df.close, mamode="sma")
    assert isinstance(result, DataFrame)
    assert result.name == "KCs_20_2"


def test_massi(df):
    result = ta.massi(df.high, df.low)
    assert isinstance(result, Series)
    assert result.name == "MASSI_9_25"


def test_natr(df):
    result = ta.natr(df.high, df.low, df.close, talib=False, prenan=True)
    assert isinstance(result, Series)
    assert result.name == "NATR_14"

    try:
        expected = tal.NATR(df.high, df.low, df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.natr(df.high, df.low, df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "NATR_14"


def test_pdist(df):
    result = ta.pdist(df.open, df.high, df.low, df.close)
    assert isinstance(result, Series)
    assert result.name == "PDIST"


def test_rvi(df):
    result = ta.rvi(df.close)
    assert isinstance(result, Series)
    assert result.name == "RVI_14"

    result = ta.rvi(df.close, df.high, df.low, refined=True)
    assert isinstance(result, Series)
    assert result.name == "RVIr_14"

    result = ta.rvi(df.close, df.high, df.low, thirds=True)
    assert isinstance(result, Series)
    assert result.name == "RVIt_14"


def test_thermo(df):
    result = ta.thermo(df.high, df.low)
    assert isinstance(result, DataFrame)
    assert result.name == "THERMO_20_2_0.5"


def test_true_range(df):
    result = ta.true_range(df.high, df.low, df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "TRUERANGE_1"

    try:
        expected = tal.TRANGE(df.high, df.low, df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.true_range(df.high, df.low, df.close)
    assert isinstance(result, Series)
    assert result.name == "TRUERANGE_1"


def test_ui(df):
    result = ta.ui(df.close)
    assert isinstance(result, Series)
    assert result.name == "UI_14"

    result = ta.ui(df.close, everget=True)
    assert isinstance(result, Series)
    assert result.name == "UIe_14"


# DataFrame Extension Tests
def test_ext_aberration(df):
    df.ta.aberration(append=True)
    columns = ["ABER_ZG_5_15", "ABER_SG_5_15", "ABER_XG_5_15", "ABER_ATR_5_15"]
    assert list(df.columns[-4:]) == columns


def test_ext_accbands(df):
    df.ta.accbands(append=True)
    assert list(df.columns[-3:]) == ["ACCBL_20", "ACCBM_20", "ACCBU_20"]


def test_ext_atr(df):
    df.ta.atr(append=True)
    assert df.columns[-1] == "ATRr_14"


def test_ext_atrts(df):
    df.ta.atrts(append=True)
    assert df.columns[-1] == "ATRTSe_14_20_3.0"


def test_ext_bbands(df):
    df.ta.bbands(append=True)
    columns = ["BBL_5_2.0", "BBM_5_2.0", "BBU_5_2.0", "BBB_5_2.0", "BBP_5_2.0"]
    assert list(df.columns[-5:]) == columns


def test_ext_chandelier_exit(df):
    df.ta.chandelier_exit(append=True)
    columns = [
        "CHDLREXTl_22_22_14_2.0", "CHDLREXTs_22_22_14_2.0", "CHDLREXTd_22_22_14_2.0"
    ]
    assert list(df.columns[-3:]) == columns


def test_ext_donchian(df):
    df.ta.donchian(append=True)
    assert list(df.columns[-3:]) == ["DCL_20_20", "DCM_20_20", "DCU_20_20"]


def test_ext_kc(df):
    df.ta.kc(append=True)
    assert list(df.columns[-3:]) == ["KCLe_20_2", "KCBe_20_2", "KCUe_20_2"]


def test_ext_massi(df):
    df.ta.massi(append=True)
    assert df.columns[-1] == "MASSI_9_25"


def test_ext_natr(df):
    df.ta.natr(append=True)
    assert df.columns[-1] == "NATR_14"


def test_ext_pdist(df):
    df.ta.pdist(append=True)
    assert df.columns[-1] == "PDIST"


def test_ext_rvi(df):
    df.ta.rvi(append=True)
    assert df.columns[-1] == "RVI_14"

    df.ta.rvi(refined=True, append=True)
    assert df.columns[-1] == "RVIr_14"

    df.ta.rvi(thirds=True, append=True)
    assert df.columns[-1] == "RVIt_14"


def test_ext_thermo(df):
    df.ta.thermo(append=True)
    columns = [
        "THERMO_20_2_0.5", "THERMOma_20_2_0.5",
        "THERMOl_20_2_0.5", "THERMOs_20_2_0.5"
    ]
    assert list(df.columns[-4:]) == columns


def test_ext_true_range(df):
    df.ta.true_range(append=True)
    assert df.columns[-1] == "TRUERANGE_1"


def test_ext_ui(df):
    df.ta.ui(append=True)
    assert df.columns[-1] == "UI_14"

    df.ta.ui(everget=True, append=True)
    assert df.columns[-1] == "UIe_14"
