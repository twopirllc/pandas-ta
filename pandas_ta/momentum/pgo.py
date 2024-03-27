# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.overlap import ema, sma
from pandas_ta.utils import v_offset, v_pos_default, v_series
from pandas_ta.volatility import atr



def pgo(
    high: Series, low: Series, close: Series, length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Pretty Good Oscillator (PGO)

    The Pretty Good Oscillator indicator was created by Mark Johnson to
    measure the distance of the current close from its N-day SMA, expressed
    in terms of an average true range over a similar period. Johnson's
    approach was to use it as a breakout system for longer term trades.
    Long if greater than 3.0 and short if less than -3.0.

    Sources:
        https://library.tradingtechnologies.com/trade/chrt-ti-pretty-good-oscillator.html

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 14)
    _length = 2 * length
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return

    offset = v_offset(offset)

    # Calculate
    pgo = (close - sma(close, length)) \
        / ema(atr(high, low, close, length), length)

    # Offset
    if offset != 0:
        pgo = pgo.shift(offset)

    # Fill
    if "fillna" in kwargs:
        pgo.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    pgo.name = f"PGO_{length}"
    pgo.category = "momentum"

    return pgo
