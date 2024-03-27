# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.overlap import ema
from pandas_ta.utils import v_offset, v_pos_default, v_series



def eri(
    high: Series, low: Series, close: Series, length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Elder Ray Index (ERI)

    Elder's Bulls Ray Index contains his Bull and Bear Powers. Which are
    useful ways to look at the price and see the strength behind the market.
    Bull Power measures the capability of buyers in the market, to lift
    prices above an average consensus of value.

    Bears Power measures the capability of sellers, to drag prices below
    an average consensus of value. Using them in tandem with a measure of
    trend allows you to identify favourable entry points.

    Sources:
        https://admiralmarkets.com/education/articles/forex-indicators/bears-and-bulls-power-indicator

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: bull power and bear power columns.
    """
    # Validate
    length = v_pos_default(length, 13)
    high = v_series(high, length)
    low = v_series(low, length)
    close = v_series(close, length)

    if high is None or low is None or close is None:
        return

    offset = v_offset(offset)

    # Calculate
    ema_ = ema(close, length)
    bull = high - ema_
    bear = low - ema_

    # Offset
    if offset != 0:
        bull = bull.shift(offset)
        bear = bear.shift(offset)

    # Fill
    if "fillna" in kwargs:
        bull.fillna(kwargs["fillna"], inplace=True)
        bear.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    bull.name = f"BULLP_{length}"
    bear.name = f"BEARP_{length}"
    bull.category = bear.category = "momentum"

    data = {bull.name: bull, bear.name: bear}
    df = DataFrame(data, index=close.index)
    df.name = f"ERI_{length}"
    df.category = bull.category

    return df
