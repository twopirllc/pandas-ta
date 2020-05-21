# -*- coding: utf-8 -*-
from pandas import DataFrame
from ..overlap.ema import ema
from ..overlap.sma import sma
from ..statistics.stdev import stdev
from ..utils import get_offset, verify_series

def bbands(close, length=None, std=None, mamode=None, offset=None, **kwargs):
    """Indicator: Bollinger Bands (BBANDS)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 5
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    std = float(std) if std and std > 0 else 2.
    mamode = mamode.lower() if mamode else 'sma'
    offset = get_offset(offset)

    # Calculate Result
    standard_deviation = stdev(close=close, length=length)
    deviations = std * standard_deviation

    if mamode is None or mamode == 'sma':
        mid = sma(close=close, length=length)
    elif mamode == 'ema':
        mid = ema(close=close, length=length, **kwargs)

    lower = mid - deviations
    upper = mid + deviations

    # Offset
    if offset != 0:
        lower = lower.shift(offset)
        mid = mid.shift(offset)
        upper = upper.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        lower.fillna(kwargs['fillna'], inplace=True)
        mid.fillna(kwargs['fillna'], inplace=True)
        upper.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        lower.fillna(method=kwargs['fill_method'], inplace=True)
        mid.fillna(method=kwargs['fill_method'], inplace=True)
        upper.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    lower.name = f"BBL_{length}"
    mid.name = f"BBM_{length}"
    upper.name = f"BBU_{length}"
    mid.category = upper.category = lower.category = 'volatility'

    # Prepare DataFrame to return
    data = {lower.name: lower, mid.name: mid, upper.name: upper}
    bbandsdf = DataFrame(data)
    bbandsdf.name = f"BBANDS_{length}"
    bbandsdf.category = 'volatility'

    return bbandsdf



bbands.__doc__ = \
"""Bollinger Bands (BBANDS)

A popular volatility indicator.

Sources:
    https://www.tradingview.com/wiki/Bollinger_Bands_(BB)

Calculation:
    Default Inputs:
        length=20, std=2
    EMA = Exponential Moving Average
    SMA = Simple Moving Average
    STDEV = Standard Deviation
    stdev = STDEV(close, length)
    if 'ema':
        MID = EMA(close, length)
    else:
        MID = SMA(close, length)
    
    LOWER = MID - std * stdev
    UPPER = MID + std * stdev

Args:
    close (pd.Series): Series of 'close's
    length (int): The short period.  Default: 20
    std (int): The long period.   Default: 2
    mamode (str): Two options: None or 'ema'.  Default: 'ema'
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: lower, mid, upper columns.
"""