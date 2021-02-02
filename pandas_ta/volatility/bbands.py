# -*- coding: utf-8 -*-
from pandas import DataFrame
from pandas_ta.overlap import ma
from pandas_ta.statistics import stdev
from pandas_ta.utils import get_offset, verify_series


def bbands(close, length=None, std=None, mamode=None, offset=None, **kwargs):
    """Indicator: Bollinger Bands (BBANDS)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 5
    std = float(std) if std and std > 0 else 2.0
    mamode = mamode if isinstance(mamode, str) else "sma"
    offset = get_offset(offset)

    # Calculate Result
    standard_deviation = stdev(close=close, length=length)
    deviations = std * standard_deviation

    mid = ma(mamode, close, length=length, **kwargs)

    lower = mid - deviations
    upper = mid + deviations

    bandwidth = 100 * (upper - lower) / mid

    # Offset
    if offset != 0:
        lower = lower.shift(offset)
        mid = mid.shift(offset)
        upper = upper.shift(offset)
        bandwidth = bandwidth.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        lower.fillna(kwargs["fillna"], inplace=True)
        mid.fillna(kwargs["fillna"], inplace=True)
        upper.fillna(kwargs["fillna"], inplace=True)
        bandwidth.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        lower.fillna(method=kwargs["fill_method"], inplace=True)
        mid.fillna(method=kwargs["fill_method"], inplace=True)
        upper.fillna(method=kwargs["fill_method"], inplace=True)
        bandwidth.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    lower.name = f"BBL_{length}_{std}"
    mid.name = f"BBM_{length}_{std}"
    upper.name = f"BBU_{length}_{std}"
    bandwidth.name = f"BBB_{length}_{std}"
    upper.category = lower.category = "volatility"
    mid.category = bandwidth.category = upper.category

    # Prepare DataFrame to return
    data = {
        lower.name: lower, mid.name: mid,
        upper.name: upper, bandwidth.name: bandwidth
    }
    bbandsdf = DataFrame(data)
    bbandsdf.name = f"BBANDS_{length}_{std}"
    bbandsdf.category = mid.category

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
    if "ema":
        MID = EMA(close, length)
    else:
        MID = SMA(close, length)

    LOWER = MID - std * stdev
    UPPER = MID + std * stdev

    BANDWIDTH = 100 * (UPPER - LOWER) / MID

Args:
    close (pd.Series): Series of 'close's
    length (int): The short period. Default: 20
    std (int): The long period. Default: 2
    mamode (str): Two options: "sma" or "ema". Default: "ema"
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: lower, mid, upper, bandwidth columns.
"""
