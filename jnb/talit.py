# -*- coding: utf-8 -*-
import datetime
# import os
from json import load as json_load
from pandas_ta.candles.ha import ha
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import rc
import mplfinance as mpf
from tqdm.notebook import trange, tqdm
import streamlit as st

import pandas_ta as ta


dt_today = datetime.datetime.now()
e = pd.DataFrame()


def _max_width_(st, pct_width:int = None):
    """"https://discuss.streamlit.io/t/custom-render-widths/81/8"""
    if pct_width is None:
        max_width_str = f"max-width: 2000px;"
    else:
        max_width_str = f"max-width: {pct_width};"

    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </
    """, unsafe_allow_html=True)


@st.cache
def app_source():
    result = ["stochastic"]
    if ta.Imports["yfinance"]: result.append("yfinance")
    if ta.Imports["alphaVantage-api"]: result.append("AlphaVantage")
    return result


def asset_class():
    return ["DEMO", "Equity", "Crypto", "FX"]


def imports(title="Available Functionality", columns:int = 4):
    st.sidebar.markdown(f"""## {title}""")
    total_items = len(ta.Imports.keys())
    for i in range(0, len(ta.Imports.keys()) - 1):
        j = 0
        for k,v in ta.Imports.items():
            col = st.columns(total_items // columns)
            # col[].write(k, v)
            # col[j].checkbox(k, v)
            print(i, j, (i + j) % columns, (i + j) % columns < columns, k, v)
            if (i + j) % columns == columns: break
            j += 1
            # st.write((i + j) % columns, k, v)
            # col.write(k)
            # j += 1
            # if j + 1 == total_items: break
            # col[i % cols].write(k)
            # st.write(k, v)
            # st.write(k, v)
            # col[(i + j) % cols].checkbox(k, v, f"i{i}{j}{cols}")
            # col[1].checkbox(obj[0], obj[1], f"ic1_{i}")
            # col[2].checkbox(obj[0], obj[1], f"ic2_{i}")
            # st.write(i, type(obj))
            # st.write(i % cols, obj[0], obj[1])
    print("\n\n")


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


def return_file(path, ftype:str="json"):
    result, p = [], Path(path)
    for item in p.iterdir():
        if item.is_file() and item.suffix == f".{ftype}":
            result.append(item)
    if len(result) == 0: result.append("")
    return result


def ta_sample_noises():
    return ta.sample().noises

def ta_sample_processes():
    return ta.sample().processes


def ticker_df(data_source:list, ticker:str):
    df = None
    print(f"[!] source: {data_source}")
    if isinstance(data_source, str) and len(data_source) > 0:
        _dsl = data_source.lower()
        if _dsl == "yfinance":
            # print(f"[!] source: yf")
            df = ta.df.ta.ticker(ticker, period="max", interval="1d", lc_cols=True)
            df.drop(columns=["dividends", "stock splits"], inplace=True)
        else: #"stochastic"
            print(f"[!] stochastic")
            # st.sidebar.selectbox("Source", ["stochastic"])
            # df = ta.sample(s0=np.sample(np.array([1, 2, 5, 10, 13, 25, 42, 50, 68])), process="gbm", length=2 * ta.RATE["TRADING_DAYS_YEAR"], verbose=True).df
            # print(np.sample(np.array([1, 2, 5, 10, 13, 25, 42, 50, 68])))
            df = ta.sample(s0=13, process="gbm", noise=None, length=ta.RATE["TRADING_DAYS_PER_YEAR"]).df
    return df


def ticker_list():
    return ["SPY", "BTC-USD", "ETH-USD", "SPY", "AA", "AAPL", "BAC", "PLTR", "SQ", "TLT", "TWTR", "XLF", "XLK", "OCUL"]


def main(*args, **kwargs):
    # study_path = kwargs.pop("study_path", "sample.json")

    st.markdown("# Pandas TAlit")
    st.markdown("---")

    # Sidebar
    st.sidebar.markdown("# OPTIONS")
    st.sidebar.markdown(f"**Date**: {dt_today.strftime('%Y-%m-%d')}")

    # # selection_col1.markdown("### Selection")
    # options_expander = st.expander("Options")
    # oe_col1, oe_col2, oe_col3, oe_col4 = options_expander.columns(4)
    # # my_expander.write('Hello there!')
    # # clicked = my_expander.button('Click me!')
    # # assets_ = my_expander.selectbox("Asset", asset_class())

    # assets_ = oe_col1.selectbox("Asset", asset_class())
    # source_ = oe_col2.selectbox("Source", app_source())
    # ticker_ = oe_col3.selectbox("Ticker", ticker_list())
    # bars_ = oe_col4.selectbox("Last", ["30", "60", "90", "180"])

    # study_expander = st.expander("Studies")
    # study_col1, study_col2, study_col3 = study_expander.columns(3)
    # study_path = study_col1.text_input("Directory", ".")
    # study_submit = study_col3.button("Submit")

    # # 
    # study_path = return_file(study_path)

    # # study_path = study_col2.selectbox("Study Path", "")
    # study_ = study_col2.selectbox("File", study_path)
    # # study = load_strategy(study_path)
    # print(dir(study_))
    # print(type(study_))
    # study = None
    # if isinstance(study_, Path) and study_.is_file():
    #     study = load_strategy(study_)
    #     print(study)
    # # with selection_col1:
    #     # assets_ = st.selectbox("Asset", asset_class())
    #     # source_ = st.selectbox("Source", ["stochastic", "yfinance", "AlphaVantage"])
    #     # ticker_ = st.selectbox("Ticker", ticker_list())
    #     # bars_ = st.selectbox("Last", ["30", "60", "90", "180"])

    # # srctkr_options_container = st.container()
    # # with srctkr_options_container:
    #     # st.markdown("# DATA")
    #     # assets_ = st.selectbox("Asset", asset_class())
    #     # source_ = st.selectbox("Source", ["stochastic", "yfinance", "AlphaVantage"])
    #     # ticker_ = st.selectbox("Ticker", ticker_list())
    #     # bars_ = st.selectbox("Last", ["30", "60", "90", "180"])


    sb_container = st.sidebar.container()
    with sb_container:
        sb_expander = st.expander("Mode")
        with sb_expander:
            mode_ = st.radio("Select", ["DEMO", "DATA", "LIVE"])

    with sb_container:
        sb_expander = st.expander("Studies")
        with sb_expander:
            json_path = st.text_input("Directory", ".", key="json_dir")
            json_path = return_file(json_path, "json")
            json_file = st.selectbox(f"Files", json_path)
            try:
                study_ = load_strategy(json_file)
                if len(study_.ta): st.text(f"Loaded: {study_.name}")
            except FileNotFoundError:
                st.text(f"[X] No JSON Strategy Found")

    sampledf = e.copy()
    with sb_container:
        sb_expander = st.expander("Source")
        with sb_expander:
            if mode_ == "DATA":
                source_ = st.radio("Select", [app_source()[0], "csv"])

                # sampledf = e.copy()
                if source_ == "stochastic":
                    st.header(source_.title())
                    source_container = st.container()
                    with source_container:
                        sp_name = st.text_input("Ticker")
                        sp_s0 = st.number_input("Initial", value=42.0, min_value=float(0.01), step=float(0.01))
                        sp_process = st.selectbox("Process", ta_sample_processes())
                        sp_noise = st.selectbox("Noise", ta_sample_noises())
                        sp_length = st.number_input("Length", value=1000, min_value=2, step=1)
                        sp_random_number = st.number_input("Random # (0 is random)", value=0, min_value=0, step=1)
                        sp_future = st.checkbox("Future", True)
                        sp_positive = st.checkbox("Positive", True)
                        sp_stats = st.checkbox("Stats", False)

                        sample_params = {
                            "name": None if len(sp_name) == 0 else sp_name,
                            "s0": sp_s0,
                            "process": sp_process,
                            "noise": sp_noise,
                            "length": sp_length,
                            "future": sp_future,
                            "positive": sp_positive,
                            "random_number": sp_random_number if sp_random_number > 0 else None
                        }
                        sampledf = ta.sample(**sample_params).df

            else:
                source_ = st.radio("Select", app_source()[1:])

    csvdf = e.copy()
    if source_ == "csv":
        with sb_container:
            sb_expander = st.expander("Local")
            with sb_expander:
                csv_path = st.text_input("Directory", ".", key="csv_dir")
                csv_path = return_file(csv_path, "csv")
                csv_ = st.selectbox("CSV File", csv_path)
                csvdf = pd.read_csv(csv_)
                # st.write(csv_path)
                # st.write(csv_)

    if not csvdf.empty:
        st.markdown("### Local Data")
        if st.checkbox("Show Chart", True):
            sample_colors = ["black", "blue"]
            if "date" in csvdf.columns: csvdf.set_index("date", inplace=True)
            if "datetime" in csvdf.columns: csvdf.set_index("datetime", inplace=True)
            # sample_fig = csvdf.plot(figsize=(16, 10), title=csv_, color=sample_colors, grid=True).figure
            sample_fig = csvdf["close"].plot(figsize=(16, 10), title=csv_, color=sample_colors, grid=True).figure
            st.pyplot(sample_fig)
        if st.checkbox("Show", False): st.dataframe(csvdf)

    # sampledf = e.copy()
    # if source_ == "stochastic":
    #     with sb_container:
    #         sb_expander = st.expander("Parameters")
    #         with sb_expander:
    #             sp_name = st.text_input("Ticker")
    #             sp_s0 = st.number_input("Initial", value=42.0, min_value=float(0.01), step=float(0.01))
    #             sp_process = st.selectbox("Process", ta_sample_processes())
    #             sp_noise = st.selectbox("Noise", ta_sample_noises())
    #             sp_length = st.number_input("Length", value=1000, min_value=2, step=1)
    #             sp_random_number = st.number_input("Random # (0 is random)", value=0, min_value=0, step=1)
    #             sp_future = st.checkbox("Future", True)
    #             sp_positive = st.checkbox("Positive", True)
    #             sp_stats = st.checkbox("Stats", False)

    #             sample_params = {
    #                 "name": None if len(sp_name) == 0 else sp_name,
    #                 "s0": sp_s0,
    #                 "process": sp_process,
    #                 "noise": sp_noise,
    #                 "length": sp_length,
    #                 "future": sp_future,
    #                 "positive": sp_positive,
    #                 "random_number": sp_random_number if sp_random_number > 0 else None
    #             }
    #             sampledf = ta.sample(**sample_params).df

    if not sampledf.empty:
        st.markdown("## Stochastic Sample")
        sample_colors = ["black", "blue"]
        sample_fig = sampledf.plot(figsize=(16, 10), title=sampledf.name, color=sample_colors, grid=True).figure
        st.pyplot(sample_fig)


    yfdf = e.copy()
    if source_ == "yfinance":
        with sb_container:
            sb_expander = st.expander("Parameters")
            with sb_expander:
                yf_ticker = st.text_input("Ticker", ticker_list()[0])
                # yf_s0 = st.number_input("Initial", value=42.0, min_value=float(0.01), step=float(0.01))
                # sp_process = st.selectbox("Process", ta_sample_processes())
                # sp_noise = st.selectbox("Noise", ta_sample_noises())
                # sp_length = st.number_input("Length", min_value=2, step=1)
                yf_period = st.selectbox("Period", "1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max".split(","))
                if yf_period in "1d,5d,1mo".split(","):
                    yf_interval = st.selectbox("Interval", "1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo".split(","))
                # sp_future = st.checkbox("Future", True)
                # sp_positive = st.checkbox("Positive", True)
                sp_stats = st.checkbox("Stats", False)

                yf_params = {
                    "ticker": None if len(yf_ticker) == 0 else yf_ticker,
                #     "s0": sp_s0,
                #     "process": sp_process,
                #     "noise": sp_noise,
                #     "length": sp_length,
                #     "future": sp_future,
                    "period": yf_period,
                    "interval": yf_interval,
                    "lc_cols": True
                }
                yfdf = ta.yf(**yf_params)

    if not yfdf.empty:
        st.markdown("## Yahoo Finance ")
        yf_colors = ["black", "blue"]
        yf_fig = yfdf.plot(figsize=(16, 10), title=yf_ticker, color=yf_colors, grid=True).figure
        st.pyplot(yf_fig)

    st.markdown("#")
    ind_help = None
    pta_help_expander = st.expander("Pandas TA Indicator Help")
    with pta_help_expander:
        all_tai = e.ta.indicators(as_list=True)
        ind_help = st.selectbox(f"Indicators [{len(all_tai)}]", all_tai)
        collapse_ta_help = st.checkbox("Collapse", False)
        if not collapse_ta_help and hasattr(ta, ind_help):
            st.help(getattr(ta, ind_help))


    # with st.sidebar.form(key="Form1"):
    #     st.header("Options")
    #     ticker_ = st.text_input("Ticker", "")
    #     _include_retweets = st.checkbox("Check")
    #     _num_of_tweets = st.number_input("number input", 100)
    #     form1_submitted = st.form_submit_button(label="Submit 🔎")

    # date_options_container = st.sidebar.container()
    # with date_options_container:
    #     st.markdown("# DATE\n\n")
        # start_date = st.sidebar.date_input("Start", datetime.date(2019, 1, 1))
        # end_date = st.sidebar.date_input("End", dt_today)

    # print(type())

    # # dl_state = st.text(f"Loading '{source_}' data...")
    # df = ticker_df(source_, ticker_)
    # print(f"df[{type(df)}:{df.shape}]:\n{df}\n")
    # # print(type(df))
    # # dl_state = st.text("")

    # if df is not None and study is not None and len(study.ta):
    #     # dl_state = st.text(f"Running Strategy: {study.name}...")
    #     df.ta.strategy(study, timed=True, verbose=True)
    #     # dl_state = st.text("")
    #     print(df)

    # print(df.shape)
    # print(ssdf.shape)

    # print(df.iloc[:,:-20])
    # print(df.tail(int(bars_)))
    # df = ta.df.ta.ticker(tickerSymbol, period="max")
    # tickerData = yf.Ticker(tickerSymbol) # Get ticker data
    # tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker
    # st.write(tickerSymbol)

    # if not df.empty and df.shape[0] > 0:
    #     st.write(_data_header + f" - Last {bars_}")
    #     st.dataframe(df[:-int(bars_)])
    # else:
        # st.write(_data_header)
        # st.dataframe(df)

    # if df is not None:# or not df.empty:
    #     _df = df.copy()
    #     _dre, _drs  = _df.index[-1].strftime('%Y-%m-%d'), _df.index[0].strftime('%Y-%m-%d')

    #     _data_header = f"{ticker_}[{source_}| {df.shape}] from {_drs} to {_dre}"
    #     if "volume" in _df.columns:
    #         colors = ["black", "blue"]
    #     else:
    #         colors = ["black", "green", "red", "violet", "purple", "violet"]

    #     if "volume" in df.columns:
    #         print(_df.columns)
    #         voldf = _df["volume"]
    #         del _df["volume"]
    #         if "OBV" in df.columns:
    #             obvdf = _df["volume"]
    #             del _df["volume"]

    #         _df = _df.iloc[:,3:]
    #         print(_df.columns)

    #         # fig = _df.plot(figsize=(16, 10), title=_data_header, color=colors, grid=True).figure
    #         # fig2 = voldf.plot(figsize=(16, 3), kind="bar", stacked=False, title=f"{_data_header} Volume", color=["silver"], grid=True).figure
    #         fig2 = voldf.plot(figsize=(16, 3), title=f"{_data_header} Volume", color=["gray"], grid=True).figure
    #         # st.pyplot(fig, clear_figure=False)
    #         st.pyplot(fig2)
    #     else:
    #         fig = _df.plot(figsize=(16, 10), title=_data_header, color=colors, grid=True).figure
    #         st.pyplot(fig)

    #     # bars_ = 20
    #     # if df.shape[0] > int(bars_):
    #     #     st.write(_data_header + f" {bars_} bars")
    #     #     st.dataframe(df[-int(bars_):], 1000)
    #     # else:
    #     #     st.write(_data_header)
    #     #     st.dataframe(df, 1000)

    # display_options_container = st.container()
    # with display_options_container:
    #     if st.checkbox(f"Maximize"):
    #         _max_width_(st)

    #     if st.checkbox(f"Last {bars_} bars"):
    #         if df.shape[0] > int(bars_):
    #             tmpdf = df.copy()
    #             st.write(_data_header + f" ({bars_} bars)")
    #             # tmpdf = tmpdf[-int(bars_):]
    #             # st.dataframe(df[-int(bars_):], 1000)
    #             st.dataframe(tmpdf, 1000)
    #         else:
    #             st.write(_data_header)
    #             st.dataframe(df, 1000)


    # def my_widget(key):
    #     st.subheader("Hello there!")
    #     return st.button(f"Click me {key}")

    # # This works in the main area
    # clicked = my_widget("first")

    # # And within an expander
    # my_expander = st.expander("Expand", expanded=True)
    # with my_expander:
    #     clicked = my_widget("second")

    # if not st.sidebar.checkbox(f"Last {ta.RATE['TRADING_DAYS_PER_YEAR']} bars"):
    #     st.table(df[:ta.RATE['TRADING_DAYS_PER_YEAR']])
    # elif st.sidebar.checkbox(f"Last {last_bars} bars"):
    #     st.table(df[:int(last_bars)])

    # Ticker information
    # string_logo = '<img src=%s>' % tickerData.info['logo_url']
    # st.markdown(string_logo, unsafe_allow_html=True)

    # string_name = tickerData.info['longName']
    # st.header('**%s**' % string_name)

    # string_summary = tickerData.info['longBusinessSummary']
    # st.info(string_summary)

    # Ticker data
    # st.header('**Ticker data**')
    # st.write(tickerDf)

    # Bollinger bands
    # st.header('**Bollinger Bands**')
    # qf = cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
    # qf.add_bollinger_bands()
    # fig = qf.iplot(asFigure=True)
    # st.plotly_chart(fig)

    ####
    #st.write('---')
    #st.write(tickerData.info)

    # show = {}
    # if show["data"]:
    #     sb_data_expander = st.sidebar.expander("Source", True)
    #     with sb_data_expander:
    #         # stoch_plot_width = st.number_input("Width", value=float(16), min_value=float(1), key="sb_stoch_plot_width")
    #         # stoch_plot_height = st.number_input("Height", value=float(8), min_value=float(1), key="sb_stoch_plot_height")
    #         data_source_ = st.radio("Select", ["local", "stochastic", "yfinance"], key="")


if __name__ == "__main__":
    main()