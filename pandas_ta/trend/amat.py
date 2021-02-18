# -*- coding: utf-8 -*-
from pandas import DataFrame
from .long_run import long_run
from .short_run import short_run
from pandas_ta.overlap import ma
from pandas_ta.utils import get_offset, verify_series


def amat(close=None, fast=None, slow=None, mamode=None, lookback=None, slope_length=None, offset=None, **kwargs):
    """Indicator: Archer Moving Averages Trends (AMAT)"""
    # Validate Arguments
    close = verify_series(close)
    fast = int(fast) if fast and fast > 0 else 8
    slow = int(slow) if slow and slow > 0 else 21
    lookback = int(lookback) if lookback and lookback > 0 else 2
    mamode = mamode.lower() if isinstance(mamode, str) else "ema"
    offset = get_offset(offset)

    # # Calculate Result
    fast_ma = ma(mamode, close, length=fast, **kwargs)
    slow_ma = ma(mamode, close, length=slow, **kwargs)

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
        f"AMAT{mamode[0]}_{mas_long.name}": mas_long,
        f"AMAT{mamode[0]}_{mas_short.name}": mas_short
    })

    # Name and Categorize it
    amatdf.name = f"AMAT_{mamode.upper()}_{fast}_{slow}_{lookback}"
    amatdf.category = "trend"

    return amatdf
