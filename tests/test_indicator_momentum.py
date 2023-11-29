# -*- coding: utf-8 -*-
import pandas.testing as pdt
import talib as tal
import pandas_ta as ta

from pandas import DataFrame, Series
from pytest import mark

from .config import CORRELATION, CORRELATION_THRESHOLD, error_analysis


# TA Lib style Tests
def test_ao(df):
    result = ta.ao(df.high, df.low)
    assert isinstance(result, Series)
    assert result.name == "AO_5_34"


def test_apo(df):
    result = ta.apo(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "APO_12_26"

    try:
        expected = tal.APO(df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            assert corr > CORRELATION_THRESHOLD
            print(f"{corr=}")
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.apo(df.close)
    assert isinstance(result, Series)
    assert result.name == "APO_12_26"


def test_bias(df):
    result = ta.bias(df.close)
    assert isinstance(result, Series)
    assert result.name == "BIAS_SMA_26"


def test_bop(df):
    result = ta.bop(df.open, df.high, df.low, df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "BOP"

    try:
        expected = tal.BOP(df.open, df.high, df.low, df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            assert corr > CORRELATION_THRESHOLD
            print(f"{corr=}")
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.bop(df.open, df.high, df.low, df.close)
    assert isinstance(result, Series)
    assert result.name == "BOP"


def test_brar(df):
    result = ta.brar(df.open, df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "BRAR_26"


def test_cci(df):
    result = ta.cci(df.high, df.low, df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "CCI_14_0.015"

    try:
        expected = tal.CCI(df.high, df.low, df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            assert corr > CORRELATION_THRESHOLD
            print(f"{corr=}")
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.cci(df.high, df.low, df.close)
    assert isinstance(result, Series)
    assert result.name == "CCI_14_0.015"


def test_cfo(df):
    result = ta.cfo(df.close)
    assert isinstance(result, Series)
    assert result.name == "CFO_9"


def test_cg(df):
    result = ta.cg(df.close)
    assert isinstance(result, Series)
    assert result.name == "CG_10"


def test_cmo(df):
    result = ta.cmo(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "CMO_14"

    try:
        expected = tal.CMO(df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            assert corr > CORRELATION_THRESHOLD
            print(f"{corr=}")
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.cmo(df.close)
    assert isinstance(result, Series)
    assert result.name == "CMO_14"


def test_coppock(df):
    result = ta.coppock(df.close)
    assert isinstance(result, Series)
    assert result.name == "COPC_11_14_10"


def test_cti(df):
    result = ta.cti(df.close)
    assert isinstance(result, Series)
    assert result.name == "CTI_12"


def test_crsi(df):
    result = ta.crsi(df.close)
    assert isinstance(result, Series)
    assert result.name == "CRSI_3_2_100"


def test_er(df):
    result = ta.er(df.close)
    assert isinstance(result, Series)
    assert result.name == "ER_10"


def test_dm(df):
    result = ta.dm(df.high, df.low, talib=False)
    assert isinstance(result, DataFrame)
    assert result.name == "DM_14"

    try:
        expected_pos = tal.PLUS_DM(df.high, df.low)
        expected_neg = tal.MINUS_DM(df.high, df.low)
        expecteddf = DataFrame({"DMP_14": expected_pos, "DMN_14": expected_neg})
        pdt.assert_frame_equal(result, expecteddf)
    except AssertionError:
        try:
            dmp_corr = ta.utils.df_error_analysis(result.iloc[:, 0], expecteddf.iloc[:, 0])
            assert dmp_corr > CORRELATION_THRESHOLD
            print(f"{dmp_corr=}")
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

        try:
            dmn_corr = ta.utils.df_error_analysis(result.iloc[:, 1], expecteddf.iloc[:, 1])
            assert dmn_corr > CORRELATION_THRESHOLD
            print(f"{dmn_corr=}")
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.dm(df.high, df.low)
    assert isinstance(result, DataFrame)
    assert result.name == "DM_14"


def test_eri(df):
    result = ta.eri(df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "ERI_13"


def test_fisher(df):
    result = ta.fisher(df.high, df.low)
    assert isinstance(result, DataFrame)
    assert result.name == "FISHERT_9_1"


def test_inertia(df):
    result = ta.inertia(df.close)
    assert isinstance(result, Series)
    assert result.name == "INERTIA_20_14"

    result = ta.inertia(df.close, df.high, df.low, refined=True)
    assert isinstance(result, Series)
    assert result.name == "INERTIAr_20_14"

    result = ta.inertia(df.close, df.high, df.low, thirds=True)
    assert isinstance(result, Series)
    assert result.name == "INERTIAt_20_14"


def test_kdj(df):
    result = ta.kdj(df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "KDJ_9_3"


def test_kst(df):
    result = ta.kst(df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "KST_10_15_20_30_10_10_10_15_9"


def test_macd(df):
    result = ta.macd(df.close, talib=False)
    assert isinstance(result, DataFrame)
    assert result.name == "MACD_12_26_9"

    try:
        expected = tal.MACD(df.close)
        expecteddf = DataFrame({
            "MACDh_12_26_9": expected[2],
            "MACDs_12_26_9": expected[1],
            "MACD_12_26_9": expected[0]
        })
        pdt.assert_frame_equal(result, expecteddf)
    except AssertionError:
        try:
            macd_corr = ta.utils.df_error_analysis(result, expected)
            print(f"{macd_corr=}")
            assert macd_corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result.iloc[:, 0], CORRELATION, ex)

        try:
            history_corr = ta.utils.df_error_analysis(result, expected)
            print(f"{history_corr=}")
            assert history_corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result.iloc[:, 1], CORRELATION, ex)

        try:
            signal_corr = ta.utils.df_error_analysis(result, expected)
            print(f"{signal_corr=}")
            assert signal_corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result.iloc[:, 2], CORRELATION, ex)

    result = ta.macd(df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "MACD_12_26_9"


def test_macdas(df):
    result = ta.macd(df.close, asmode=True)
    assert isinstance(result, DataFrame)
    assert result.name == "MACDAS_12_26_9"


def test_mom(df):
    result = ta.mom(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "MOM_10"

    try:
        expected = tal.MOM(df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.mom(df.close)
    assert isinstance(result, Series)
    assert result.name == "MOM_10"


def test_pgo(df):
    result = ta.pgo(df.high, df.low, df.close, asmode=True)
    assert isinstance(result, Series)
    assert result.name == "PGO_14"


def test_ppo(df):
    result = ta.ppo(df.close, talib=False)
    assert isinstance(result, DataFrame)
    assert result.name == "PPO_12_26_9"

    try:
        expected = tal.PPO(df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.ppo(df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "PPO_12_26_9"


def test_psl(df):
    result = ta.psl(df.close, asmode=True)
    assert isinstance(result, Series)
    assert result.name == "PSL_12"


def test_pvo(df):
    result = ta.pvo(df.volume, asmode=True)
    assert isinstance(result, DataFrame)
    assert result.name == "PVO_12_26_9"


def test_qqe(df):
    result = ta.qqe(df.volume, asmode=True)
    assert isinstance(result, DataFrame)
    assert result.name == "QQE_14_5_4.236"


def test_roc(df):
    result = ta.roc(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "ROC_10"

    try:
        expected = tal.ROC(df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.roc(df.close)
    assert isinstance(result, Series)
    assert result.name == "ROC_10"


def test_rsi(df):
    result = ta.rsi(df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "RSI_14"

    try:
        expected = tal.RSI(df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.rsi(df.close)
    assert isinstance(result, Series)
    assert result.name == "RSI_14"


def test_rsx(df):
    result = ta.rsx(df.close)
    assert isinstance(result, Series)
    assert result.name == "RSX_14"


@mark.skip(reason="AttributeError: 'Series' object has no attribute 'df'")
def test_rvgi(df):
    result = ta.rvgi(df.open, df.high, df.low. df.close) # Weird Exception
    assert isinstance(result, Series)
    assert result.name == "RVGI_14_4"


def test_slope(df):
    result = ta.slope(df.close)
    assert isinstance(result, Series)
    assert result.name == "SLOPE_1"

    result = ta.slope(df.close, as_angle=True)
    assert isinstance(result, Series)
    assert result.name == "ANGLEr_1"

    result = ta.slope(df.close, as_angle=True, to_degrees=True)
    assert isinstance(result, Series)
    assert result.name == "ANGLEd_1"


def test_smi(df):
    result = ta.smi(df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "SMI_5_20_5_1.0"

    result = ta.smi(df.close, scalar=10)
    assert isinstance(result, DataFrame)
    assert result.name == "SMI_5_20_5_10.0"


def test_squeeze(df):
    result = ta.squeeze(df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "SQZ_20_2.0_20_1.5"

    result = ta.squeeze(df.high, df.low, df.close, tr=False)
    assert isinstance(result, DataFrame)
    assert result.name == "SQZhlr_20_2.0_20_1.5"

    result = ta.squeeze(df.high, df.low, df.close, lazybear=True)
    assert isinstance(result, DataFrame)
    assert result.name == "SQZ_20_2.0_20_1.5_LB"

    result = ta.squeeze(df.high, df.low, df.close, tr=False, lazybear=True)
    assert isinstance(result, DataFrame)
    assert result.name == "SQZhlr_20_2.0_20_1.5_LB"


def test_squeeze_pro(df):
    result = ta.squeeze_pro(df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "SQZPRO_20_2.0_20_2.0_1.5_1.0"

    result = ta.squeeze_pro(df.high, df.low, df.close, tr=False)
    assert isinstance(result, DataFrame)
    assert result.name == "SQZPROhlr_20_2.0_20_2.0_1.5_1.0"

    result = ta.squeeze_pro(df.high, df.low, df.close, 20, 2, 20, 3, 2, 1)
    assert isinstance(result, DataFrame)
    assert result.name == "SQZPRO_20_2_20_3.0_2.0_1.0"

    result = ta.squeeze_pro(df.high, df.low, df.close, 20, 2, 20, 3, 2, 1, tr=False)
    assert isinstance(result, DataFrame)
    assert result.name == "SQZPROhlr_20_2_20_3.0_2.0_1.0"


def test_stc(df):
    result = ta.stc(df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "STC_10_12_26_0.5"


def test_stoch(df):
    result = ta.stoch(df.high, df.low, df.close, talib=False)
    assert isinstance(result, DataFrame)
    assert result.name == "STOCH_14_3_3"

    try:
        expected = tal.STOCH(df.high, df.low, df.close, 14, 3, 0, 3, 0)
        expecteddf = DataFrame({"STOCHk_14_3_0_3_0": expected[0], "STOCHd_14_3_0_3": expected[1]})
        pdt.assert_frame_equal(result, expecteddf)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.stoch(df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "STOCH_14_3_3"


def test_stochf(df):
    result = ta.stochf(df.high, df.low, df.close, talib=False)
    assert isinstance(result, DataFrame)
    assert result.name == "STOCHF_14_3"

    try:
        expected = tal.STOCHF(df.high, df.low, df.close, 14, 3, 0)
        expecteddf = DataFrame({"STOCHFk_14_3_0": expected[0], "STOCHFd_14_3_0": expected[1]})
        pdt.assert_frame_equal(result, expecteddf)
    except AssertionError:
        try:
            stochk_corr = ta.utils.df_error_analysis(result.iloc[:, 0], expected.iloc[:, 0])
            print(f"{stochk_corr=}")
            assert stochk_corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result.iloc[:, 0], CORRELATION, ex)

        try:
            stochd_corr = ta.utils.df_error_analysis(result.iloc[:, 1], expected.iloc[:, 1])
            print(f"{stochd_corr=}")
            assert stochd_corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result.iloc[:, 1], CORRELATION, ex)

    result = ta.stochf(df.high, df.low, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "STOCHF_14_3"


def test_stochrsi(df):
    # TV Correlation
    result = ta.stochrsi(df.close, talib=False)
    assert isinstance(result, DataFrame)
    assert result.name == "STOCHRSI_14_14_3_3"

    try:
        expected = tal.STOCHRSI(df.close, 14, 14, 3, 0)
        expecteddf = DataFrame({
            "STOCHRSIk_14_14_0_3": expected[0],
            "STOCHRSId_14_14_3_0": expected[1]
        })
        pdt.assert_frame_equal(result, expecteddf)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result.iloc[:, 0], expecteddf.iloc[:, 1])
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result.iloc[:, 0], CORRELATION, ex, newline=False)


def test_tmo(df):
    result = ta.tmo(df.open, df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "TMO_14_5_3"

    result = ta.tmo(df.open, df.close, compute_momentum=True)
    assert isinstance(result, DataFrame)
    assert result.name == "TMO_14_5_3"


def test_trix(df):
    result = ta.trix(df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "TRIX_30_9"


def test_td_seq(df):
    result = ta.td_seq(df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "TD_SEQ"


def test_tsi(df):
    result = ta.tsi(df.close)
    assert isinstance(result, DataFrame)
    assert result.name == "TSI_13_25_13"


def test_uo(df):
    result = ta.uo(df.high, df.low, df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "UO_7_14_28"

    try:
        expected = tal.ULTOSC(df.high, df.low, df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.uo(df.high, df.low, df.close)
    assert isinstance(result, Series)
    assert result.name == "UO_7_14_28"


def test_willr(df):
    result = ta.willr(df.high, df.low, df.close, talib=False)
    assert isinstance(result, Series)
    assert result.name == "WILLR_14"

    try:
        expected = tal.WILLR(df.high, df.low, df.close)
        pdt.assert_series_equal(result, expected, check_names=False)
    except AssertionError:
        try:
            corr = ta.utils.df_error_analysis(result, expected)
            print(f"{corr=}")
            assert corr > CORRELATION_THRESHOLD
        except Exception as ex:
            error_analysis(result, CORRELATION, ex)

    result = ta.willr(df.high, df.low, df.close)
    assert isinstance(result, Series)
    assert result.name == "WILLR_14"


# DataFrame Extension Tests
def test_ext_ao(df):
    df.ta.ao(append=True)
    assert df.columns[-1] == "AO_5_34"


def test_ext_apo(df):
    df.ta.apo(append=True)
    assert df.columns[-1] == "APO_12_26"


def test_ext_bias(df):
    df.ta.bias(append=True)
    assert df.columns[-1] == "BIAS_SMA_26"


def test_ext_bop(df):
    df.ta.bop(append=True)
    assert df.columns[-1] == "BOP"


def test_ext_brar(df):
    df.ta.brar(append=True)
    assert df.columns[-1] == "BR_26"


def test_ext_cci(df):
    df.ta.cci(append=True)
    assert df.columns[-1] == "CCI_14_0.015"


def test_ext_cfo(df):
    df.ta.cfo(append=True)
    assert df.columns[-1] == "CFO_9"


def test_ext_cg(df):
    df.ta.cg(append=True)
    assert df.columns[-1] == "CG_10"


def test_ext_cmo(df):
    df.ta.cmo(append=True)
    assert df.columns[-1] == "CMO_14"


def test_ext_coppock(df):
    df.ta.coppock(append=True)
    assert df.columns[-1] == "COPC_11_14_10"


def test_ext_crsi(df):
    df.ta.crsi(append=True)
    assert df.columns[-1] == "CRSI_3_2_100"


def test_ext_cti(df):
    df.ta.cti(append=True)
    assert df.columns[-1] == "CTI_12"


def test_ext_crsi(df):
    df.ta.crsi(append=True)
    assert df.columns[-1] == "CRSI_3_2_100"


def test_ext_er(df):
    df.ta.er(append=True)
    assert df.columns[-1] == "ER_10"


def test_ext_eri(df):
    df.ta.eri(append=True)
    assert list(df.columns[-2:]) == ["BULLP_13", "BEARP_13"]


def test_ext_fisher(df):
    df.ta.fisher(append=True)
    assert list(df.columns[-2:]) == ["FISHERT_9_1", "FISHERTs_9_1"]


def test_ext_inertia(df):
    df.ta.inertia(append=True)
    assert df.columns[-1] == "INERTIA_20_14"


def test_ext_kdj(df):
    df.ta.kdj(append=True)
    assert list(df.columns[-3:]) == ["K_9_3", "D_9_3", "J_9_3"]


def test_ext_kst(df):
    df.ta.kst(append=True)
    assert list(df.columns[-2:]) == ["KST_10_15_20_30_10_10_10_15", "KSTs_9"]


def test_ext_macd(df):
    df.ta.macd(append=True)
    columns = ["MACD_12_26_9", "MACDh_12_26_9", "MACDs_12_26_9"]
    assert list(df.columns[-3:]) == columns


def test_ext_mom(df):
    df.ta.mom(append=True)
    assert df.columns[-1] == "MOM_10"


def test_ext_pgo(df):
    df.ta.pgo(append=True)
    assert df.columns[-1] == "PGO_14"


def test_ext_ppo(df):
    df.ta.ppo(append=True)
    assert list(df.columns[-3:]) == ["PPO_12_26_9", "PPOh_12_26_9", "PPOs_12_26_9"]


def test_ext_psl(df):
    df.ta.psl(append=True)
    assert df.columns[-1] == "PSL_12"


def test_ext_pvo(df):
    df.ta.pvo(append=True)
    assert list(df.columns[-3:]) == ["PVO_12_26_9", "PVOh_12_26_9", "PVOs_12_26_9"]


def test_ext_qqe(df):
    df.ta.qqe(append=True)
    columns = [
        "QQE_14_5_4.236", "QQE_14_5_4.236_RSIMA",
        "QQEl_14_5_4.236", "QQEs_14_5_4.236"
    ]
    assert list(df.columns[-4:]) == columns


def test_ext_roc(df):
    df.ta.roc(append=True)
    assert df.columns[-1] == "ROC_10"


def test_ext_rsi(df):
    df.ta.rsi(append=True)
    assert df.columns[-1] == "RSI_14"


def test_ext_rsx(df):
    df.ta.rsx(append=True)
    assert df.columns[-1] == "RSX_14"


def test_ext_rvgi(df):
    df.ta.rvgi(append=True)
    assert list(df.columns[-2:]) == ["RVGI_14_4", "RVGIs_14_4"]


def test_ext_slope(df):
    df.ta.slope(append=True)
    assert df.columns[-1] == "SLOPE_1"


def test_ext_smi(df):
    df.ta.smi(append=True)
    columns = ["SMI_5_20_5_1.0", "SMIs_5_20_5_1.0", "SMIo_5_20_5_1.0"]
    assert list(df.columns[-3:]) == columns


def test_ext_squeeze(df):
    df.ta.squeeze(append=True)
    columns = ["SQZ_20_2.0_20_1.5", "SQZ_ON", "SQZ_OFF", "SQZ_NO"]
    assert list(df.columns[-4:]) == columns


def test_ext_squeeze_pro(df):
    df.ta.squeeze_pro(append=True)
    columns = ["SQZPRO_ON_NORMAL", "SQZPRO_ON_NARROW", "SQZPRO_OFF", "SQZPRO_NO"]
    assert list(df.columns[-4:]) == columns


def test_ext_stc(df):
    df.ta.stc(append=True)
    columns = ["STC_10_12_26_0.5", "STCmacd_10_12_26_0.5", "STCstoch_10_12_26_0.5"]
    assert list(df.columns[-3:]) == columns


def test_ext_stoch(df):
    df.ta.stoch(append=True)
    columns = ["STOCHk_14_3_3", "STOCHd_14_3_3", "STOCHh_14_3_3"]
    assert list(df.columns[-3:]) == columns


def test_ext_stochf(df):
    df.ta.stochf(append=True)
    assert list(df.columns[-2:]) == ["STOCHFk_14_3", "STOCHFd_14_3"]


def test_ext_stochrsi(df):
    df.ta.stochrsi(append=True)
    assert list(df.columns[-2:]) == ["STOCHRSIk_14_14_3_3", "STOCHRSId_14_14_3_3"]


def test_ext_td_seq(df):
    df.ta.td_seq(append=True)
    assert list(df.columns[-2:]) == ["TD_SEQ_UPa", "TD_SEQ_DNa"]


def test_ext_tmo(df):
    df.ta.tmo(append=True)
    columns = ["TMO_14_5_3", "TMOs_14_5_3", "TMOM_14_5_3", "TMOMs_14_5_3"]
    assert list(df.columns[-4:]) == columns


def test_ext_trix(df):
    df.ta.trix(append=True)
    assert list(df.columns[-2:]) == ["TRIX_30_9", "TRIXs_30_9"]


def test_ext_tsi(df):
    df.ta.tsi(append=True)
    assert list(df.columns[-2:]) == ["TSI_13_25_13", "TSIs_13_25_13"]


def test_ext_uo(df):
    df.ta.uo(append=True)
    assert df.columns[-1] == "UO_7_14_28"


def test_ext_willr(df):
    df.ta.willr(append=True)
    assert df.columns[-1] == "WILLR_14"
