# -*- coding: utf-8 -*-
from pandas import DataFrame
from ..momentum.macd import macd
from ..utils import above_value, below_value, cross_value

def macd_signals(close, fast=None, slow=None, signal=None, offset=None, **kwargs):
    """Indicator: Signals based on Moving Average, Convergence/Divergence (MACD)"""
    macd_df = macd(close, fast=fast, slow=slow, signal=signal, offset=offset, **kwargs)
    histogram_col = macd_df.columns.values[macd_df.columns.str.startswith('MACDH')][0]
    histogram_serie = macd_df[histogram_col]
    macd_col = macd_df.columns.values[macd_df.columns.str.startswith('MACD_')][0]
    macd_serie = macd_df[macd_col]

    signals_above = cross_value(histogram_serie, 0, above=True, asint=True, **kwargs)
    signals_below = cross_value(histogram_serie, 0, above=False, asint=True, **kwargs)
    bull = above_value(histogram_serie, 0, asint=True, **kwargs)
    bear = below_value(histogram_serie, 0, asint=True, **kwargs)

    # Name and Categorize it
    # Not needed because above_value/below_value is already naming
    signals_above.name = f"{macd_serie.name}_X_BULL" 
    signals_below.name = f"{macd_serie.name}_X_BEAR"
    bull.name = f"{macd_serie.name}_BULL" 
    bear.name = f"{macd_serie.name}_BEAR"
    signals_above.category = signals_below.category = bull.category = bear.category = 'signals'

    # Prepare DataFrame to return
    data = {
        signals_above.name: signals_above,
        signals_below.name: signals_below,
        bull.name: bull,
        bear.name: bear
    }

    macddf = DataFrame(data)
    macddf.name = f"{macd_serie.name}_signals"
    macddf.category = 'signals'

    return macddf



macd.__doc__ = \
"""Moving Average Convergence Divergence (MACD)

The MACD is a popular indicator to that is used to identify a security's trend.
While APO and MACD are the same calculation, MACD also returns two more series
called Signal and Histogram.  The Signal is an EMA of MACD and the Histogram is
the difference of MACD and Signal.

Sources:
    https://www.tradingview.com/wiki/MACD_(Moving_Average_Convergence/Divergence)

Calculation:
    Default Inputs:
        fast=12, slow=26, signal=9
    EMA = Exponential Moving Average
    MACD = EMA(close, fast) - EMA(close, slow)
    Signal = EMA(MACD, signal)
    Histogram = MACD - Signal

Args:
    close (pd.Series): Series of 'close's
    fast (int): The short period.  Default: 12
    slow (int): The long period.   Default: 26
    signal (int): The signal period.   Default: 9
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: macd, histogram, signal columns.
"""