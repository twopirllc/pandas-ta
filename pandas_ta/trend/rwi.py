# -*- coding: utf-8 -*-
from pandas import DataFrame
from pandas_ta.volatility import atr
from pandas_ta.utils import get_drift, get_offset, verify_series, zero

def rwi(high, low, close, length=None, lensig=None, scalar=None, mamode=None, drift=None, offset=None, **kwargs):
    """Indicator: RWI"""
    # Validate Arguments
    length = length if length and length > 0 else 14
    lensig = lensig if lensig and lensig > 0 else length
    mamode = mamode if isinstance(mamode, str) else "rma"
    scalar = float(scalar) if scalar else 100
    high = verify_series(high, length)
    low = verify_series(low, length)
    close = verify_series(close, length)
    drift = get_drift(drift)
    offset = get_offset(offset)

    if high is None or low is None: return

    # Calculate Result
    atr_ = atr(high=high, low=low, close=close, length=length)

    rwi_high = ((high - low.shift(length)) / (atr_ * (length ** 0.5)))#.shift(-length)
    rwi_low = ((high.shift(length) - low) / (atr_ * (length ** 0.5)))#.shift(-length)

    print((high - low.shift(length)).shift(-length))

    # Offset
    if offset != 0:
        rwi_high = rwi_high.shift(offset)
        rwi_low = rwi_low.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        rwi_high.fillna(kwargs["fillna"], inplace=True)
        rwi_low.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        rwi_high.fillna(method=kwargs["fill_method"], inplace=True)
        rwi_low.fillna(method=kwargs["fill_method"], inplace=True)


    # Name and Categorize it
    rwi_high.name = f"RWI_HIGH_{lensig}"
    rwi_low.name = f"RWI_LOW_{lensig}"

    rwi_high.category = "trend"
    rwi_low.category = "trend"

    # Prepare DataFrame to return
    data = {rwi_high.name: rwi_high, rwi_low.name: rwi_low}
    rwidf = DataFrame(data)
    rwidf.name = f"RWI_{lensig}"
    rwidf.category = "trend"

    return rwidf

rwi.__doc__ = \
"""Random Walk Index (RWI)

This indicator aims to differntiate whether the price is following a specific trend
or is doing a random walk

Sources:
    https://www.technicalindicators.net/indicators-technical-analysis/168-rwi-random-walk-index

Calculation:
    rwihigh = (high - low[length]) / (atr * sqrt(length))
    rwilow = (high[length] - low) / (atr * sqrt(length))

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): It's period. Default: 14
    lensig (int): Signal Length. Like TradingView's default ADX. Default: length
    scalar (float): How much to magnify. Default: 100
    mamode (str): See ```help(ta.ma)```. Default: 'rma'
    drift (int): The difference period. Default: 1
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: high, low columns.
"""
