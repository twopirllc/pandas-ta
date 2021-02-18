# -*- coding: utf-8 -*-
import datetime as dt

from pathlib import Path
from random import random
from typing import Tuple

import pandas as pd  # pip install pandas
from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override() # <== that's all it takes :-)

from numpy import arange as npArange
from numpy import append as npAppend
from numpy import array as npArray

import alphaVantageAPI as AV # pip install alphaVantage-api
import pandas_ta as ta # pip install pandas_ta


def colors(colors: str = None, default: str = "GrRd"):
    aliases = {
        # Pairs
        "GrRd": ["green", "red"],
        "RdGr": ["red", "green"],
        "BkGy": ["black", "gray"],
        "BkSv": ["black", "silver"],
        "BkPr": ["black", "purple"],
        "BkBl": ["black", "blue"],
        "GyBk": ["gray", "black"],
        "GySv": ["gray", "silver"],
        "GyPr": ["gray", "purple"],
        "GyBl": ["gray", "blue"],
        "SvGy": ["silver", "gray"],
        "FcLi": ["fuchsia", "lime"],
        # Triples
        "BkGrRd": ["black", "green", "red"],
        "BkBlPr": ["black", "blue", "purple"],
        "GrOrRd": ["green", "orange", "red"],
        "RdOrGr": ["red", "orange", "green"],
        # Quads
        "BkGrOrRd": ["black", "green", "orange", "red"],
        # Quints
        "BkGrOrRdMr": ["black", "green", "orange", "red", "maroon"],
        # Indicators
        "bbands": ["blue", "navy", "blue"],
        "kc": ["purple", "fuchsia", "purple"],
    }
    aliases["default"] = aliases[default]
    if colors in aliases.keys():
        return aliases[colors]
    return aliases["default"]


class Watchlist(object):
    """
    # Watchlist Class (** This is subject to change! **)
    A simple Class to load/download financial market data and automatically
    apply Technical Analysis indicators with a Pandas TA Strategy.

    Default Strategy: pandas_ta.CommonStrategy

    ## Package Support:
    ### Data Source (Default: AlphaVantage)
    - AlphaVantage (pip install alphaVantage-api).
    - Python Binance (pip install python-binance). # Future Support
    - Yahoo Finance (pip install yfinance). # Almost Supported

    # Technical Analysis:
    - Pandas TA (pip install pandas_ta)

    ## Required Arguments:
    - tickers: A list of strings containing tickers. Example: ["SPY", "AAPL"]
    """

    def __init__(self,
        tickers: list, tf: str = None, name: str = None,
        strategy: ta.Strategy = None, ds_name: str = "av", **kwargs,
    ):
        self.verbose = kwargs.pop("verbose", False)
        self.debug = kwargs.pop("debug", False)
        self.timed = kwargs.pop("timed", False)

        self.tickers = tickers
        self.tf = tf
        self.name = name if isinstance(name, str) else f"Watch: {', '.join(tickers)}"
        self.data = None
        self.kwargs = kwargs
        self.strategy = strategy

        self._init_data_source(ds_name)


    def _init_data_source(self, ds: str) -> None:
        self.ds_name = ds.lower() if isinstance(ds, str) else "av"

        # Default: AlphaVantage
        AVkwargs = {"api_key": "YOUR API KEY", "clean": True, "export": True, "output_size": "full", "premium": False}
        self.av_kwargs = self.kwargs.pop("av_kwargs", AVkwargs)
        self.ds = AV.AlphaVantage(**self.av_kwargs)
        self.file_path = self.ds.export_path

        if self.ds_name == "yahoo":
            self.ds = yf

    def _drop_columns(self, df: pd.DataFrame, cols: list = None) -> pd.DataFrame:
        if cols is None or not isinstance(cols, list):
            cols = ["Unnamed: 0", "date", "split_coefficient", "dividend"]
        else: cols
        """Helper methods to drop columns silently."""
        df_columns = list(df.columns)
        if any(_ in df_columns for _ in cols):
            if self.debug:
                print(f"[i] Possible columns dropped: {', '.join(cols)}")
            df = df.drop(cols, axis=1, errors="ignore")
        return df

    def _load_all(self, **kwargs) -> dict:
        """Updates the Watchlist's data property with a dictionary of DataFrames
        keyed by ticker."""
        if (self.tickers is not None and isinstance(self.tickers, list) and
                len(self.tickers)):
            self.data = {ticker: self.load(ticker, **kwargs) for ticker in self.tickers}
            return self.data

    def _plot(self, df, mas:bool = True, constants:bool = False, **kwargs) -> None:

        if constants:
            chart_lines = npAppend(npArange(-5, 6, 1), npArange(-100, 110, 10))
            df.ta.constants(True, chart_lines) # Adding the constants for the charts
            df.ta.constants(False, npArray([-60, -40, 40, 60])) # Removing some constants from the DataFrame
            if self.verbose: print(f"[i] {df.ticker} constants added.")

        if ta.Imports["matplotlib"]:
            _exchange = kwargs.pop("exchange", "NYSE")
            _time = ta.get_time(_exchange, to_string=True)
            _kind = kwargs.pop("plot_kind", None)
            _figsize = kwargs.pop("figsize", (16, 10))
            _colors = kwargs.pop("figsize", ["black", "green", "orange", "red", "maroon"])
            _grid = kwargs.pop("grid", True)
            _alpha = kwargs.pop("alpha", 1)
            _last = kwargs.pop("last", 252)
            _title = kwargs.pop("title", f"{df.ticker}   {_time}   [{self.ds_name}]")

            col = kwargs.pop("close", "close")
            if mas:
                # df.ta.strategy(self.strategy, append=True)
                price = df[[col, "SMA_10", "SMA_20", "SMA_50", "SMA_200"]]
            else:
                price = df[col]

            if _kind is None:
                price.tail(_last).plot(figsize=_figsize, color=_colors, linewidth=2, title=_title, grid=_grid, alpha=_alpha)
            else:
                print(f"[X] Plot kind not implemented")
                return


    def load(self,
        ticker: str = None, tf: str = None, index: str = "date",
        drop: list = [], plot: bool = False, **kwargs
    ) -> pd.DataFrame:
        """Loads or Downloads (if a local csv does not exist) the data from the
        Data Source. When successful, it returns a Data Frame for the requested
        ticker. If no tickers are given, it loads all the tickers."""

        tf = self.tf if tf is None else tf.upper()
        if ticker is not None and isinstance(ticker, str):
            ticker = str(ticker).upper()
        else:
            print(f"[!] Loading All: {', '.join(self.tickers)}")
            self._load_all(**kwargs)
            return

        filename_ = f"{ticker}_{tf}.csv"
        current_file = Path(self.file_path) / filename_

        # Load local or from Data Source
        if current_file.exists():
            file_loaded = f"[i] Loaded {ticker}[{tf}]: {filename_}"
            # if self.ds_name == "av":
            if self.ds_name in ["av", "yahoo"]:
                df = pd.read_csv(current_file, index_col=0)
                if not df.ta.datetime_ordered:
                    df = df.set_index(pd.DatetimeIndex(df.index))
                print(file_loaded)
            else:
                print(f"[X] {filename_} not found in {Path(self.file_path)}")
                return
        else:
            print(f"[+] Downloading[{self.ds_name}]: {ticker}[{tf}]")
            if self.ds_name == "av":
                df = self.ds.data(ticker, tf)
                if not df.ta.datetime_ordered:
                    df = df.set_index(pd.DatetimeIndex(df[index]))
            if self.ds_name == "yahoo":
                yf_data = self.ds.Ticker(ticker)
                df = yf_data.history(period="max")
                to_save = f"{self.file_path}/{ticker}_{tf}.csv"
                print(f"[+] Saving: {to_save}")
                df.to_csv(to_save)

        # Remove select columns
        df = self._drop_columns(df, drop)

        if kwargs.pop("analyze", True):
            if self.debug: print(f"[+] TA[{len(self.strategy.ta)}]: {self.strategy.name}")
            df.ta.strategy(self.strategy, timed=self.timed, **kwargs)

        df.ticker = ticker # Attach ticker to the DataFrame
        df.tf = tf

        if plot: self._plot(df, **kwargs)
        return df

    @property
    def data(self) -> dict:
        """When not None, it contains a dictionary of DataFrames keyed by ticker. data = {"SPY": pd.DataFrame, ...}"""
        return self._data

    @data.setter
    def data(self, value: dict) -> None:
        # Later check dict has string keys and DataFrame values
        if value is not None and isinstance(value, dict):
            if self.verbose:
                print(f"[+] New data")
            self._data = value
        else:
            self._data = None

    @property
    def name(self) -> str:
        """The name of the Watchlist. Default: "Watchlist: {Watchlist.tickers}"."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if isinstance(value, str):
            self._name = str(value)
        else:
            self._name = f"Watchlist: {', '.join(self.tickers)}"

    @property
    def strategy(self) -> ta.Strategy:
        """Sets a valid Strategy. Default: pandas_ta.CommonStrategy"""
        return self._strategy

    @strategy.setter
    def strategy(self, value: ta.Strategy) -> None:
        if value is not None and isinstance(value, ta.Strategy):
            self._strategy = value
        else:
            self._strategy = ta.CommonStrategy

    @property
    def tf(self) -> str:
        """Alias for timeframe. Default: 'D'"""
        return self._tf

    @tf.setter
    def tf(self, value: str) -> None:
        if isinstance(value, str):
            value = str(value)
            self._tf = value
        else:
            self._tf = "D"

    @property
    def tickers(self) -> list:
        """tickers

        If a string, it it converted to a list. Example: "AAPL" -> ["AAPL"]
            * Does not accept, comma seperated strings.
        If a list, checks if it is a list of strings.
        """
        return self._tickers

    @tickers.setter
    def tickers(self, value: Tuple[list, str]) -> None:
        if value is None:
            print(f"[X] {value} is not a value in Watchlist ticker.")
            return
        elif isinstance(value, list) and [isinstance(_, str) for _ in value]:
            self._tickers = list(map(str.upper, value))
        elif isinstance(value, str):
            self._tickers = [value.upper()]
        self.name = self._tickers

    @property
    def verbose(self) -> bool:
        """Toggle the verbose property. Default: False"""
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        if isinstance(value, bool):
            self._verbose = bool(value)
        else:
            self._verbose = False

    def indicators(self, *args, **kwargs) -> any:
        """Returns the list of indicators that are available with Pandas Ta."""
        pd.DataFrame().ta.indicators(*args, **kwargs)

    def __repr__(self) -> str:
        s = f"Watch(name='{self.name}', ds_name='{self.ds_name}', tickers[{len(self.tickers)}]='{', '.join(self.tickers)}', tf='{self.tf}', strategy[{self.strategy.total_ta()}]='{self.strategy.name}'"
        if self.data is not None:
            s += f", data[{len(self.data.keys())}])"
            return s
        return s + ")"
