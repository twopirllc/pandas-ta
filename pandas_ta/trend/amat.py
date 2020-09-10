# -*- coding: utf-8 -*-
from pandas import DataFrame
from .long_run import long_run
from .short_run import short_run
from pandas_ta.overlap import ema, hma, linreg, rma, sma, wma
from pandas_ta.utils import get_offset, verify_series

def amat(close=None, fast=None, slow=None, mamode=None, lookback=None, offset=None, **kwargs):
    """Indicator: Archer Moving Averages Trends (AMAT)"""
    # Validate Arguments
    close = verify_series(close)
    fast = int(fast) if fast and fast > 0 else 8
    slow = int(slow) if slow and slow > 0 else 21
    lookback = int(lookback) if lookback and lookback > 0 else 2
    mamode = mamode.lower() if mamode else "ema"
    offset = get_offset(offset)

    # Calculate Result
    if mamode == "hma":
        fast_ma = hma(close=close, length=fast, **kwargs)
        slow_ma = hma(close=close, length=slow, **kwargs)
    elif mamode == "linreg":
        fast_ma = linreg(close=close, length=fast, **kwargs)
        slow_ma = linreg(close=close, length=slow, **kwargs)
    elif mamode == "rma":
        fast_ma = rma(close=close, length=fast, **kwargs)
        slow_ma = rma(close=close, length=slow, **kwargs)
    elif mamode == "sma":
        fast_ma = sma(close=close, length=fast, **kwargs)
        slow_ma = sma(close=close, length=slow, **kwargs)
    elif mamode == "wma":
        fast_ma = wma(close=close, length=fast, **kwargs)
        slow_ma = wma(close=close, length=slow, **kwargs)
    else: # "ema"
        fast_ma = ema(close=close, length=fast, **kwargs)
        slow_ma = ema(close=close, length=slow, **kwargs)


    mas_long = long_run(fast_ma, slow_ma, length=lookback)
    mas_short = short_run(fast_ma, slow_ma, length=lookback)

    # Offset
    if offset != 0:
        mas_long = mas_long.shift(offset)
        mas_short = mas_short.shift(offset)

    # # Handle fills
    if "fillna" in kwargs:
        mas_long.fillna(kwargs["fillna"], inplace=True)
        mas_short.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        mas_long.fillna(method=kwargs["fill_method"], inplace=True)
        mas_short.fillna(method=kwargs["fill_method"], inplace=True)

    # Prepare DataFrame to return
    amatdf = DataFrame({
        f"AMAT_{mas_long.name}": mas_long,
        f"AMAT_{mas_short.name}": mas_short
    })

    # Name and Categorize it
    amatdf.name = f"AMAT_{mamode.upper()}_{fast}_{slow}_{lookback}"
    amatdf.category = "trend"

    return amatdf