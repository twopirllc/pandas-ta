# -*- coding: utf-8 -*-
import datetime
from pathlib import Path

from numpy import array
from pandas import DataFrame, DatetimeIndex, read_csv
import pandas_datareader as pdr

import pandas_ta
from pandas_ta._typing import DictLike, IntFloat

sample_adx_data = read_csv(
    f"data/ADX_D.csv", index_col=0,
    parse_dates=True, date_format="%f"
)

ALERT: str = f"[!]"
INFO: str = f"[i]"
TEST: str = f"[T]"

CORRELATION: str = "corr"  # "sem"
CORRELATION_THRESHOLD: IntFloat = 0.99  # Less than 0.99 is undesirable
VERBOSE: bool = False

welles_wilder_df = DataFrame({
    "open": array([50, 50.7, 51.7, 52.5, 53.6, 54.4, 52.9, 52]),
    "high": array([51.2, 51.8, 52.9, 53.7, 54.8, 54.4, 53.2, 52.7]),
    "low": array([49.8, 50.3, 51.7, 52.3, 53.5, 52.9, 52, 52]),
    "close": array([50.9, 51.5, 52.8, 53.5, 54.7, 53, 52, 52.2])
})


def error_analysis(
    df: DataFrame, kind: str, msg: str,
    icon: str = INFO, newline: bool = True
):
    if VERBOSE:
        s = f"{icon} {df.name}['{kind}']: {msg}"
        if newline:
            s = f"\n{s}"
        print(s)


def load(**kwargs: DictLike):
    kwargs.setdefault("ticker", "SPY")
    kwargs.setdefault("fpath", "data/SPY_D.csv")
    kwargs.setdefault("prefix", "PDR_")
    kwargs.setdefault("interval", "d")

    kwargs.setdefault("index_col", 0)
    kwargs.setdefault("parse_dates", True)

    kwargs.setdefault("verbose", False)

    print(f"\n{TEST} Pandas TA on {datetime.datetime.now()}")
    fpath = Path(kwargs["fpath"])
    try:
        df = read_csv(
            fpath,
            index_col=kwargs["index_col"],
            parse_dates=kwargs["parse_dates"],
        )
        _mode = "Loading"
    except BaseException as err:
        print(f"{ALERT} {err}")
        if kwargs["verbose"]: print(f"{INFO} Downloading: {kwargs['ticker']} from YF")
        df = pdr.get_data_yahoo(kwargs['ticker'], interval=kwargs['interval'])
        df.to_csv(Path(fpath), mode="a")
        _mode = "Downloading"

    kwargs.setdefault("n", None)
    if isinstance(kwargs["n"], int):
        if kwargs["n"] > 0:
            df = df[:kwargs["n"]]
        elif kwargs['n'] < 0:
            df = df[kwargs["n"]:]

    df.columns = df.columns.str.lower()
    if kwargs["verbose"]:
        print(f"{INFO} {_mode} {kwargs['ticker']}{df.shape} from {fpath}")
        print(f"{INFO} From {df.index[0]} to {df.index[-1]}\n{df}\n")
    return df

_tdpy = pandas_ta.RATE["TRADING_DAYS_PER_YEAR"]
# At least 90 (88 with trix with default values) bars/rows/observations are
# needed to test All indicators individually and within the DataFrame
# extension. A larger sample may be required because of the Unstable Period
sample_data = load(
        fpath="data/SPY_D.csv",
        n = [
            -2 * _tdpy, -_tdpy,
            -200, -89, 0, 89, 200,
            _tdpy, 2 * _tdpy
        ][4],
        verbose=VERBOSE
    )


# Example multiindex download code
# _df = DataFrame()
# tickers =["SQ", "PLTR"]
# data = {t:_df.ta.ticker(t, period="1y", timed=True) for t in tickers if len(t) > 1}
# assets = concat(data, names=["ticker", "datetime"], verify_integrity=True)
