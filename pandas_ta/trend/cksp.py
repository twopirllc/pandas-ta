# -*- coding: utf-8 -*-
from pandas import DataFrame
from ..volatility.atr import atr
from ..utils import get_offset, verify_series

def cksp(high, low, close, p=None, x=None, q=None, offset=None, **kwargs):
    """Indicator: Chande Kroll Stop (CKSP)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    p = int(p) if p and p > 0 else 10
    x = float(x) if x and x > 0 else 1
    q = int(q) if q and q > 0 else 9
    offset = get_offset(offset)

    # Calculate Result
    atr_ = atr(high=high, low=low, close=close, length=p)

    long_stop_ = high.rolling(p).max() - x * atr_
    long_stop = long_stop_.rolling(q).max()

    short_stop_ = high.rolling(p).min() + x * atr_
    short_stop = short_stop_.rolling(q).min()

    # Offset
    if offset != 0:
        long_stop = long_stop.shift(offset)
        short_stop = short_stop.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        long_stop.fillna(kwargs['fillna'], inplace=True)
        short_stop.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        long_stop.fillna(method=kwargs['fill_method'], inplace=True)
        short_stop.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    _props = f"_{p}_{x}_{q}"
    long_stop.name = f"CKSPl{_props}"
    short_stop.name = f"CKSPs{_props}"
    long_stop.category = short_stop.category = 'trend'

    # Prepare DataFrame to return
    ckspdf = DataFrame({long_stop.name: long_stop, short_stop.name: short_stop})
    ckspdf.name = f"CKSP{_props}"
    ckspdf.category = 'trend'

    return ckspdf



cksp.__doc__ = \
"""Chande Kroll Stop (CKSP)

The Tushar Chande and Stanley Kroll in their book
“The New Technical Trader”. It is a trend-following indicator,
identifying your stop by calculating the average true range of
the recent market volatility.

Sources:
    https://www.multicharts.com/discussion/viewtopic.php?t=48914

Calculation:
    Default Inputs:
        p=10, x=1, q=9
    ATR = Average True Range

    LS0 = high.rolling(p).max() - x * ATR(length=p)
    LS = LS0.rolling(q).max()

    SS0 = high.rolling(p).min() + x * ATR(length=p)
    SS = SS0.rolling(q).min()

Args:
    close (pd.Series): Series of 'close's
    p (int): ATR and first stop period.  Default: 10
    x (float): ATR scalar.  Default: 1
    q (int): Second stop period.  Default: 9
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: long and short columns.
"""