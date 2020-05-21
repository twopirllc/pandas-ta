# -*- coding: utf-8 -*-
from pandas import DataFrame
from ..momentum.rsi import rsi
from ..utils import above_value, below_value

def rsi_signals(close, above_val=None, below_val=None, length=None, drift=None, offset=None, **kwargs):
    """Indicator: Overbought or Oversold based on Relative Strength Index (RSI)"""
    rsi_series = rsi(close, length=None, drift=None, offset=None, **kwargs)
    above_val = int(above_val) if above_val and above_val > 0 else 80
    below_val = int(below_val) if below_val and below_val > 0 else 20

    above = above_value(rsi_series, above_val, asint=True, **kwargs)
    below = below_value(rsi_series, below_val, asint=True, **kwargs)

    # Name and Categorize it
    # Not needed because above_value/below_value is already naming
    # above.name = f"RSI_{length}_A_{above_val}" 
    # below.name = f"RSI_{length}_B_{below_val}"
    above.category = below.category = 'signals'

    # Prepare DataFrame to return
    data = {above.name: above, below.name: below}
    rsidf = DataFrame(data)
    rsidf.name = f"RSI_signals"
    rsidf.category = 'signals'

    return rsidf



rsi.__doc__ = \
"""Overbought or Oversold based on Relative Strength Index (RSI)

The Relative Strength Index is popular momentum oscillator used to measure the
velocity as well as the magnitude of directional price movements. RSI reading 
above 0.8 is considered overbought, while a reading below 0.2 is considered oversold.

Sources:
    https://www.tradingview.com/wiki/Relative_Strength_Index_(RSI)

Calculation:
    Default Inputs:
        length=14, drift=1
    ABS = Absolute Value
    EMA = Exponential Moving Average
    positive = close if close.diff(drift) > 0 else 0
    negative = close if close.diff(drift) < 0 else 0
    pos_avg = EMA(positive, length)
    neg_avg = ABS(EMA(negative, length))
    RSI = 100 * pos_avg / (pos_avg + neg_avg)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    drift (int): The difference period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""