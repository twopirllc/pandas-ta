# -*- coding: utf-8 -*-
import datetime
from os import read
from pathlib import Path
from json import load as json_load
from json import loads as json_loads
from json import dump as json_dump
from json import dumps as json_dumps

from time import sleep as tsleep
from matplotlib.pyplot import axis

import numpy as np
import pandas as pd

# import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# from matplotlib import rc
# import mplfinance as mpf
# from tqdm.notebook import trange, tqdm
import streamlit as st
from streamlit.state.session_state import SessionState

import pandas_ta as ta


dt_today = datetime.datetime.now()
e = pd.DataFrame()

pta_session = {}

strategy_sample = \
"""{
    "name": "Sample JSON Strategy",
    "description": "Sample JSON Strategy Test",
    "ta": [
        {"kind": "ema", "length": 10, "sma": false},
        {"kind": "sma", "length": 50, "talib": false},
        {
            "kind": "bbands",
            "talib": true,
            "col_numbers": [0, 1, 2],
            "col_names": ["BBL", "BBM", "BBU"]
        },
        {
            "kind": "atr",
            "length": 50,
            "talib": true,
            "col_names": ["ATR"]
        }
    ]
}"""

if "pta" not in st.session_state:
    st.session_state["pta"] = pta_session

print(f"[!] st.session_state: {st.session_state}\n")



def _chart():
    pass

def _count_down_container(message:str = None, n:int = 1):
    """https://docs.streamlit.io/library/api-reference/layout/st.empty"""
    with st.empty():
        for seconds in range(n):
            if message is None:
                st.write(f"⏳ {seconds} seconds have passed")
            else:
                st.write(message)
            tsleep(1)

        if message is None: st.write("✔️ Times up!")
        st.empty()


def _is_st_column(column):
    if column is None: return st
    return column if isinstance(column, st._DeltaGenerator) else st


@st.cache(ttl=60, show_spinner=True)
def _load_file(file):
    """Load file of type st.UploadedFile"""
    suffix = file.name.split(".")[1]
    result = None
    if suffix == "csv":
        result = pd.read_csv(file)
    elif suffix == "json":
        result = pd.read_json(file)
    elif suffix == "pkl":
        result = pd.read_pickle(file)
    else: # Default
        result = pd.read_csv(file)
    return result


def _max_width_(pct_width:int = None):
    """"https://discuss.streamlit.io/t/custom-render-widths/81/8"""
    if pct_width is None:
        max_width_str = f"max-width: 2000px;"
    else:
        max_width_str = f"max-width: {pct_width}%;"

    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </
    """, unsafe_allow_html=True)


def _success(msg:str = "Success!", secs:float = 1.25):
    ready = st.success(msg)
    tsleep(secs)
    ready.empty()


def _talist2tuple(ta_list:list):
    """Convert "col_numbers" and "col_names" list values to tuples"""
    for indicator in ta_list:
        if "col_numbers" in indicator and len(indicator["col_numbers"]):
            indicator["col_numbers"] = tuple(indicator["col_numbers"])
        if "col_names" in indicator and len(indicator["col_names"]):
            indicator["col_names"] = tuple(indicator["col_names"])
    return ta_list


def permute_col(x: pd.Series):
    """Permute values in a Pandas Series"""
    return np.random.permutation(x)

def shuffle_col(x: pd.Series, frac:float = 1.0):
    """Shuffle values and reset index in a Pandas Series"""
    _ = x.sample(frac=frac)
    _.index = x.index
    return _


def check_strategy(json_text, as_bool:bool = False):
    strat = json_loads(json_text)
    if "name" not in strat or "ta" not in strat: return False

    if isinstance(strat["ta"], list) and len(strat["ta"]) > 0:
        strat["ta"] = _talist2tuple(strat["ta"])
    else:
        return False

    result = None
    if "description" in strat:
        result = ta.Strategy(name=strat["name"], ta=strat["ta"], description=strat["description"])
    else:
        result = ta.Strategy(name=strat["name"], ta=strat["ta"])

    if as_bool:
        return True if result is not None else False
    return result


def exclude_indicators():
    return [
        "above", "above_value", "below", "below_value", "cross", "cross_value"
    ]


def load_strategy(path:str):
    strat, json_strat = None, json_load(open(path))
    strat = json_strat[0] if isinstance(json_strat, list) and len(json_strat) == 1 else json_strat

    for indicator in strat["ta"]:
        if "col_numbers" in indicator and len(indicator["col_numbers"]):
            indicator["col_numbers"] = tuple(indicator["col_numbers"])
        if "col_names" in indicator and len(indicator["col_names"]):
            indicator["col_names"] = tuple(indicator["col_names"])

    if strat is not None and hasattr(strat, "description") and len(strat):
        return ta.Strategy(name=strat["name"], ta=strat["ta"], description=strat["description"])
    else:
        return ta.Strategy(name=strat["name"], ta=strat["ta"])


def localfile_data(title="### Upload"):
    # st.markdown(title)
    base = st.container()
    with base:
        parameters = st.container()
        with parameters:

            # st.markdown("#### Parameters")

            # lf_p11, lf_p12, lf_p13 = st.columns(3)

            # fpath = lf_p11.text_input("Directory", ".", key="local_dir")
            # file_suffix = lf_p12.selectbox(f"File Type", ["csv", "json"])
            # fpath = return_file(fpath, file_suffix)
            # file_ = lf_p13.selectbox(f"{file_suffix.upper()} File", fpath)


            # uploaded_file = st.file_uploader("Choose a file", type=["csv", "json"], key="uploadfile")
            # lf_p21, lf_p22 = st.columns(2)
            localdf = pd.DataFrame()
            file_ = st.file_uploader("Choose a file", type=["csv", "json"], key="uploaded_file")
            if file_ is not None:
                file_suffix = file_.name.split(".")[1]
                # fd = file_.read()
                # st.write([x for x in dir(file_) if not x.startswith('_')])
                _success(f"{file_.name} Ready")

                if "local_file_name" not in st.session_state["pta"]:
                    st.session_state["pta"]["local_file_name"] = file_.name

                # st.write(st.session_state)

                if file_suffix == "csv":
                    localdf = pd.read_csv(file_)
                elif file_suffix == "json":
                    localdf = pd.read_json(file_)
                else: pass

                if "localdf" not in st.session_state["pta"]:
                    st.session_state["pta"]["localdf"] = localdf

            if not localdf.empty:
                st.markdown("### Chart")
                localdf.name = Path(file_).name.split(".")[0]
                localdf_full = localdf.copy()
                # pdf, vdf = yf_chart(localdf, fig_size=(16, 8), stats=False, linreg=False)
                # st.pyplot(pdf.figure)
                # if vdf is not None: st.pyplot(vdf.figure)
                _success(f"{localdf.name} Ready")

                if st.checkbox(f"Show DataFrame: {localdf.name} | {localdf.shape}", False, key="show_localdf"): st.dataframe(localdf_full)


def localfile_selector(column=None, title="### Upload"):
    column = _is_st_column(column)
    column.markdown(title)
    # localfile_data()
    with st.container():
        file = st.file_uploader("Choose a file", type=["csv", "json"], key="uploaded_file")
        if file is not None:
            file_suffix = file.name.split(".")[1]
            # fd = file_.read()
            # st.write([x for x in dir(file_) if not x.startswith('_')])
            _success(f"{file.name} Ready")
            # ready = st.success(f"{file.name} Ready")
            # tsleep(1.2)
            # ready.empty()

            if "local_file_name" not in st.session_state["pta"]:
                st.session_state["pta"]["local_file_name"] = file.name

            if file_suffix == "csv":
                localdf = pd.read_csv(file)
            if file_suffix == "json":
                localdf = pd.read_json(file)

            if "localdf" not in st.session_state["pta"]:
                st.session_state["pta"]["localdf"] = localdf

            if not localdf.empty:
                st.markdown("### Chart")
                # st.markdown(st.session_state["pta"]["localdf"])
                # st.markdown(type(st.session_state["pta"]["localdf"]))

                if st.checkbox(f"Show DataFrame: {file.name} | {localdf.shape}", False, key="show_localdf"): st.dataframe(localdf)
        else:
            if "local_file_name" not in st.session_state["pta"]:
                st.session_state["pta"]["local_file_name"] = None
            # st.write(f"file: {file}")



def return_file(path, ftype:str="json"):
    result, p = [], Path(path)
    for item in p.iterdir():
        if item.is_file() and item.suffix == f".{ftype}":
            result.append(item)

    if len(result) == 0: result.append("")
    return sorted(result)


def sample_chart(df:pd.DataFrame, fig_size=(16, 5), colors:list = None, stats:bool = False, idx:int = None, linreg:bool = None):
    if df.empty: return
    idx = int(idx) if idx is not None and idx >= 0 else None
    linreg = bool(linreg) if linreg is not None and isinstance(linreg, bool) else False

    title_ = f"{df.name}" if idx is None else f"{idx}: {df.name}"

    if colors is not None and isinstance(colors, list) and len(colors):
        colors = ["black", "gray", "green", "lightgreen", "pink", "red", "orange", "orange"]
    else:
        colors = None

    if stats:
        min_, max_ = np.min(df.values), np.max(df.values)
        mu_, std_ = np.mean(df.values), np.std(df.values)
        df["mu"] = mu_
        df["mu-2std"] = mu_ - 2 * std_
        df["mu-std"] = mu_ - std_
        df["mu+std"] = mu_ + std_
        df["mu+2std"] = mu_ + 2 * std_
        df["min"] = min_
        df["max"] = max_

        if linreg:
            df.ta.linreg(close=df.iloc[:,0], length=df.shape[0], fill_method="bfill", append=True)
            if colors is not None: colors.append("magenta")

    if colors is not None:
        fig = df.plot(figsize=fig_size, title=title_, color=colors, grid=True, legend=False if len(df.columns) > 10 else True)
    else:
        fig = df.plot(figsize=fig_size, title=title_, grid=True, legend=False if len(df.columns) > 10 else True)
    return fig



def stochastic_data(title="### Stochastic Options"):
    st.markdown("###")
    st.markdown(title)
    base = st.container()
    # if st.session_state["sb_stochastic_help"]:
        # st.write("HELP")

    with base:
        with st.form("stochastic_params"):
            stoch_parameters = st.container()
            with stoch_parameters:
                st.markdown("#### Parameters")
                stoch_s11, stoch_s12, stoch_s13 = st.columns(3)
                sp_ticker = stoch_s11.text_input("Ticker", key="stochastic_ticker")
                sp_process = stoch_s12.selectbox("Process", ta_sample_processes())
                sp_noise = stoch_s13.selectbox("Noise", ta_sample_noises())

                stoch_s21, stoch_s22, stoch_s23 = st.columns(3)
                sp_s0 = stoch_s21.number_input("Initial", value=42.00, min_value=0.00001, step=1e-6, format="%.5f")
                sp_length = stoch_s22.number_input("Length", value=50, min_value=2, step=1)
                sp_random_number = stoch_s23.number_input("Random # (0 is random)", value=10, min_value=0, step=1)

                stoch_s31, stoch_s32, stoch_s33 = st.columns(3)
                sp_future = stoch_s31.checkbox("Future", False)
                sp_positive = stoch_s32.checkbox("Positive", False)
                sp_stats = stoch_s33.checkbox("Stats", False, key="sp_stats")

            stoch_addparameters = st.container()
            with stoch_addparameters:
                st.markdown("#### Additional Parameters")
                stoch_s41, stoch_s42, stoch_s43, stoch_s44 = st.columns(4)
                sp_speed = stoch_s41.number_input("Speed", value=1.00, step=1e-6, format="%.5f")
                sp_hurst = stoch_s42.number_input("Hurst", value=0.5, min_value=0.0, max_value=1.0, step=1e-6, format="%.5f")
                sp_scale = stoch_s43.number_input("Scale", value=1.00, step=1e-6, format="%.5f")
                sp_freq = stoch_s44.selectbox("Date Freq", ["D", "B", "W", "M", "H", "BH", "T", "S", "L", "U", "N", "MS", "BMS", "SM", "SMS", "Q", "QS", "A", "AS", "BA", "BAS"])

                stoch_s51, stoch_s52, stoch_s53, stoch_s54 = st.columns(4)
                sp_drift = stoch_s51.number_input("Drift", value=0.00, step=1e-6, format="%.5f")
                sp_volatility = stoch_s52.number_input("Volatility", value=1.00, step=1e-6, format="%.5f")
                sp_b = stoch_s53.number_input("b", value=0.01, step=1e-6, format="%.5f")
                sp_t = stoch_s54.number_input("t", value=1.00, step=1e-6, format="%.5f")

            sample_params = {
                "name": None if len(sp_ticker) == 0 else sp_ticker.upper(),
                "s0": sp_s0, "length": sp_length,
                "process": sp_process, "noise": sp_noise, "scale": sp_scale,
                "drift": sp_drift, "volatility": sp_volatility,
                "b": sp_b, "t": sp_t, "speed": sp_speed, "hurst": sp_hurst,
                "future": sp_future, "positive": sp_positive,
                "random_number": sp_random_number if sp_random_number > 0 else None,
                "freq": sp_freq
            }

            mc_parameters = st.container()
            with mc_parameters:
                st.markdown("#### Montecarlo Simulation Parameters")
                # montecarlo = st.checkbox("Simulate", False, key="stoch_montecarlo") # False
                # if montecarlo:
                stoch_s61, stoch_s62, stoch_s63, stoch_s64 = st.columns(4)
                sp_mc_count = stoch_s61.number_input("Simulations", value=5, min_value=2, max_value=10_000, step=1)
                sp_mc_return_type = stoch_s62.selectbox("Return", ["percent", "log"])
                sp_mc_selection = stoch_s63.selectbox("Selection", ["permutation", "shuffle", "both"])
                sp_mc_range = stoch_s64.slider("MC Columns", value=(0, sp_mc_count), min_value=0, max_value=sp_mc_count)

            st.markdown("####")
            submitted = st.form_submit_button("Submit")

        st.markdown("###")
        st.markdown("submitted")
        st.write(submitted)
        # samplenp = ta.sample(**sample_params).np

        df = ta.sample(**sample_params).df if submitted else ta.df

        if "sampledf" not in st.session_state["pta"]:
            st.session_state["pta"]["sampledf"] = df

        if not df.empty:
            # st.markdown(f"### Chart {sampledf.name}")
            st.markdown(f"#### {df.name}")
            if st.checkbox(f"Show Chart", True, key="show_sampledf"):
                sample_fig = sample_chart(df, fig_size=(stoch_plot_width, stoch_plot_height), colors=None, stats=sp_stats).figure
                st.pyplot(sample_fig)
            _success(f"Sample Ready")
            # ready = st.success("Sample Ready")
            # tsleep(1.2)
            # ready.empty()

            if st.checkbox(f"Show DataFrame", True, key="show_sampledf"): st.dataframe(df)

        mcdf = pd.DataFrame()
        # if montecarlo:
        mcdf = df.copy()
        # mcdf = pd.DataFrame(np.tile(sampledf.values, sp_mc_count))
        if sp_mc_return_type == "percent":
            mcdf_returns = mcdf.ta.percent_return(cumulative=False, fillna=0, append=True)
        else:
            mcdf_returns = mcdf.ta.log_return(cumulative=False, fillna=0, append=True)

        return_tilesdf = pd.DataFrame(np.tile(mcdf_returns.values, (sp_mc_count, 1))).T

        if sp_mc_selection == "permutation":
            return_tilesdf.iloc[1:,1:] = return_tilesdf.iloc[1:,1:].apply(permute_col)
        if sp_mc_selection == "shuffle":
            return_tilesdf.iloc[1:,1:] = return_tilesdf.iloc[1:,1:].apply(shuffle_col)
        if sp_mc_selection == "both":
            return_tilesdf.iloc[1:,1:] = return_tilesdf.iloc[1:,1:].apply(permute_col)
            return_tilesdf.iloc[1:,1:] = return_tilesdf.iloc[1:,1:].apply(shuffle_col)

        pricesdf = sp_s0 * (1 + return_tilesdf).cumprod()

        mcdf = pricesdf.copy()
        mcdf.index = df.index
        mcdf = mcdf.iloc[:,sp_mc_range[0]:sp_mc_range[1]]
        # df.name = "YOU" if len(sp_ticker) == 0 else sp_ticker.upper()
        # df.name = sp_ticker.upper()
        # mcdf.name = f"MC{sp_mc_count} - {df.name}"
        mcdf.name = df.name

        if not mcdf.empty:
            # st.markdown(f"### Chart {mcdf.name}")
            sim_statsdf = mcdf.describe(include="all").T
            sim_mean = sim_statsdf["mean"].mean()
            sim_std = sim_statsdf["std"].mean()

            st.markdown("---")
            st.markdown(f"#### {mcdf.name}")
            st.markdown(f"**{sp_mc_return_type.title()} Return Simulations**: {sp_mc_count}, **Mean**: {round(sim_mean, 5)}, **Stdev**: {round(sim_std, 5)}")

            if st.checkbox(f"Show Chart", True, key="show_mcdf_chart"):
                mc_fig = sample_chart(mcdf, fig_size=(stoch_plot_width, stoch_plot_height), colors=None).figure
                st.pyplot(mc_fig)
            _success(f"MC Ready")
            # ready = st.success("MC Ready")
            # tsleep(1.2)
            # ready.empty()

            # if not st.checkbox(f"MC Simulations Minimized", True, key="show_mcdf"): st.dataframe(mcdf)
            if st.checkbox(f"Show DataFrame", True, key="show_mcdf_df"):
                st.markdown("###")
                st.dataframe(mcdf)
                st.markdown("###")
                # st.dataframe(mcdf.cumsum(axis=0))
                # st.markdown("###")
                # st.dataframe(mcdf.describe(include="all"))
                # st.markdown("###")
                # st.dataframe()


def stochastic_selector(column=None, title="### Stochastic Processes"):
    column = _is_st_column(column)
    _help_txt = "help(ta.sample)"
    column.markdown(title)
    sandbox = column.checkbox("Options", False, "stochastic_sandbox")
    if sandbox: stochastic_data()
    expand_stochastic = column.checkbox(_help_txt, False, "expand_stochastic")
    if expand_stochastic: st.help(ta.sample)


def ta_sample_noises():
    return ta.sample().noises

def ta_sample_processes():
    return ta.sample().processes


def yf_chart(df:pd.DataFrame, fig_size=(16, 10), stats:bool = False, linreg:bool = None):
    if df.empty: return
    linreg = bool(linreg) if linreg is not None and isinstance(linreg, bool) else False

    title_ = f"{df.name}" if hasattr(df, "name") else "Local"
    colors = ["black", "gray", "green", "lightgreen", "pink", "red", "orange", "orange"]

    volumedf = pd.DataFrame()
    if "volume" in df.columns:
        volumedf = pd.DataFrame(df["volume"])
        del df["volume"]

    if stats:
        min_, max_ = np.min(df.values), np.max(df.values)
        mu_, std_ = np.mean(df.values), np.std(df.values)
        df["mu"] = mu_
        df["mu-2std"] = mu_ - 2 * std_
        df["mu-std"] = mu_ - std_
        df["mu+std"] = mu_ + std_
        df["mu+2std"] = mu_ + 2 * std_
        df["min"] = min_
        df["max"] = max_

        if linreg:
            df.ta.linreg(close=df.iloc[:,0], length=df.shape[0], fill_method="bfill", append=True)
            colors.append("magenta")

    if "open" in df.columns: del df["open"]
    if "high" in df.columns: del df["high"]
    if "low" in df.columns: del df["low"]

    price_fig = df.plot(figsize=fig_size, title=title_, color=colors, grid=True)

    if volumedf.empty:
        volume_fig = None
    else:
        volume_fig = volumedf.plot(figsize=(fig_size[0], 2.5), kind="area", stacked=False, title=f"{title_} Volume", color=["gray"], alpha=0.6, grid=True)
    return price_fig, volume_fig


def yfinance_data(title="### Yahoo Finance Sandbox"):
    st.markdown(title)
    base = st.container()
    with base:
        stoch_parameters = st.container()
        with stoch_parameters:
            st.markdown("#### Parameters")
            with st.form("yfinance_form"):

                yf_p11, yf_p12, yf_p13 = st.columns(3)
                yf_ticker = yf_p11.text_input("Ticker", "SPY", key="yf_ticker")

                yf_period = yf_p12.selectbox("Period", "1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max".split(","))
                yf_interval = yf_p13.selectbox("Interval", "1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo".split(","))

                yf_p21, yf_p22, yf_p23 = st.columns(3)
                yf_dividends = yf_p21.checkbox("Dividends", False)
                yf_stocksplits = yf_p22.checkbox("Stock Splits", False)
                yf_stats = yf_p23.checkbox("Stats", False, key="yf_stats")

                yf_params = {
                    "ticker": "SPY" if len(yf_ticker) == 0 else yf_ticker.upper(),
                    "period": yf_period,
                    "interval": yf_interval,
                    "lc_cols": True
                }

                yf_submitted = st.form_submit_button("Submit")

            yfdf = ta.df
            if yf_submitted:
                yfdf = ta.df.ta.ticker(**yf_params)

                _drop_cols = []
                if not yf_dividends: _drop_cols.append("dividends")
                if not yf_stocksplits: _drop_cols.append("stock splits")
                yfdf.drop(columns=_drop_cols, errors="ignore", inplace=True)

                if "yfdf" not in st.session_state["pta"]:
                    st.session_state["pta"]["yfdf"] = yfdf

                if not yfdf.empty:
                    st.markdown("### Chart")
                    yfdf_full = yfdf.copy()

                    _success(f"{yf_ticker.upper()} Ready")
                    # ready = st.success(f"{yf_ticker.upper()} YF Data Ready")
                    # tsleep(1.25)
                    # ready.empty()
                    # pdf, vdf = yf_chart(yfdf, fig_size=(16, 8), stats=yf_stats, linreg=True)
                    # st.pyplot(pdf.figure)
                    # st.pyplot(vdf.figure)

def yfinance_selector(column=None, title="### Yahoo Finance"):
    column = _is_st_column(column)
    _help_txt = "help(ta.yf)"
    column.markdown(title)
    sandbox = column.checkbox("Options", False, "yfinance_options")
    if sandbox: yfinance_data()
    expand_yfinance = column.checkbox(_help_txt, False, "expand_yfinance")
    if expand_yfinance: st.help(ta.yf)


### Streamlit Sections


def description():
    expander = st.expander("", True)
    with expander:
        bcol1, logocol, bcol2 = st.columns(3)
        with bcol1: st.write("")
        with logocol: st.image("https://raw.githubusercontent.com/twopirllc/pandas-ta/main/images/logo.png")
        with bcol2: st.write("")

        st.markdown("""
        # Pandas TA
        ## A Technical Analysis Library in Python 3
        ####""")

        st.markdown("""
        [![license](https://img.shields.io/github/license/twopirllc/pandas-ta)](#license)
        [![Python Version](https://img.shields.io/pypi/pyversions/pandas-ta?style=flat)](https://pypi.org/project/pandas_ta/)
        [![PyPi Version](https://img.shields.io/pypi/v/pandas-ta?style=flat)](https://pypi.org/project/pandas_ta/)
        [![Package Status](https://img.shields.io/pypi/status/pandas-ta?style=flat)](https://pypi.org/project/pandas_ta/)
        [![Downloads](https://img.shields.io/pypi/dm/pandas_ta?style=flat)](https://pypistats.org/packages/pandas_ta)
        [![Stars](https://img.shields.io/github/stars/twopirllc/pandas-ta?style=flat)](#stars)
        [![Forks](https://img.shields.io/github/forks/twopirllc/pandas-ta?style=flat)](#forks)
        [![Used By](https://img.shields.io/badge/used_by-184-orange.svg?style=flat)](#usedby)
        [![Contributors](https://img.shields.io/github/contributors/twopirllc/pandas-ta?style=flat)](#contributors)
        [![Issues](https://img.shields.io/github/issues-raw/twopirllc/pandas-ta?style=flat)](#issues)
        [![Closed Issues](https://img.shields.io/github/issues-closed-raw/twopirllc/pandas-ta?style=flat)](#closed-issues)
        [![Buy Me a Coffee](https://img.shields.io/badge/buy_me_a_coffee-orange.svg?style=flat)](https://www.buymeacoffee.com/twopirllc)

        ###
        _Pandas Technical Analysis_ (**Pandas TA**) is an easy to use library that leverages the Pandas package with more than 140 Indicators and Utility functions and more than 60 TA Lib Candlestick Patterns. Many commonly used indicators are included, such as: _Candle Pattern_(**cdl_pattern**), _Simple Moving Average_ (**sma**) _Moving Average Convergence Divergence_ (**macd**), _Hull Exponential Moving Average_ (**hma**), _Bollinger Bands_ (**bbands**), _On-Balance Volume_ (**obv**), _Aroon & Aroon Oscillator_ (**aroon**), _Squeeze_ (**squeeze**) and **_many more_**.

        ###
        ### Example Streamlit Application
        **This** is a Basic [Streamlit](https://streamlit.io/) Application using the following packages: ```matplotlib```, ```numpy```, ```pandas```, ```pandas_ta```, ```stochastic```, ```streamlit```, ```yfinance```. It is currently not optimized but Pull Requests are open for those that want to help make it better. :sunglasses: It's purpose is to help the user easily find help on indicators and functions as well as allow them to download or generate data for analysis. While this has been initially built with ```matplotlib``` for charting, feel free to modify and include your charts that [Streamlit Charts](https://docs.streamlit.io/library/api-reference/charts) supports.

        To get the most of this App, install:
        """)
        st.code("(env) $ pip install matplotlib numpy pandas pandas_ta stochastic streamlit yfinance", "shell")

        st.markdown("""Run the App and check your browser tab for the application.""")
        st.code("(env) $ streamlit run pta_streamlit.py", "shell")
        st.markdown("""
        ####
        ### For more information
        See the **Pandas TA** [README](https://github.com/twopirllc/pandas-ta) for more details on basic usage and the [Example Notebooks](https://github.com/twopirllc/pandas-ta/tree/main/examples) for detailed usage.
        """)


def installation(title="**Installation**"):
    expander = st.expander("", True)
    with expander:
        st.markdown(f"""
        {title}
        ===================

        Stable
        ------
        The ```pip``` version is the last stable release. Version: *0.3.14b*""")
        st.code("(env) $ pip install pandas_ta", "shell")

        st.markdown("""
        Latest Version
        --------------
        Best choice! Version: *0.3.32b*
        """)
        st.code("(env) $ pip install -U git+https://github.com/twopirllc/pandas-ta", "shell")

        st.markdown("""
        Cutting Edge
        ------------
        This is the _Development Version_ which could have bugs and other undesireable side effects. Use at own risk!
        """)
        st.code("(env) $ pip install -U git+https://github.com/twopirllc/pandas-ta.git@development", "shell")


def tahelp(title="Help"):
    expander = st.expander("", True)
    with expander:
        st.markdown(f"""
        ## {title}
        """)
        st.code("""
import pandas as pd
import pandas_ta as ta

# Create a DataFrame so 'ta' can be used.
df = pd.DataFrame()

# Help about this, 'ta', extension
help(df.ta)

# List of all indicators
df.ta.indicators()

# Help about an indicator such as bbands
help(ta.bbands)
        """)

        st.markdown("####")
        st.markdown("""### Categories""")
        all_tai = [""]
        all_tai += e.ta.indicators(as_list=True, exclude=exclude_indicators())
        ind_help = st.selectbox(f"Indicators [{len(all_tai) - 1}]", all_tai)
        expand_indicators = st.checkbox("Expand", True, "expand_indicators")
        if expand_indicators and hasattr(ta, ind_help):
            st.help(getattr(ta, ind_help))

        st.markdown("####")
        other = [
            "", "category_files", "combination", "df_dates", "df_month_to_date",
            "df_quarter_to_date", "df_year_to_date", "erf", "geometric_mean",
            "get_drift", "get_offset", "hpoly", "inv_norm",
            "is_datetime_ordered", "linear_regression", "log_geometric_mean",
            "non_zero_range", "pascals_triangle", "sample", "signed_series",
            "symmetric_triangle", "tal_ma", "to_utc", "unsigned_differences",
            "verify_series", "yf", "zero"
        ]
        other_help = st.selectbox(f"Other [{len(other) - 1}]", other)
        expand_other = st.checkbox("Expand", True, "expand_other")
        if expand_other and hasattr(ta, other_help):
            st.help(getattr(ta, other_help))


def data(title="## Data"):

    expander = st.expander("", True)
    with expander:
        st.markdown(title)
        st.markdown("""**Pandas TA** includes wrappers around ```stochastic```, to generate sample realizations,
        or ```yfinance```, download US Market data from Yahoo Finance. If you have local _csv_ or _json_ files, you can import them from the left sidebar under "Local".""")

        # st.write(locals())
        # st.write(st.session_state)
        if df is not None:# and not df.empty:
            st.markdown("### Local File")
            st.markdown("###")
            st.markdown(f"**Shape**: {df.shape}")
            # st.markdown(f"**Index**: {', '.join(df.index)}")
            st.markdown(f"**Index**: {df.index}, **Datetime Ordered**: {ta.is_datetime_ordered(df)}")
            st.markdown(f"**Columns**: {', '.join(df.columns)}")
            if st.checkbox("Set Index", True, key="df_set_index"):
                index_col = st.selectbox("Index by:", [""] + list(df.columns))
                st.markdown(f"### index_col: {index_col}")
                if index_col:
                    df.set_index(pd.DatetimeIndex(df[index_col]), inplace=True, drop=True)
                    df.drop(index_col, axis=1, inplace=True)

            st.markdown(f"### {df.name} Details")
            df_detail_11, df_detail_12 = st.columns(2)
            df_detail_11.markdown(f"**Start**: {df.index[0]}")
            df_detail_12.markdown(f"**End**: {df.index[-1]}")

                    # df.set_index(pd.DatetimeIndex(index_col), drop=True)
            st.dataframe(df)
        # col11, col12 = st.columns(2)
        # if ta.Imports["stochastic"] and ta.Imports["yfinance"]:
        #     stochastic_selector(col11)
        #     yfinance_selector(col12)
        # elif ta.Imports["stochastic"]:
        #     stochastic_selector(col11)
        #     with col12.container():
        #         st.markdown("#### For Yahoo Finance Data")
        #         st.code("$ pip install yfinance", "shell")
        # elif ta.Imports["yfinance"]:
        #     yfinance_selector(col11)
        #     with col12.container():
        #         st.markdown("#### For Stochastic Data")
        #         st.code("$ pip install stochastic", "shell")
        # else: pass


def analysis(title="Analysis"):
    expander = st.expander("", True)
    with expander:
        st.markdown(f"""
        ## {title}
        Pandas TA has three [Programming Conventions](https://github.com/twopirllc/pandas-ta#programming-conventions) to support your programming "style". Below are examples of each convention with indicators shown on the README.
        """)
        st.code("""
# Standard imports
import pandas as pd
import pandas_ta as ta
        """)

        st.markdown("####")
        st.markdown("""### Data""")
        st.markdown("Select one of the data source options from the Data section.")

        df_ = pd.DataFrame()
        if "sampledf" in st.session_state["pta"]:
            _success("Using Stochastic Data.")
            df_ = st.session_state["pta"]["sampledf"]
        if "localdf" in st.session_state["pta"] and st.session_state["pta"]["local_file_name"] is not None:
            local_file_name = st.session_state["pta"]["local_file_name"]
            _success(f"Using local file: {local_file_name}")
            df_ = st.session_state["pta"]["localdf"]
        if "yfdf" in st.session_state["pta"]:
            _success("Using Yahoo Finance Download.")
            df_ = st.session_state["pta"]["yfdf"]
        if df_.empty:
            st.info("No ohlcv data selected from 'Data' Section")

        if not df_.empty:
            st.markdown("#")

            expand_standard_style = st.checkbox("Show Standard Style", False, "expand_standard_style")
            if expand_standard_style:
                st.markdown("##")
                st.markdown("""## Standard (TA Lib style)""")
                with st.echo():
                    df = df_.copy()
                    sma10 = ta.sma(df["close"], length=10)
                    donchiandf = ta.donchian(df["high"], df["low"], lower_length=10, upper_length=15)
                    ema10_ohlc4 = ta.ema(ta.ohlc4(df["open"], df["high"], df["low"], df["close"]), length=10)
                    # You handle the input/output
                    sma10
                    donchiandf
                    ema10_ohlc4

            expand_df_style = st.checkbox("Show DataFrame Extension Style", False, "expand_df_style")
            if expand_df_style:
                st.markdown("##")
                st.markdown("""### DataFrame Extension""")
                with st.echo():
                    df = df_.copy()
                    sma10 = df.ta.sma(length=10, append=True)
                    df.ta.ema(close=df.ta.ohlc4(append=True), length=10, suffix="OHLC4", append=True)
                    donchiandf = df.ta.donchian(lower_length=10, upper_length=15, append=True)
                    # Append with 'append=True' when using the DataFrame Extension .ta.
                    df
                    # As well as Standard Style returns
                    sma10
                    donchiandf

            expand_pta_style = st.checkbox("Show Pandas TA Style", False, "expand_pta_style")
            if expand_pta_style:
                st.markdown("##")
                st.markdown("""### Pandas TA Strategy""")
                with st.echo():
                    df = df_.copy()
                    # (1) Create the Strategy
                    MyStrategy = ta.Strategy(
                        name="DCSMA10",
                        ta=[
                            {"kind": "ohlc4"},
                            {"kind": "sma", "length": 10},
                            {"kind": "donchian", "lower_length": 10, "upper_length": 15},
                            {"kind": "ema", "close": "OHLC4", "length": 10, "suffix": "OHLC4"},
                        ]
                    )

                    # (2) Run the Strategy
                    df.ta.strategy(MyStrategy)
                    df


def strategy_checker(title="## Strategy Checker"):
    # expander = st.expander("", True)
    # with expander:
    with st.expander("", True):
        st.markdown(title)
        st.markdown("""
        Check your **Pandas TA** Strategy code.

        When testing JSON Strategy code, use array notation and _not_ tuple notation for 'col_names' and 'col_numbers' keywords. The arrays _will_ be converted to tuples in the process.
        """)

        # strategy = None
        with st.form(key="json_strategy_checker"):
            if "strategy_txt" not in st.session_state["pta"]:
                st.session_state["pta"]["strategy_txt"] = strategy_sample

            json_strategy_text = st.text_area("Paste JSON below.", height=300, value=st.session_state["pta"]["strategy_txt"])
            submit_json_strategy_check = st.form_submit_button("Check")
            if submit_json_strategy_check:
                strategy = check_strategy(json_strategy_text, False)
                if strategy is not None and not isinstance(strategy, bool):
                    _success(f"{strategy.name} is valid.")

                    strat_check_col1, strat_check_col2, strat_check_col3, strat_check_col4 = st.columns(4)
                    strat_check_col1.markdown("**Name**")
                    strat_check_col2.write(strategy.name)
                    if hasattr(strategy, "description") and len(strategy.description):
                        strat_check_col3.markdown("**Description**")
                        strat_check_col4.write(strategy.description)
                    st.markdown(f"**TA[{len(strategy.ta)}]**")
                    st.json(strategy.ta)

                    # if "strategy_txt" not in st.session_state["pta"]:
                    st.session_state["pta"]["strategy_txt"] = json_strategy_text


                else:
                    st.warning("Not a valid Pandas TA JSON Strategy")


def chart(title="Charting"):
    st.markdown(f"""
    ## {title}
    """)


def disclaimer(title="## Disclaimer"):
    st.markdown(f"""
    {title}

    ###### All investments involve risk, and the past performance of a security, industry, sector, market, financial product, trading strategy, or individual’s trading does not guarantee future results or returns. Investors are fully responsible for any investment decisions they make. Such decisions should be based solely on an evaluation of their financial circumstances, investment objectives, risk tolerance, and liquidity needs.

    ###### Any opinions, news, research, analyses, prices, or other information offered is provided as general market commentary, and does not constitute investment advice. I will not accept liability for any loss or damage, including without limitation any loss of profit, which may arise directly or indirectly from use of or reliance on such information.
    """)


def sidebar(title="Site Options"):
    st.sidebar.markdown(f"# {title}")

    st.sidebar.container()
    container = st.sidebar.container()
    # with container:

        # st.sidebar.checkbox("Show Installation", True)
        # st.sidebar.checkbox("Show Disclaimer", True)
        # show_installation = st.sidebar.checkbox("Show Installation", True)
        # show_disclaimer = st.sidebar.checkbox("Show Disclaimer", True)
    return st

def sidebar_data_options(title="## Data"):
    with st.sidebar.expander("Options", True):
        sources = ["Local"]
        if ta.Imports["stochastic"]: sources.append("Stochastic")
        if ta.Imports["yfinance"]: sources.append("Yahoo Finance")

        data_choice = st.radio("Select", sources, key="sb_data_choice")

        if data_choice == "Stochastic":
            st.checkbox("Options", False, key="sb_stochastic_options")
            st.checkbox("Help", False, key="sb_stochastic_help")

        if data_choice == "Yahoo Finance":
            st.checkbox("Options", False, key="sb_yfinance_options")
            st.checkbox("Help", False, key="sb_yfinance_help")

        if data_choice == "Local":
            file = st.file_uploader("Choose a file", type=["csv", "json"], key="sb_uploaded_file")
            if file is not None:
                # file_suffix = file.name.split(".")[1]
                _success(f"{file.name} Ready")

                # if "local_file_name" not in st.session_state["pta"]:
                #     st.session_state["pta"]["local_file_name"] = file.name

                if st.session_state["sb_uploaded_file"] is not None:
                    df = _load_file(st.session_state["sb_uploaded_file"])
                    df.name = file.name.split(".")[0]

                # if "localdf" not in st.session_state["pta"]:
                #     st.session_state["pta"]["localdf"] = localdf

                # if st.session_state["sb_uploaded_file"] is None:
                #     if "data_local_filename" not in st.session_state:
                #         st.session_state["data_local_filename"] = file.name

                # st.write(st.session_state.get("data_local_filename"))
                # st.write(st.session_state.get("sb_uploaded_file"))
                # if st.checkbox(f"Loaded {file.name} | {localdf.shape}", False, key="show_localdf"):
                #     st.write("1, 2, 3, ...")
                return df

            # if file_ is not None:
            #     file_suffix = file_.name.split(".")[1]
            #     # fd = file_.read()
            #     # st.write([x for x in dir(file_) if not x.startswith('_')])
            #     _success(f"{file_.name} Ready")

            #     if "local_file_name" not in st.session_state["pta"]:
            #         st.session_state["pta"]["local_file_name"] = file_.name

            #     # st.write(st.session_state)

            #     if file_suffix == "csv":
            #         localdf = pd.read_csv(file_)
            #     elif file_suffix == "json":
            #         localdf = pd.read_json(file_)
            #     else: pass

            #     if "localdf" not in st.session_state["pta"]:
            #         st.session_state["pta"]["localdf"] = localdf

            # if not localdf.empty and file is not None:
            #     st.markdown("### Chart")
            #     localdf.name = file.name
            #     # localdf.name = Path(file).name.split(".")[0]
            #     localdf_full = localdf.copy()
            #     # pdf, vdf = yf_chart(localdf, fig_size=(16, 8), stats=False, linreg=False)
            #     # st.pyplot(pdf.figure)
            #     # if vdf is not None: st.pyplot(vdf.figure)
            #     _success(f"{localdf.name} Ready")


if __name__ == "__main__":
    st.set_page_config(
        "Pandas TA Help and Examples",
        page_icon=":bar-chart:",
        initial_sidebar_state="expanded",
        layout="wide"
    )
    # st.sidebar.markdown(f"**Date**: {dt_today.strftime('%Y-%m-%d')}")
    show = {}

    # Sidebar
    page_options = st.sidebar.container()
    with page_options:
        st.sidebar.markdown("# Sections")
        show["description"] = st.sidebar.checkbox("Description", False, key="sb_description_check")
        show["installation"] = st.sidebar.checkbox("Installation", False, key="sb_installation_check")
        show["help"] = st.sidebar.checkbox("Help", False, key="sb_help_check")

        show["data"] = st.sidebar.checkbox("Data", True, key="sb_data_check")
        df = sidebar_data_options() if show["data"] else None

        show["analysis"] = st.sidebar.checkbox("Analysis", False, key="sb_analysis_check")
        show["strategy_checker"] = st.sidebar.checkbox("Strategy Checker", False, key="sb_strategy_check")
        show["chart"] = st.sidebar.checkbox("Charting", False, key="sb_chart_check")
        show["disclaimer"] = st.sidebar.checkbox("Disclaimer", False, key="sb_disclaimer_check")

    st.sidebar.markdown("---")
    st.sidebar.markdown("# Settings")
    show["display"] = st.sidebar.checkbox("Display", True, key="sb_display_check")
    # width_slider = st.sidebar.slider("Width Percent", value=95, min_value=85, max_value=100)
    # _max_width_(pct_width=width_slider)
    if show["display"]:
        sb_plot_expander = st.sidebar.expander("Stochastic Plot Size", False)
        with sb_plot_expander:
            stoch_plot_width = st.number_input("Width", value=float(16), min_value=float(1), key="sb_stoch_plot_width")
            stoch_plot_height = st.number_input("Height", value=float(8), min_value=float(1), key="sb_stoch_plot_height")

    # Main Page
    if show["description"]: description()
    if show["installation"]: installation()
    if show["help"]: tahelp()
    if show["data"]:
        data()
        # Options for Stoch and YF here
        def _sb_stochastic_options():
            if "sb_stochastic_options" in st.session_state and st.session_state["sb_stochastic_options"]:
                stochastic_data()
        def _sb_stochastic_help():
            if "sb_stochastic_help" in st.session_state and st.session_state["sb_stochastic_help"]:
                st.markdown("---")
                st.markdown("#### Stochastic Help")
                st.help(ta.sample)

        def _sb_yfinance_options():
            if "sb_yfinance_options" in st.session_state and st.session_state["sb_yfinance_options"]:
                st.markdown("---")
                st.markdown("### Yahoo Finance Options")
                yfinance_data()

                if not st.session_state["yfdf"].empty:
                    st.dataframe(st.session_state["yfdf"])
                    # st.dataframe(yfdf_full)
                    # if st.checkbox(f"Show DataFrame: {yf_ticker.upper()} | {yfdf.shape}", False, key="show_yfdf"):
                        # st.dataframe(yfdf_full)

        def _sb_yfinance_help():
            if "sb_yfinance_help" in st.session_state and st.session_state["sb_yfinance_help"]:
                st.markdown("---")
                st.markdown("#### Yahoo Finance Help")
                st.help(ta.yf)

        _sb_stochastic_options()
        _sb_stochastic_help()

        _sb_yfinance_options()
        _sb_yfinance_help()
    if show["analysis"]: analysis()
    if show["strategy_checker"]: strategy_checker()
    if show["chart"]: chart()
    if show["disclaimer"]: disclaimer()
    # imports()

st.markdown("###")
st.markdown("---")
st.write("st.session_state")
st.write(st.session_state)
