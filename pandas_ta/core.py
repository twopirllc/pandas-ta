# -*- coding: utf-8 -*-
import time
from functools import wraps

import pandas as pd
from pandas.core.base import PandasObject

from pandas_ta.candles import *
from pandas_ta.momentum import *
from pandas_ta.overlap import *
from pandas_ta.performance import *
from pandas_ta.statistics import *
from pandas_ta.trend import *
from pandas_ta.volatility import *
from pandas_ta.volume import *
from pandas_ta.utils import *

version = ".".join(("0", "1", "66b"))

def finalize(method):
    @wraps(method)
    def _wrapper(*class_methods, **method_kwargs):
        cm = class_methods[0]
        result = method(cm, **method_kwargs)

        cm._add_prefix_suffix(result, **method_kwargs)
        cm._append(result, **method_kwargs)
        return result
    return _wrapper


class BasePandasObject(PandasObject):
    """Simple PandasObject Extension

    Ensures the DataFrame is not empty and has columns. It would be a
    sad Panda otherwise.

    Args:
        df (pd.DataFrame): Extends Pandas DataFrame
    """
    def __init__(self, df, **kwargs):
        if df.empty: return

        if len(df.columns) > 0:
            self._df = df
        else:
            raise AttributeError(f" [X] No columns!")

    def __call__(self, kind, *args, **kwargs):
        raise NotImplementedError()


@pd.api.extensions.register_dataframe_accessor('ta')
class AnalysisIndicators(BasePandasObject):
    """AnalysisIndicators is a class that extends the Pandas DataFrame via
    Pandas @pd.api.extensions.register_dataframe_accessor('name') decorator.

    This Pandas Extension is named 'ta' for Technical Analysis that allows us
    to apply technical indicators by extension.  Even though 'ta' is a
    Pandas DataFrame Extension, you can still call the Indicators
    individually. Use help() if needed.

    By default the 'ta' extension uses lower case column names: open, high,
    low, close, and volume.  You can override the defaults by providing the
    it's replacement name when calling the indicator.  For example, to call the
    indicator hl2().

    With 'default' columns: open, high, low, close, and volume.
    >>> df.ta.hl2()
    >>> df.ta(kind='hl2')

    With DataFrame columns: Open, High, Low, Close, and Volume.
    >>> df.ta.hl2(high='High', low='Low')
    >>> df.ta(kind='hl2', high='High', low='Low')

    If you do not want to use a DataFrame Extension, just call it normally.
    >>> sma10 = ta.sma(df['Close']) # Default length=10
    >>> sma50 = ta.sma(df['Close'], length=50)
    >>> ichimoku, span = ta.ichimoku(df['High'], df['Low'], df['Close'])

    Args:
        kind (str, optional): Default: None.  Kind is the 'name' of the indicator.
            It converts kind to lowercase before calling.
        timed (bool, optional): Default: False.  Curious about the execution
            speed?
        kwargs: Extension specific modifiers.
            append (bool, optional):  Default: False.  When True, it appends the
            resultant column(s) to the DataFrame.

    Returns:
        Most Indicators will return a Pandas Series.  Others like MACD, BBANDS,
        KC, et al will return a Pandas DataFrame.  Ichimoku on the other hand
        will return two DataFrames, the Ichimoku DataFrame for the known period
        and a Span DataFrame for the future of the Span values.

    Let's get started!

    1. Loading the 'ta' module:
    >>> import pandas as pd
    >>> import ta as ta

    2. Load some data:
    >>> df = pd.read_csv('AAPL.csv', index_col='date', parse_dates=True)

    3. Help!
    3a. General Help:
    >>> help(df.ta)
    >>> df.ta()
    3b. Indicator Help:
    >>> help(ta.apo)
    3c. Indicator Extension Help:
    >>> help(df.ta.apo)

    4. Ways of calling an indicator.
    4a. Calling just the MACD indicator without 'ta' DataFrame extension.
    >>> ta.apo(df['close'])
    4b. Calling just the MACD indicator with 'ta' DataFrame extension.
    >>> df.ta.apo()
    4c. Calling using kind.
    >>> df.ta(kind='apo')

    5. Working with kwargs
    5a. Append the result to the working df.
    >>> df.ta.apo(append=True)
    5b. Timing an indicator.
    >>> apo = df.ta(kind='apo', timed=True)
    >>> print(apo.timed)
    """
    _adjusted = None

    def __call__(self, kind=None, alias=None, timed=False, **kwargs):
        try:
            if isinstance(kind, str):
                kind = kind.lower()
                fn = getattr(self, kind)

                if timed:
                    stime = time.time()

                # Run the indicator
                indicator = fn(**kwargs)

                if timed:
                    time_diff = time.time() - stime
                    ms = time_diff * 1000
                    indicator.timed = f"{ms:2.3f} ms ({time_diff:2.3f} s)"
                    # print(f"execution time: {indicator.timed}")
                    self._df.timed = indicator.timed

                # Add an alias if passed
                if alias:
                    indicator.alias = f"{alias}"

                return indicator
            else:
                self.help()

        except:
            self.help()


    @property
    def adjusted(self) -> str:
        """property: df.ta.adjusted"""
        return self._adjusted

    @adjusted.setter
    def adjusted(self, value:str) -> None:
        """property: df.ta.adjusted = 'adj_close'"""
        if value is not None and isinstance(value, str):
            self._adjusted = value
        else:
            self._adjusted = None

    @property
    def datetime_ordered(self) -> bool:
        """Returns True if the index is a datetime and ordered."""
        return is_datetime_ordered(self._df)

    @property
    def reverse(self) -> pd.DataFrame:
        """Reverses the DataFrame. Simply: df.iloc[::-1]"""
        return self._df.iloc[::-1]

    @property
    def version(self) -> str:
        """Returns the version."""
        return version

    def _append(self, result=None, **kwargs):
        """Appends a Pandas Series or DataFrame columns to self._df."""
        if 'append' in kwargs and kwargs['append']:
            df = self._df
            if df is None or result is None: return
            else:
                if isinstance(result, pd.DataFrame):
                    for i, column in enumerate(result.columns):
                        df[column] = result.iloc[:,i]
                else:
                    df[result.name] = result


    def _add_prefix_suffix(self, result=None, **kwargs):
        """Add prefix and/or suffix to the result columns"""
        if result is None: return
        else:
            prefix = suffix = ""
            # delimiter = kwargs.pop("delimiter", "_")

            if "prefix" in kwargs:
                prefix = f"{kwargs['prefix']}_"
            if "suffix" in kwargs:
                suffix = f"_{kwargs['suffix']}"

            if isinstance(result, pd.Series):
                result.name = prefix + result.name + suffix
            else:
                result.columns = [prefix + column + suffix for column in result.columns]


    def _get_column(self, series, default):
        """Attempts to get the correct series or 'column' and return it."""
        df = self._df
        if df is None: return

        # Explicitly passing a pd.Series to override default.
        if isinstance(series, pd.Series):
            return series
        # Apply default if no series nor a default.
        elif series is None or default is None:
            return df[self.adjusted] if self.adjusted is not None else df[default]
        # Ok.  So it's a str.
        elif isinstance(series, str):
            # Return the df column since it's in there.
            if series in df.columns:
                return df[series]
            else:
                # Attempt to match the 'series' because it was likely misspelled.
                matches = df.columns.str.match(series, case=False)
                match = [i for i, x in enumerate(matches) if x]
                # If found, awesome.  Return it or return the 'series'.
                cols = ', '.join(list(df.columns))
                NOT_FOUND = f" [X] Ooops!!!: It's {series not in df.columns}, the series '{series}' not in {cols}"
                return df.iloc[:,match[0]] if len(match) else print(NOT_FOUND)


    def constants(self, append, lower_bound=-100, upper_bound=100, every=1):
        """Constants

        Useful for creating indicator levels or if you need some constant value
        easily added to your DataFrame.

        Add constant '1' to the DataFrame
        >>> df.ta.constants(True, 1, 1, 1)
        Remove constant '1' to the DataFrame
        >>> df.ta.constants(False, 1, 1, 1)

        Adding constants that range of constants from -4 to 4 inclusive
        >>> df.ta.constants(True, -4, 4, 1)
        Removing constants that range of constants from -4 to 4 inclusive
        >>> df.ta.constants(False, -4, 4, 1)

        Args:
            append (bool): Default: None.  If True, appends the range of constants to the
                working DataFrame.  If False, it removes the constant range from the working
                DataFrame.
            lower_bound (int): Default: -100.  Lowest integer for the constant range.
            upper_bound (int): Default: 100.  Largest integer for the constant range.
            every (int): Default: 10.  How often to include a new constant.

        Returns:
            Returns nothing to the user.  Either adds or removes constant ranges from the
            working DataFrame.
        """
        levels = [x for x in range(lower_bound, upper_bound + 1) if x % every == 0]
        if append:
            for x in levels:
                self._df[f'{x}'] = x
        else:
            for x in levels:
                del self._df[f'{x}']


    def indicators(self, **kwargs):
        """List of Indicators
        
        Args:
            kwargs:
                as_list (bool, optional):  Default: False.  When True, it returns a list
                    of the indicators.  Helpful you want to filter out what you want to run.
                exclude (list, optional):  Default: None.  The passed in list will be
                    excluded from the indicators list.

        Returns:
            Prints the list of indicators. If as_list=True, then a list.
        """
        as_list = kwargs.pop("as_list", False)
        helper_methods = ["constants", "indicators", "strategy"]  # Public non-indicator methods
        ta_properties = ["adjusted", "datetime_ordered", "reverse", "version"]
        exclude_methods = kwargs.pop("exclude", None)
        ta_indicators = list((x for x in dir(pd.DataFrame().ta) if not x.startswith('_') and not x.endswith('_')))

        for x in helper_methods:
            ta_indicators.remove(x)

        for x in ta_properties:
            ta_indicators.remove(x)

        if isinstance(exclude_methods, list) and len(exclude_methods) > 0:
            for x in exclude_methods:
                ta_indicators.remove(x)

        if as_list:
            return ta_indicators

        header = f"pandas.ta - Technical Analysis Indicators - v{self.version}"
        total_indicators = len(ta_indicators)
        s = f"{header}\nTotal Indicators: {total_indicators}\n"
        if total_indicators > 0:            
            abbr_list = ", ".join(ta_indicators)
            print(f"{s}Abbreviations:\n    {abbr_list}")
        else:
            print(s)


    # ALL Features
    def _all(self, **kwargs):
        """Appends by default all non-excluded indicators to the DataFrame. Used by ta.strategy(**kwargs)"""
        append = kwargs.pop("append", True)
        verbose = kwargs.pop("verbose", False)
        user_excluded = kwargs.pop("exclude", [])

        excluded = ["above", "above_value", "below", "below_value",
        "cross", "cross_value", "long_run", "short_run", "trend_return", "vp"]
        excluded += user_excluded
        print(f"[i] excluded[{len(excluded)}]: {', '.join(excluded)}") if verbose else None

        indicators = self.indicators(as_list=True, exclude=excluded)

        if verbose and bool(kwargs):
            print(f"[i] All indicators with the following arguments: {kwargs}")

        for kind in indicators:
            fn = getattr(self, kind)
            fn(append=append, **kwargs)
            print(f"[+] {kind}") if verbose else None


    def strategy(self, **kwargs):
        """Strategy Method

        An experimental method that by default runs all applicable indicators.
        Future implementations will allow more specific indicator generation through
        a json config file.

        Args:
            name (str, optional): Default: 'all'
            exclude (list, optional): Default: []. List of indicator names to exclude.
            verbose (bool): Default: False

            kwargs:
                (optional) Default: {}. Any indicator argument you want to modify.
                    For example, length=20 or offset=-1 or high=df['High'] ...

        """
        name = kwargs.pop("name", "all")
        if name is None or name == "" or not isinstance(name, str): # Extra check
            name = "all"
        self._all(**kwargs) if name == "all" else None


    # Candles
    @finalize
    def ha(self, open_=None, high=None, low=None, close=None, offset=None, **kwargs):
        open_ = self._get_column(open_, 'open')
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = ha(open_=open_, high=high, low=low, close=close, offset=offset, **kwargs)
        return result

    # Momentum Indicators
    @finalize
    def ao(self, high=None, low=None, fast=None, slow=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        result = ao(high=high, low=low, fast=fast, slow=slow, offset=offset, **kwargs)
        return result

    @finalize
    def apo(self, close=None, fast=None, slow=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = apo(close=close, fast=fast, slow=slow, offset=offset, **kwargs)
        return result

    @finalize
    def bias(self, close=None, length=None, mamode=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = bias(close=close, length=length, mamode=mamode, offset=offset, **kwargs)
        return result

    @finalize
    def bop(self, open_=None, high=None, low=None, close=None, percentage=False, offset=None, **kwargs):
        open_ = self._get_column(open_, 'open')
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = bop(open_=open_, high=high, low=low, close=close, percentage=percentage, offset=offset, **kwargs)
        return result

    @finalize
    def brar(self, open_=None, high=None, low=None, close=None, length=None, scalar=None, drift=None, offset=None, **kwargs):
        open_ = self._get_column(open_, 'open')
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = brar(open_=open_, high=high, low=low, close=close, length=length, scalar=scalar, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def cci(self, high=None, low=None, close=None, length=None, c=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = cci(high=high, low=low, close=close, length=length, c=c, offset=offset, **kwargs)
        return result

    @finalize
    def cg(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = cg(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def cmo(self, close=None, length=None, scalar=None, drift=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = cmo(close=close, length=length, scalar=scalar, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def coppock(self, close=None, length=None, fast=None, slow=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = coppock(close=close, length=length, fast=fast, slow=slow, offset=offset, **kwargs)
        return result

    @finalize
    def fisher(self, high=None, low=None, length=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')

        result = fisher(high=high, low=low, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def kdj(self, high=None, low=None, close=None, length=None, signal=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = kdj(high=high, low=low, close=close, length=length, signal=signal, offset=offset, **kwargs)
        return result

    @finalize
    def kst(self, close=None, roc1=None, roc2=None, roc3=None, roc4=None, sma1=None, sma2=None, sma3=None, sma4=None, signal=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = kst(close=close, roc1=roc1, roc2=roc2, roc3=roc3, roc4=roc4, sma1=sma1, sma2=sma2, sma3=sma3, sma4=sma4, signal=signal, offset=offset, **kwargs)
        return result

    @finalize
    def macd(self, close=None, fast=None, slow=None, signal=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = macd(close=close, fast=fast, slow=slow, signal=signal, offset=offset, **kwargs)
        return result

    @finalize
    def mom(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = mom(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def ppo(self, close=None, fast=None, slow=None, percentage=True, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = ppo(close=close, fast=fast, slow=slow, percentage=percentage, offset=offset, **kwargs)
        return result

    @finalize
    def psl(self, close=None, open_=None, length=None, scalar=None, drift=None, offset=None, **kwargs):
        if open_ is not None:
            open_ = self._get_column(open_, 'open')
        close = self._get_column(close, 'close')

        result = psl(close=close, open_=open_, length=length, scalar=scalar, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def roc(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = roc(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def rsi(self, close=None, length=None, scalar=None, drift=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = rsi(close=close, length=length, scalar=scalar, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def rvi(self, open_=None, high=None, low=None, close=None, length=None, swma_length=None, offset=None, **kwargs):
        open_ = self._get_column(open_, 'open')
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = rvi(open_=open_, high=high, low=low, close=close, length=length, swma_length=swma_length, offset=offset, **kwargs)
        return result

    @finalize
    def slope(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = slope(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def stoch(self, high=None, low=None, close=None, fast_k=None, slow_k=None, slow_d=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = stoch(high=high, low=low, close=close, fast_k=fast_k, slow_k=slow_k, slow_d=slow_d, offset=offset, **kwargs)
        return result

    @finalize
    def trix(self, close=None, length=None, signal=None, scalar=None, drift=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = trix(close=close, length=length, signal=signal, scalar=scalar, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def tsi(self, close=None, fast=None, slow=None, drift=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = tsi(close=close, fast=fast, slow=slow, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def uo(self, high=None, low=None, close=None, fast=None, medium=None, slow=None, fast_w=None, medium_w=None, slow_w=None, drift=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = uo(high=high, low=low, close=close, fast=fast, medium=medium, slow=slow, fast_w=fast_w, medium_w=medium_w, slow_w=slow_w, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def willr(self, high=None, low=None, close=None, length=None, percentage=True, offset=None,**kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = willr(high=high, low=low, close=close, length=length, percentage=percentage, offset=offset, **kwargs)
        return result


    # Overlap Indicators
    @finalize
    def dema(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = dema(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def ema(self, close=None, length=None, offset=None, adjust=None, **kwargs):
        close = self._get_column(close, 'close')

        result = ema(close=close, length=length, offset=offset, adjust=adjust, **kwargs)
        return result

    @finalize
    def fwma(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = fwma(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def hl2(self, high=None, low=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')

        result = hl2(high=high, low=low, offset=offset, **kwargs)
        return result

    @finalize
    def hlc3(self, high=None, low=None, close=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = hlc3(high=high, low=low, close=close, offset=offset, **kwargs)
        return result

    @finalize
    def hma(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = hma(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def kama(self, close=None, length=None, fast=None, slow=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = kama(close=close, length=length, fast=fast, slow=slow, offset=offset, **kwargs)
        return result

    # @finalize
    def ichimoku(self, high=None, low=None, close=None, tenkan=None, kijun=None, senkou=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result, span = ichimoku(high=high, low=low, close=close, tenkan=tenkan, kijun=kijun, senkou=senkou, offset=offset, **kwargs)
        self._add_prefix_suffix(result, **kwargs)
        self._add_prefix_suffix(span, **kwargs)
        self._append(result, **kwargs)
        return result, span

    @finalize
    def linreg(self, close=None, length=None, offset=None, adjust=None, **kwargs):
        close = self._get_column(close, 'close')

        result = linreg(close=close, length=length, offset=offset, adjust=adjust, **kwargs)
        return result

    @finalize
    def midpoint(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = midpoint(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def midprice(self, high=None, low=None, length=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')

        result = midprice(high=high, low=low, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def ohlc4(self, open_=None, high=None, low=None, close=None, offset=None, **kwargs):
        open_ = self._get_column(open_, 'open')
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = ohlc4(open_=open_, high=high, low=low, close=close, offset=offset, **kwargs)
        return result

    @finalize
    def pwma(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = pwma(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def rma(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = rma(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def sinwma(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = sinwma(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def sma(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = sma(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def supertrend(self, high=None, low=None, close=None, length=None, multiplier=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = supertrend(high=high, low=low, close=close, length=length, multiplier=multiplier, offset=offset, **kwargs)
        return result

    @finalize
    def swma(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = swma(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def t3(self, close=None, length=None, a=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = t3(close=close, length=length, a=a, offset=offset, **kwargs)
        return result

    @finalize
    def tema(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = tema(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def trima(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = trima(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def vwap(self, high=None, low=None, close=None, volume=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        # Ensure volume has a datetime ordered index
        if not self.datetime_ordered:
            volume.index = self._df.index

        result = vwap(high=high, low=low, close=close, volume=volume, offset=offset, **kwargs)
        return result

    @finalize
    def vwma(self, close=None, volume=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = vwma(close=close, volume=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def wcp(self, high=None, low=None, close=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = wcp(high=high, low=low, close=close, offset=offset, **kwargs)
        return result

    @finalize
    def wma(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = wma(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def zlma(self, close=None, length=None, mamode=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = zlma(close=close, length=length, mamode=mamode, offset=offset, **kwargs)
        return result


    # Performance Indicators
    @finalize
    def log_return(self, close=None, length=None, cumulative=False, percent=False, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = log_return(close=close, length=length, cumulative=cumulative, percent=percent, offset=offset, **kwargs)
        return result

    @finalize
    def percent_return(self, close=None, length=None, cumulative=False, percent=False, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = percent_return(close=close, length=length, cumulative=cumulative, percent=percent, offset=offset, **kwargs)
        return result

    @finalize
    def trend_return(self, close=None, trend=None, log=True, cumulative=None, offset=None, trend_reset=None, **kwargs):
        close = self._get_column(close, 'close')
        trend = self._get_column(trend, f"{trend}")

        result = trend_return(close=close, trend=trend, log=log, cumulative=cumulative, offset=offset, trend_reset=trend_reset, **kwargs)
        return result


    # Statistics Indicators
    @finalize
    def entropy(self, close=None, length=None, base=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = entropy(close=close, length=length, base=base, offset=offset, **kwargs)
        return result

    @finalize
    def kurtosis(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = kurtosis(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def mad(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = mad(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def median(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = median(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def quantile(self, close=None, length=None, q=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = quantile(close=close, length=length, q=q, offset=offset, **kwargs)
        return result

    @finalize
    def skew(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = skew(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def stdev(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = stdev(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def variance(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = variance(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def zscore(self, close=None, length=None, std=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = zscore(close=close, length=length, std=std, offset=offset, **kwargs)
        return result



    # Trend Indicators
    @finalize
    def adx(self, high=None, low=None, close=None, drift=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = adx(high=high, low=low, close=close, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def amat(self, close=None, fast=None, slow=None, mamode=None, lookback=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = amat(close=close, fast=fast, slow=slow, mamode=mamode, lookback=lookback, offset=offset, **kwargs)
        return result

    @finalize
    def aroon(self, high=None, low=None, length=None, scalar=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')

        result = aroon(high=high, low=low, length=length, scalar=scalar, offset=offset, **kwargs)
        return result

    @finalize
    def chop(self, high=None, low=None, close=None, length=None, atr_length=None, scalar=None, drift=None, offset=None, **kwargs):
        high = self._get_column(close, 'high')
        low = self._get_column(close, 'low')
        close = self._get_column(close, 'close')

        result = chop(high=high, low=low, close=close, length=length, atr_length=atr_length, scalar=scalar, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def cksp(self, high=None, low=None, close=None, p=None, x=None, q=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = cksp(high=high, low=low, close=close, p=p, x=x, q=q, offset=offset, **kwargs)
        return result

    @finalize
    def decreasing(self, close=None, length=None, asint=True, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = decreasing(close=close, length=length, asint=asint, offset=offset, **kwargs)
        return result

    @finalize
    def dpo(self, close=None, length=None, centered=True, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = dpo(close=close, length=length, centered=centered, offset=offset, **kwargs)
        return result

    @finalize
    def increasing(self, close=None, length=None, asint=True, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = increasing(close=close, length=length, asint=asint, offset=offset, **kwargs)
        return result

    @finalize
    def linear_decay(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = linear_decay(close=close, length=length, offset=offset, **kwargs)
        return result

    # @finalize
    def long_run(self, fast=None, slow=None, length=None, offset=None, **kwargs):
        if fast is None and slow is None: return self._df
        else:
            fast = self._get_column(fast, f"{fast}")
            slow = self._get_column(slow, f"{slow}")

            result = long_run(fast=fast, slow=slow, length=length, offset=offset, **kwargs)
            self._add_prefix_suffix(result, **kwargs)
            self._append(result, **kwargs)
            return result

    @finalize
    def psar(self, high=None, low=None, close=None, af=None, max_af=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        if close is not None:
            close = self._get_column(close, 'close')

        result = psar(high=high, low=low, close=close, af=af, max_af=max_af, offset=offset, **kwargs)
        return result

    @finalize
    def qstick(self, open_=None, close=None, length=None, offset=None, **kwargs):
        open_ = self._get_column(open_, 'open')
        close = self._get_column(close, 'close')

        result = qstick(open_=open_, close=close, length=length, offset=offset, **kwargs)
        return result

    # @finalize
    def short_run(self, fast=None, slow=None, length=None, offset=None, **kwargs):
        if fast is None and slow is None: return self._df
        else:
            fast = self._get_column(fast, f"{fast}")
            slow = self._get_column(slow, f"{slow}")

            result = short_run(fast=fast, slow=slow, length=length, offset=offset, **kwargs)
            self._add_prefix_suffix(result, **kwargs)
            self._append(result, **kwargs)
            return result

    @finalize
    def supertrend(self, high=None, low=None, close=None, period=None, multiplier=None, mamode=None, drift=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = supertrend(high=high, low=low, close=close, period=period, multiplier=multiplier, mamode=mamode, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def vortex(self, high=None, low=None, close=None, drift=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = vortex(high=high, low=low, close=close, drift=drift, offset=offset, **kwargs)
        return result



    # Utility Indicators
    @finalize
    def above(self, a=None, b=None, asint=True, offset=None, **kwargs):
        if a is None and b is None: return self._df
        else:
            a = self._get_column(a, f"{a}")
            b = self._get_column(b, f"{b}")
            result = above(series_a=a, series_b=b, asint=asint, offset=offset, **kwargs)
            return result

    @finalize
    def above_value(self, a=None, value=None, asint=True, offset=None, **kwargs):
        if a is None and value is None: return self._df
        else:
            a = self._get_column(a, f"{a}")
            result = above_value(series_a=a, value=value, asint=asint, offset=offset, **kwargs)
            return result

    @finalize
    def below(self, a=None, b=None, asint=True, offset=None, **kwargs):
        if a is None and b is None: return self._df
        else:
            a = self._get_column(a, f"{a}")
            b = self._get_column(b, f"{b}")
            result = below(series_a=a, series_b=b, asint=asint, offset=offset, **kwargs)
            return result

    @finalize
    def below_value(self, a=None, value=None, asint=True, offset=None, **kwargs):
        if a is None and value is None: return self._df
        else:
            a = self._get_column(a, f"{a}")
            result = below_value(series_a=a, value=value, asint=asint, offset=offset, **kwargs)
            return result

    @finalize
    def cross(self, a=None, b=None, above=True, asint=True, offset=None, **kwargs):
        if a is None and b is None: return self._df
        else:
            a = self._get_column(a, f"{a}")
            b = self._get_column(b, f"{b}")
            result = cross(series_a=a, series_b=b, above=above, asint=asint, offset=offset, **kwargs)
            return result

    @finalize
    def cross_value(self, a=None, value=None, above=True, asint=True, offset=None, **kwargs):
        if a is None and value is None: return self._df
        else:
            a = self._get_column(a, f"{a}")
            result = cross_value(series_a=a, value=value, above=above, asint=asint, offset=offset, **kwargs)
            return result


    # Volatility Indicators
    @finalize
    def aberration(self, high=None, low=None, close=None, length=None, atr_length=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = aberration(high=high, low=low, close=close, length=length, atr_length=atr_length, offset=offset, **kwargs)
        return result

    @finalize
    def accbands(self, high=None, low=None, close=None, length=None, c=None, mamode=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = accbands(high=high, low=low, close=close, length=length, c=c, mamode=mamode, offset=offset, **kwargs)
        return result

    @finalize
    def atr(self, high=None, low=None, close=None, length=None, mamode=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = atr(high=high, low=low, close=close, length=length, mamode=mamode, offset=offset, **kwargs)
        return result

    @finalize
    def bbands(self, close=None, length=None, stdev=None, mamode=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = bbands(close=close, length=length, stdev=stdev, mamode=mamode, offset=offset, **kwargs)
        return result

    @finalize
    def donchian(self, close=None, length=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')

        result = donchian(close=close, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def kc(self, high=None, low=None, close=None, length=None, scalar=None, mamode=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = kc(high=high, low=low, close=close, length=length, scalar=scalar, mamode=mamode, offset=offset, **kwargs)
        return result

    @finalize
    def massi(self, high=None, low=None, fast=None, slow=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')

        result = massi(high=high, low=low, fast=fast, slow=slow, offset=offset, **kwargs)
        return result

    @finalize
    def natr(self, high=None, low=None, close=None, length=None, mamode=None, scalar=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = natr(high=high, low=low, close=close, length=length, mamode=mamode, scalar=scalar, offset=offset, **kwargs)
        return result

    @finalize
    def pdist(self, open_=None, high=None, low=None, close=None, drift=None, offset=None, **kwargs):
        open_ = self._get_column(open_, 'open')
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = pdist(open_=open_, high=high, low=low, close=close, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def true_range(self, high=None, low=None, close=None, drift=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')

        result = true_range(high=high, low=low, close=close, drift=drift, offset=offset, **kwargs)
        return result



    # Volume Indicators
    @finalize
    def ad(self, high=None, low=None, close=None, volume=None, open_=None, signed=True, offset=None, **kwargs):
        if open_ is not None:
            open_ = self._get_column(open_, 'open')
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = ad(high=high, low=low, close=close, volume=volume, open_=open_, signed=signed, offset=offset, **kwargs)
        return result

    @finalize
    def adosc(self, high=None, low=None, close=None, volume=None, open_=None, fast=None, slow=None, signed=True, offset=None, **kwargs):
        if open_ is not None:
            open_ = self._get_column(open_, 'open')
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = adosc(high=high, low=low, close=close, volume=volume, open_=open_, fast=fast, slow=slow, signed=signed, offset=offset, **kwargs)
        return result

    @finalize
    def aobv(self, close=None, volume=None, fast=None, slow=None, mamode=None, max_lookback=None, min_lookback=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = aobv(close=close, volume=volume, fast=fast, slow=slow, mamode=mamode, max_lookback=max_lookback, min_lookback=min_lookback, offset=offset, **kwargs)
        return result

    @finalize
    def cmf(self, high=None, low=None, close=None, volume=None, open_=None, length=None, offset=None, **kwargs):
        if open_ is not None:
            open_ = self._get_column(open_, 'open')
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = cmf(high=high, low=low, close=close, volume=volume, open_=open_, length=length, offset=offset, **kwargs)
        return result

    @finalize
    def efi(self, close=None, volume=None, length=None, mamode=None, offset=None, drift=None, **kwargs):
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = efi(close=close, volume=volume, length=length, offset=offset, mamode=mamode, drift=drift, **kwargs)
        return result

    @finalize
    def eom(self, high=None, low=None, close=None, volume=None, length=None, divisor=None, offset=None, drift=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = eom(high=high, low=low, close=close, volume=volume, length=length, divisor=divisor, offset=offset, drift=drift, **kwargs)
        return result

    @finalize
    def mfi(self, high=None, low=None, close=None, volume=None, length=None, drift=None, offset=None, **kwargs):
        high = self._get_column(high, 'high')
        low = self._get_column(low, 'low')
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = mfi(high=high, low=low, close=close, volume=volume, length=length, drift=drift, offset=offset, **kwargs)
        return result

    @finalize
    def nvi(self, close=None, volume=None, length=None, initial=None, signed=True, offset=None, **kwargs):
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = nvi(close=close, volume=volume, length=length, initial=initial, signed=signed, offset=offset, **kwargs)
        return result

    @finalize
    def obv(self, close=None, volume=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = obv(close=close, volume=volume, offset=offset, **kwargs)
        return result

    @finalize
    def pvi(self, close=None, volume=None, length=None, initial=None, signed=True, offset=None, **kwargs):
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = pvi(close=close, volume=volume, length=length, initial=initial, signed=signed, offset=offset, **kwargs)
        return result

    @finalize
    def pvol(self, close=None, volume=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = pvol(close=close, volume=volume, offset=offset, **kwargs)
        return result

    @finalize
    def pvt(self, close=None, volume=None, offset=None, **kwargs):
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = pvt(close=close, volume=volume, offset=offset, **kwargs)
        return result

    @finalize
    def vp(self, close=None, volume=None, width=None, percent=None, **kwargs):
        close = self._get_column(close, 'close')
        volume = self._get_column(volume, 'volume')

        result = vp(close=close, volume=volume, width=width, percent=percent, **kwargs)
        return result
