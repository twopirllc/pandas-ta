# -*- coding: utf-8 -*-
from pandas import DataFrame
from ..overlap.ema import ema
from ..utils import get_offset, verify_series

def ppo(close, fast=None, slow=None, signal=None, offset=None, **kwargs):
    """Indicator: Percentage Price Oscillator (PPO)"""
    # Validate Arguments
    close = verify_series(close)
    fast = int(fast) if fast and fast > 0 else 12
    slow = int(slow) if slow and slow > 0 else 26
    signal = int(signal) if signal and signal > 0 else 9
    if slow < fast:
        fast, slow = slow, fast
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else fast
    offset = get_offset(offset)

    # Calculate Result
    fastma = close.rolling(fast, min_periods=min_periods).mean()
    slowma = close.rolling(slow, min_periods=min_periods).mean()

    ppo = 100 * (fastma - slowma) / slowma
    signalma = ema(close=ppo, length=signal, **kwargs)
    histogram = ppo - signalma

    # Offset
    if offset != 0:
        ppo = ppo.shift(offset)
        signalma = signalma.shift(offset)
        histogram = histogram.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        ppo.fillna(kwargs['fillna'], inplace=True)
        histogram.fillna(kwargs['fillna'], inplace=True)
        signalma.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        ppo.fillna(method=kwargs['fill_method'], inplace=True)
        histogram.fillna(method=kwargs['fill_method'], inplace=True)
        signalma.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    _props = f"_{fast}_{slow}_{signal}"
    ppo.name = f"PPO{_props}"
    histogram.name = f"PPOH{_props}"
    signalma.name = f"PPOS{_props}"
    ppo.category = histogram.category = signalma.category = 'momentum'

    # Prepare DataFrame to return
    data = {ppo.name: ppo, histogram.name: histogram, signalma.name: signalma}
    ppodf = DataFrame(data)
    ppodf.name = f"PPO{_props}"
    ppodf.category = 'momentum'

    return ppodf



ppo.__doc__ = \
"""Percentage Price Oscillator (PPO)

The Percentage Price Oscillator is similar to MACD in measuring momentum.

Sources:
    https://www.tradingview.com/wiki/MACD_(Moving_Average_Convergence/Divergence)

Calculation:
    Default Inputs:
        fast=12, slow=26
    SMA = Simple Moving Average
    EMA = Exponential Moving Average
    fast_sma = SMA(close, fast)
    slow_sma = SMA(close, slow)
    PPO = 100 * (fast_sma - slow_sma) / slow_sma
    Signal = EMA(PPO, signal)
    Histogram = PPO - Signal

Args:
    close(pandas.Series): Series of 'close's
    fast(int): The short period.  Default: 12
    slow(int): The long period.   Default: 26
    signal(int): The signal period.   Default: 9
    offset(int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: ppo, histogram, signal columns
"""