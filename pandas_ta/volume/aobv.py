# -*- coding: utf-8 -*-
from pandas import DataFrame
from .obv import obv
from ..overlap.ema import ema
from ..overlap.hma import hma
from ..overlap.linreg import linreg
from ..overlap.sma import sma
from ..overlap.wma import wma
from ..trend.long_run import long_run
from ..trend.short_run import short_run
from ..utils import get_offset, verify_series

def aobv(close, volume, fast=None, slow=None, mamode=None, max_lookback=None, min_lookback=None, offset=None, **kwargs):
    """Indicator: Archer On Balance Volume (AOBV)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    offset = get_offset(offset)
    fast = int(fast) if fast and fast > 0 else 2
    slow = int(slow) if slow and slow > 0 else 4
    max_lookback = int(max_lookback) if max_lookback and max_lookback > 0 else 2
    min_lookback = int(min_lookback) if min_lookback and min_lookback > 0 else 2
    if slow < fast:
        fast, slow = slow, fast
    mamode = mamode.upper() if mamode else None
    run_length = kwargs.pop('run_length', 2)

    # Calculate Result
    obv_ = obv(close=close, volume=volume, **kwargs)
    if mamode is None or mamode == 'EMA':
        mamode = 'EMA'
        maf = ema(close=obv_, length=fast, **kwargs)
        mas = ema(close=obv_, length=slow, **kwargs)
    elif mamode == 'HMA':
        maf = hma(close=obv_, length=fast, **kwargs)
        mas = hma(close=obv_, length=slow, **kwargs)
    elif mamode == 'LINREG':
        maf = linreg(close=obv_, length=fast, **kwargs)
        mas = linreg(close=obv_, length=slow, **kwargs)
    elif mamode == 'SMA':
        maf = sma(close=obv_, length=fast, **kwargs)
        mas = sma(close=obv_, length=slow, **kwargs)
    elif mamode == 'WMA':
        maf = wma(close=obv_, length=fast, **kwargs)
        mas = wma(close=obv_, length=slow, **kwargs)

    # When MAs are long and short
    obv_long = long_run(maf, mas, length=run_length)
    obv_short = short_run(maf, mas, length=run_length)

    # Offset
    if offset != 0:
        obv_ = obv_.shift(offset)
        maf = maf.shift(offset)
        mas = mas.shift(offset)
        obv_long = obv_long.shift(offset)
        obv_short = obv_short.shift(offset)

    # # Handle fills
    if 'fillna' in kwargs:
        obv_.fillna(kwargs['fillna'], inplace=True)
        maf.fillna(kwargs['fillna'], inplace=True)
        mas.fillna(kwargs['fillna'], inplace=True)
        obv_long.fillna(kwargs['fillna'], inplace=True)
        obv_short.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        obv_.fillna(method=kwargs['fill_method'], inplace=True)
        maf.fillna(method=kwargs['fill_method'], inplace=True)
        mas.fillna(method=kwargs['fill_method'], inplace=True)
        obv_long.fillna(method=kwargs['fill_method'], inplace=True)
        obv_short.fillna(method=kwargs['fill_method'], inplace=True)

    # Prepare DataFrame to return
    data = {
        obv_.name: obv_,
        f"OBV_min_{min_lookback}": obv_.rolling(min_lookback).min(),
        f"OBV_max_{max_lookback}": obv_.rolling(max_lookback).max(),
        f"OBV_{maf.name}": maf,
        f"OBV_{mas.name}": mas,
        f"AOBV_LR_{run_length}": obv_long,
        f"AOBV_SR_{run_length}": obv_short
    }
    aobvdf = DataFrame(data)

    # Name and Categorize it
    aobvdf.name = f"AOBV_{mamode}_{fast}_{slow}_{min_lookback}_{max_lookback}_{run_length}"
    aobvdf.category = 'volume'

    return aobvdf
