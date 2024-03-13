# -*- coding: utf-8 -*-
import numpy as np
import pandas.testing as pdt
import talib as tal
import pandas_ta as ta

from pandas import DataFrame, Series
from pytest import mark

from .config import CORRELATION, CORRELATION_THRESHOLD, error_analysis


# TA Lib style Tests
def test_alligator(df):
    result = ta.alligator(df.high, df.low)
    assert isinstance(result, DataFrame)
    assert result.name == "AG_13_8_5"


def test_alma(df):
    result = ta.alma(df.close)
    assert isinstance(result, Series)
    assert result.name == "ALMA_9_6.0_0.85"


def test_dema(df):
    result = ta.dema(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "DEMA_10"

    try:
        expected = tal.DEMA(df.close, 10)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.dema(df.close)
    assert isinstance(result, Series)
    assert result.name == "DEMA_10"


def test_ema(df):
    result = ta.ema(df.close, talib=False, presma=True)
    assert isinstance(result, Series)
    assert result.name == "EMA_10"

    try:
        expected = tal.EMA(df.close, 10)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.ema(df.close, talib=True)
    assert isinstance(result, Series)
    assert result.name == "EMA_10"

    result = ta.ema(df.close, talib=True, presma=False, adjust=False)
    assert isinstance(result, Series)
    assert result.name == "EMA_10"

    result = ta.ema(df.close, talib=True, presma=False, adjust=True)
    assert isinstance(result, Series)
    assert result.name == "EMA_10"

    result = ta.ema(df.close, talib=True, presma=True, adjust=True)
    assert isinstance(result, Series)
    assert result.name == "EMA_10"


def test_fwma(df):
    result = ta.fwma(df.close)
    assert isinstance(result, Series)
    assert result.name == "FWMA_10"


def test_hilo(df):
    result = ta.hilo(df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "HILO_13_21"


def test_hl2(df):
    result = ta.hl2(df.high, df.low)
    assert isinstance(result, Series)
    assert result.name == "HL2"


def test_hlc3(df):
    result = ta.hlc3(df.high, df.low, df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "HLC3"

    try:
        expected = tal.TYPPRICE(df.high, df.low, df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.hlc3(df.high, df.low, df.close)
    assert isinstance(result, Series)
    assert result.name == "HLC3"


def test_hma(df):
    result = ta.hma(df.close)
    assert isinstance(result, Series)
    assert result.name == "HMA_10"


def test_hwma(df):
    result = ta.hwma(df.close)
    assert isinstance(result, Series)
    assert result.name == "HWMA_0.2_0.1_0.1"


def test_ichimoku(df):
    result_ichimoku, result_span = ta.ichimoku(df.high, df.low, df.close)
    assert isinstance(result_ichimoku, DataFrame)
    assert isinstance(result_span, DataFrame)
    assert result_ichimoku.name == "ICHIMOKU_9_26_52"
    assert result_span.name == "ICHISPAN_9_26"


def test_jma(df):
    result = ta.jma(df.close)
    assert isinstance(result, Series)
    assert result.name == "JMA_7_0.0"


def test_kama(df):
    result = ta.kama(df.close)
    assert isinstance(result, Series)
    assert result.name == "KAMA_10_2_30"


def test_linreg(df):
    result = ta.linreg(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "LINREG_14"

    try:
        expected = tal.LINEARREG(df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.linreg(df.close, talib=True)
    assert isinstance(result, Series)
    assert result.name == "LINREG_14"


def test_linreg_angle(df):
    result = ta.linreg(df.close, angle=True, talib=False)
    assert isinstance(result, Series)
    assert result.name == "LINREGa_14"

    try:
        expected = tal.LINEARREG_ANGLE(df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.linreg(df.close, angle=True, talib=True)
    assert isinstance(result, Series)
    assert result.name == "LINREGa_14"


def test_linreg_intercept(df):
    result = ta.linreg(df.close, intercept=True, talib=False)
    assert isinstance(result, Series)
    assert result.name == "LINREGb_14"

    try:
        expected = tal.LINEARREG_INTERCEPT(df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.linreg(df.close, intercept=True, talib=True)
    assert isinstance(result, Series)
    assert result.name == "LINREGb_14"


def test_linreg_r(df):
    result = ta.linreg(df.close, r=True)
    assert isinstance(result, Series)
    assert result.name == "LINREGr_14"


def test_linreg_slope(df):
    result = ta.linreg(df.close, slope=True, talib=False)
    assert isinstance(result, Series)
    assert result.name == "LINREGm_14"

    try:
        expected = tal.LINEARREG_SLOPE(df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.linreg(df.close, slope=True, talib=True)
    assert isinstance(result, Series)
    assert result.name == "LINREGm_14"


def test_ma(df):
    result = ta.ma()
    assert isinstance(result, list)
    assert len(result) > 0

    result = ta.ma("ema", df.close)
    assert isinstance(result, Series)
    assert result.name == "EMA_10"

    result = ta.ma("fwma", df.close, length=4)
    assert isinstance(result, Series)
    assert result.name == "FWMA_4"


def test_mama(df):
    result = ta.mama(df.close, talib=False)
    assert isinstance(result, DataFrame)
    assert result.name == "MAMA_0.5_0.05"

    try:
        expected = tal.MAMA(df.close)
        expecteddf = DataFrame({
            "MAMA_0.5_0.05": expected[0],
            "FAMA_0.5_0.05": expected[1]
        })
        pdt.assert_frame_equal(result, expecteddf)
    except AssertionError:
        try:
            mama_corr = ta.utils.df_error_analysis(result.iloc[:, 0], expecteddf.iloc[:, 0])
            assert mama_corr > CORRELATION_THRESHOLD
            print(f"{mama_corr=}")
        except Exception as ex:
            error_analysis(result.iloc[:, 0], CORRELATION, ex)

        try:
            fama_corr = ta.utils.df_error_analysis(result.iloc[:, 1], expecteddf.iloc[:, 1])
            assert fama_corr > CORRELATION_THRESHOLD
            print(f"{fama_corr=}")
        except Exception as ex:
            error_analysis(result.iloc[:, 1], CORRELATION, ex)

    result = ta.mama(df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "MAMA_0.5_0.05"


def test_mcgd(df):
    result = ta.mcgd(df.close)
    assert isinstance(result, Series)
    assert result.name == "MCGD_10"


def test_midpoint(df):
    result = ta.midpoint(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "MIDPOINT_2"

    try:
        expected = tal.MIDPOINT(df.close, 2)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.midpoint(df.close)
    assert isinstance(result, Series)
    assert result.name == "MIDPOINT_2"


def test_midprice(df):
    result = ta.midprice(df.high, df.low, talib=False)
    assert isinstance(result, Series)
    assert result.name == "MIDPRICE_2"

    try:
        expected = tal.MIDPRICE(df.high, df.low, 2)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.midprice(df.high, df.low)
    assert isinstance(result, Series)
    assert result.name == "MIDPRICE_2"


def test_ohlc4(df):
    result = ta.ohlc4(df.open, df.high, df.low, df.close)
    assert isinstance(result, Series)
    assert result.name == "OHLC4"


@mark.parametrize("method,name,columns", [
    (None, "PIVOTS_TRAD_D", 9), ("camarilla", "PIVOTS_CAMA_D", 9),
    ("classic", "PIVOTS_CLAS_D", 9), ("demark", "PIVOTS_DEMA_D", 3),
    ("fibonacci", "PIVOTS_FIBO_D", 7), ("traditional", "PIVOTS_TRAD_D", 9),
    ("woodie", "PIVOTS_WOOD_D", 9)
])
def test_pivots(df, method, name, columns):
    result = ta.pivots(df.open, df.high, df.low, df.close, method=method)
    assert isinstance(result, DataFrame)
    assert result.name == name
    assert result.columns.size == columns


def test_pwma(df):
    result = ta.pwma(df.close)
    assert isinstance(result, Series)
    assert result.name == "PWMA_10"


def test_rma(df):
    result = ta.rma(df.close)
    assert isinstance(result, Series)
    assert result.name == "RMA_10"


def test_sinwma(df):
    result = ta.sinwma(df.close)
    assert isinstance(result, Series)
    assert result.name == "SINWMA_14"


def test_sma(df):
    result = ta.sma(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "SMA_10"

    try:
        expected = tal.SMA(df.close, 10)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.sma(df.close, talib=True)
    assert isinstance(result, Series)
    assert result.name == "SMA_10"


def test_smma(df):
    result = ta.smma(df.close)
    assert isinstance(result, Series)
    assert result.name == "SMMA_7"


def test_ssf(df):
    result = ta.ssf(df.close)
    assert isinstance(result, Series)
    assert result.name == "SSF_20"

    result = ta.ssf(df.close, pi=np.pi, sqrt2=np.sqrt(2), everget=True)
    assert isinstance(result, Series)
    assert result.name == "SSFe_20"


def test_ssf3(df):
    result = ta.ssf3(df.close)
    assert isinstance(result, Series)
    assert result.name == "SSF3_20"


def test_swma(df):
    result = ta.swma(df.close)
    assert isinstance(result, Series)
    assert result.name == "SWMA_10"


def test_supertrend(df):
    result = ta.supertrend(df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "SUPERT_7_3.0"


def test_t3(df):
    result = ta.t3(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "T3_10_0.7"

    try:
        expected = tal.T3(df.close, 10)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.t3(df.close, talib=True)
    assert isinstance(result, Series)
    assert result.name == "T3_10_0.7"


def test_tema(df):
    result = ta.tema(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "TEMA_10"

    try:
        expected = tal.TEMA(df.close, 10)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.tema(df.close, talib=True)
    assert isinstance(result, Series)
    assert result.name == "TEMA_10"


def test_trima(df):
    result = ta.trima(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "TRIMA_10"

    try:
        expected = tal.TRIMA(df.close, 10)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.trima(df.close, talib=True)
    assert isinstance(result, Series)
    assert result.name == "TRIMA_10"


def test_tsf(df):
    result = ta.linreg(df.close, tsf=True, talib=False)
    assert isinstance(result, Series)
    assert result.name == "LINREG_14"

    try:
        expected = tal.TSF(df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.linreg(df.close, tsf=True, talib=True)
    assert isinstance(result, Series)
    assert result.name == "LINREG_14"


def test_vidya(df):
    result = ta.vidya(df.close)
    assert isinstance(result, Series)
    assert result.name == "VIDYA_14"


def test_vwma(df):
    result = ta.vwma(df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "VWMA_10"


def test_wcp(df):
    result = ta.wcp(df.high, df.low, df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "WCP"

    try:
        expected = tal.WCLPRICE(df.high, df.low, df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.wcp(df.high, df.low, df.close, talib=True)
    assert isinstance(result, Series)
    assert result.name == "WCP"


def test_wma(df):
    result = ta.wma(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "WMA_10"

    try:
        expected = tal.WMA(df.close, 10)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.wma(df.close, talib=True)
    assert isinstance(result, Series)
    assert result.name == "WMA_10"


def test_zlma(df):
    result = ta.zlma(df.close, df.volume)
    assert isinstance(result, Series)
    assert result.name == "ZL_EMA_10"


# DataFrame Extension Tests
def test_ext_alligator(df):
    df.ta.alligator(append=True)
    assert list(df.columns[-3:]) == ["AGj_13_8_5", "AGt_13_8_5", "AGl_13_8_5"]


def test_ext_alma(df):
    df.ta.alma(append=True)
    assert df.columns[-1] == "ALMA_9_6.0_0.85"


def test_ext_dema(df):
    df.ta.dema(append=True)
    assert df.columns[-1] == "DEMA_10"


def test_ext_ema(df):
    df.ta.ema(append=True)
    assert df.columns[-1] == "EMA_10"


def test_ext_fwma(df):
    df.ta.fwma(append=True)
    assert df.columns[-1] == "FWMA_10"


def test_ext_hilo(df):
    df.ta.hilo(append=True)
    assert list(df.columns[-3:]) == ["HILO_13_21", "HILOl_13_21", "HILOs_13_21"]


def test_ext_hl2(df):
    df.ta.hl2(append=True)
    assert df.columns[-1] == "HL2"


def test_ext_hlc3(df):
    df.ta.hlc3(append=True)
    assert df.columns[-1] == "HLC3"


def test_ext_hma(df):
    df.ta.hma(append=True)
    assert df.columns[-1] == "HMA_10"


def test_ext_hwma(df):
    df.ta.hwma(append=True)
    assert df.columns[-1] == "HWMA_0.2_0.1_0.1"


def test_ext_ichimoku(df):
    df.ta.ichimoku(append=True)
    columns = ["ISA_9", "ISB_26", "ITS_9", "IKS_26", "ICS_26"]
    assert list(df.columns[-5:]) == columns


def test_ext_jma(df):
    df.ta.jma(append=True)
    assert df.columns[-1] == "JMA_7_0.0"


def test_ext_kama(df):
    df.ta.kama(append=True)
    assert df.columns[-1] == "KAMA_10_2_30"


def test_ext_linreg(df):
    df.ta.linreg(append=True)
    assert df.columns[-1] == "LINREG_14"


def test_ext_mama(df):
    df.ta.mama(append=True)
    assert list(df.columns[-2:]) == ["MAMA_0.5_0.05", "FAMA_0.5_0.05"]


def test_ext_mcgd(df):
    df.ta.mcgd(append=True)
    assert df.columns[-1] == "MCGD_10"


def test_ext_midpoint(df):
    df.ta.midpoint(append=True)
    assert df.columns[-1] == "MIDPOINT_2"


def test_ext_midprice(df):
    df.ta.midprice(append=True)
    assert df.columns[-1] == "MIDPRICE_2"


def test_ext_ohlc4(df):
    df.ta.ohlc4(append=True)
    assert df.columns[-1] == "OHLC4"


def test_ext_pivots(df):
    df.ta.pivots(append=True)
    assert len(df.columns[-9:]) == 9


def test_ext_hl2(df):
    df.ta.hl2(append=True)
    assert df.columns[-1] == "HL2"


def test_ext_pwma(df):
    df.ta.pwma(append=True)
    assert df.columns[-1] == "PWMA_10"


def test_ext_sinwma(df):
    df.ta.sinwma(append=True)
    assert df.columns[-1] == "SINWMA_14"


def test_ext_sma(df):
    df.ta.sma(append=True)
    assert df.columns[-1] == "SMA_10"


def test_ext_smma(df):
    df.ta.smma(append=True)
    assert df.columns[-1] == "SMMA_7"


def test_ext_ssf(df):
    df.ta.ssf(append=True)
    assert df.columns[-1] == "SSF_20"


def test_ext_ssf3(df):
    df.ta.ssf3(append=True)
    assert df.columns[-1] == "SSF3_20"


def test_ext_swma(df):
    df.ta.swma(append=True)
    assert df.columns[-1] == "SWMA_10"


def test_ext_supertrend(df):
    df.ta.supertrend(append=True)
    columns = ["SUPERT_7_3.0", "SUPERTd_7_3.0", "SUPERTl_7_3.0", "SUPERTs_7_3.0"]
    assert list(df.columns[-4:]) == columns


def test_ext_t3(df):
    df.ta.t3(append=True)
    assert df.columns[-1] == "T3_10_0.7"


def test_ext_tema(df):
    df.ta.tema(append=True)
    assert df.columns[-1] == "TEMA_10"


def test_ext_trima(df):
    df.ta.trima(append=True)
    assert df.columns[-1] == "TRIMA_10"


def test_ext_vidya(df):
    df.ta.vidya(append=True)
    assert df.columns[-1] == "VIDYA_14"


def test_ext_vwap(df):
    df.ta.vwap(append=True)
    assert df.columns[-1] == "VWAP_D"


def test_ext_vwma(df):
    df.ta.vwma(append=True)
    assert df.columns[-1] == "VWMA_10"


def test_ext_wcp(df):
    df.ta.wcp(append=True)
    assert df.columns[-1] == "WCP"


def test_ext_wma(df):
    df.ta.wma(append=True)
    assert df.columns[-1] == "WMA_10"


def test_ext_zlma(df):
    df.ta.zlma(append=True)
    assert df.columns[-1] == "ZL_EMA_10"
