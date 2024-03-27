# -*- coding: utf-8 -*-
from numpy import log, log10
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import (
    v_bool,
    v_drift,
    v_offset,
    v_pos_default,
    v_scalar,
    v_series
)
from pandas_ta.volatility import atr



def chop(
    high: Series, low: Series, close: Series,
    length: Int = None, atr_length: Int = None,
    ln: bool = None, scalar: IntFloat = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Choppiness Index (CHOP)

    The Choppiness Index was created by Australian commodity trader
    E.W. Dreiss and is designed to determine if the market is choppy
    (trading sideways) or not choppy (trading within a trend in either
    direction). Values closer to 100 implies the underlying is choppier
    whereas values closer to 0 implies the underlying is trending.

    Sources:
        https://www.tradingview.com/scripts/choppinessindex/
        https://www.motivewave.com/studies/choppiness_index.htm

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        atr_length (int): Length for ATR. Default: 1
        ln (bool): When True, it uses 'ln' instead of 'log10'. Default: False
        scalar (float): How much to magnify. Default: 100
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 14)
    high = v_series(high, length + 1)
    low = v_series(low, length + 1)
    close = v_series(close, length + 1)

    if high is None or low is None or close is None:
        return

    atr_length = v_pos_default(atr_length, 1)
    scalar = v_scalar(scalar, 100)
    ln = v_bool(ln, False)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    diff = high.rolling(length).max() - low.rolling(length).min()

    atr_ = atr(high=high, low=low, close=close, length=atr_length)
    atr_sum = atr_.rolling(length).sum()

    chop = scalar
    if ln:
        chop *= (log(atr_sum) - log(diff)) / log(length)
    else:
        chop *= (log10(atr_sum) - log10(diff)) / log10(length)

    # Offset
    if offset != 0:
        chop = chop.shift(offset)

    # Fill
    if "fillna" in kwargs:
        chop.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    chop.name = f"CHOP{'ln' if ln else ''}_{length}_{atr_length}_{scalar}"
    chop.category = "trend"

    return chop
