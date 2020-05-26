# -*- coding: utf-8 -*-
from pandas import DataFrame, concat
from ..overlap.ema import ema
from ..utils import get_offset, verify_series, signals

def macd(close, fast=None, slow=None, signal=None, offset=None, **kwargs):
    """Indicator: Moving Average, Convergence/Divergence (MACD)"""
    # Validate arguments
    close = verify_series(close)
    fast = int(fast) if fast and fast > 0 else 12
    slow = int(slow) if slow and slow > 0 else 26
    signal = int(signal) if signal and signal > 0 else 9
    if slow < fast:
        fast, slow = slow, fast
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else fast
    offset = get_offset(offset)

    # Calculate Result
    fastma = ema(close, length=fast, **kwargs)
    slowma = ema(close, length=slow, **kwargs)

    macd = fastma - slowma
    signalma = ema(close=macd, length=signal, **kwargs)
    histogram = macd - signalma

    # Offset
    if offset != 0:
        macd = macd.shift(offset)
        histogram = histogram.shift(offset)
        signalma = signalma.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        macd.fillna(kwargs['fillna'], inplace=True)
        histogram.fillna(kwargs['fillna'], inplace=True)
        signalma.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        macd.fillna(method=kwargs['fill_method'], inplace=True)
        histogram.fillna(method=kwargs['fill_method'], inplace=True)
        signalma.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    macd.name = f"MACD_{fast}_{slow}_{signal}"
    histogram.name = f"MACDH_{fast}_{slow}_{signal}"
    signalma.name = f"MACDS_{fast}_{slow}_{signal}"
    macd.category = histogram.category = signalma.category = 'momentum'

    # Prepare DataFrame to return
    data = {macd.name: macd, histogram.name: histogram, signalma.name: signalma}
    macddf = DataFrame(data)
    macddf.name = f"MACD_{fast}_{slow}_{signal}"
    macddf.category = 'momentum'

    signal_indicators = kwargs.pop('signal_indicators', False)
    if signal_indicators:
        signalsdf = concat(
            [
                macddf,
                signals(
                    indicator=histogram,
                    xa=kwargs.pop('xa', 0),
                    xb=kwargs.pop('xb', None),
                    xserie=kwargs.pop('xserie', None),
                    xserie_a=kwargs.pop('xserie_a', None),
                    xserie_b=kwargs.pop('xserie_b', None),
                    cross_values=kwargs.pop('cross_values', True),
                    cross_series=kwargs.pop('cross_series', True),
                    offset=offset,
                ),
                signals(
                    indicator=macd,
                    xa=kwargs.pop('xa', 0),
                    xb=kwargs.pop('xb', None),
                    xserie=kwargs.pop('xserie', None),
                    xserie_a=kwargs.pop('xserie_a', None),
                    xserie_b=kwargs.pop('xserie_b', None),
                    cross_values=kwargs.pop('cross_values', False),
                    cross_series=kwargs.pop('cross_series', True),
                    offset=offset,
                ),
            ],
            axis=1
        )

        return signalsdf
    else:
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