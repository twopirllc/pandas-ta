# -*- coding: utf-8 -*-

import os
import sys
from os.path import dirname, abspath, join
from glob import glob
import importlib
import pandas_ta

def import_dir(dir_path, create_categories=True, verbose=True):

    # ensure that the passed directory exists / is readable
    if not os.path.exists(dir_path):
        print(f"[X] Unable to read the directory '{dir_path}'.")
        return
   
    # list the contents of the directory
    dirs = glob(abspath(join(dir_path, '*')))

    # optionally add any missing category subdirectories
    if create_categories:
        for sd in [*pandas_ta.Category]:
            d = abspath(join(dir_path, sd)
            if not os.path.exists(d):
                os.makedirs(directory

    # traverse the directory, importing all modules found there
    for d in dirs:
        dirname = os.path.basename(d)

        if dirname not in [*pandas_ta.Category]:
            print(f"[i] Skipping the sub-directory '{dirname}' since it's not a pandas_ta category.")
            continue

        for module in glob(abspath(join(dir_path, dirname, '*.py'))):
            module = os.path.splitext(os.path.basename(module))[0]

            if module in pandas_ta.Category[dirname]:
                print(f"[X] Skipping the custom module '{module}' since a function with that name already exists in pandas_ta.")
                continue

            # import the module and add it to the correct category
            pandas_ta.Category[dirname].append(module)
            if d not in sys.path:
                sys.path.append(d) 
            importlib.import_module(module, d)

            if verbose:
                print(f"[i] Successfully imported the module '{module}' into category '{dirname}'.")

import_dir.__doc__ = \
"""
This method allows you to experiment and develop your own technical analysis
indicators independantly in a separate local directory of your choice but
still use them seamlessly together with the existing pandas_ta functions just 
like if they were part of pandas_ta.

If you at some late point would like to push them into the pandas_ta library
you can do so very easily by following the step by step instruction here
https://github.com/twopirllc/pandas-ta/issues/264.

----------------------------------

By default, the 'ta' extension uses lower case column names: open, high,
low, close, and volume. You can override the defaults by providing the it's
replacement name when calling the indicator. For example, to call the
indicator hl2().

With 'default' columns: open, high, low, close, and volume.
>>> df.ta.hl2()
>>> df.ta(kind="hl2")

With DataFrame columns: Open, High, Low, Close, and Volume.
>>> df.ta.hl2(high="High", low="Low")
>>> df.ta(kind="hl2", high="High", low="Low")

If you do not want to use a DataFrame Extension, just call it normally.
>>> sma10 = ta.sma(df["Close"]) # Default length=10
>>> sma50 = ta.sma(df["Close"], length=50)
>>> ichimoku, span = ta.ichimoku(df["High"], df["Low"], df["Close"])

Args:
    kind (str, optional): Default: None. Kind is the 'name' of the indicator.
        It converts kind to lowercase before calling.
    timed (bool, optional): Default: False. Curious about the execution
        speed?
    kwargs: Extension specific modifiers.
        append (bool, optional): Default: False. When True, it appends the
        resultant column(s) to the DataFrame.

Returns:
    Most Indicators will return a Pandas Series. Others like MACD, BBANDS,
    KC, et al will return a Pandas DataFrame. Ichimoku on the other hand
    will return two DataFrames, the Ichimoku DataFrame for the known period
    and a Span DataFrame for the future of the Span values.

Let's get started!

1. Loading the 'ta' module:
>>> import pandas as pd
>>> import ta as ta

2. Load some data:
>>> df = pd.read_csv("AAPL.csv", index_col="date", parse_dates=True)

3. Help!
3a. General Help:
>>> help(df.ta)
>>> df.ta()
3b. Indicator Help:
>>> help(ta.apo)
3c. Indicator Extension Help:
>>> help(df.ta.apo)

4. Ways of calling an indicator.
4a. Standard: Calling just the APO indicator without "ta" DataFrame extension.
>>> ta.apo(df["close"])
4b. DataFrame Extension: Calling just the APO indicator with "ta" DataFrame extension.
>>> df.ta.apo()
4c. DataFrame Extension (kind): Calling APO using 'kind'
>>> df.ta(kind="apo")
4d. Strategy:
>>> df.ta.strategy("All") # Default
>>> df.ta.strategy(ta.Strategy("My Strat", ta=[{"kind": "apo"}])) # Custom

5. Working with kwargs
5a. Append the result to the working df.
>>> df.ta.apo(append=True)
5b. Timing an indicator.
>>> apo = df.ta(kind="apo", timed=True)
>>> print(apo.timed)
"""
