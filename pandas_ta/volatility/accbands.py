# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.ma import ma
from pandas_ta.utils import non_zero_range, v_drift, v_mamode
from pandas_ta.utils import v_offset, v_pos_default, v_series


def accbands(
    high: Series, low: Series, close: Series, length: Int = None,
    c: IntFloat = None, drift: Int = None, mamode: str = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Acceleration Bands (ACCBANDS)

    Acceleration Bands created by Price Headley plots upper and lower envelope
    bands around a simple moving average.

    Sources:
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/acceleration-bands-abands/

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        c (int): Multiplier. Default: 4
        mamode (str): See ``help(ta.ma)``. Default: 'sma'
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: lower, mid, upper columns.
    """
    # Validate
    length = v_pos_default(length, 20)
    high = v_series(high, length)
    low = v_series(low, length)
    close = v_series(close, length)

    if high is None or low is None or close is None:
        return

    c = v_pos_default(c, 4)
    mamode = v_mamode(mamode, "sma")
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    high_low_range = non_zero_range(high, low)
    hl_ratio = high_low_range / (high + low)
    hl_ratio *= c
    _lower = low * (1 - hl_ratio)
    _upper = high * (1 + hl_ratio)

    lower = ma(mamode, _lower, length=length)
    mid = ma(mamode, close, length=length)
    upper = ma(mamode, _upper, length=length)

    # Offset
    if offset != 0:
        lower = lower.shift(offset)
        mid = mid.shift(offset)
        upper = upper.shift(offset)

    # Fill
    if "fillna" in kwargs:
        lower.fillna(kwargs["fillna"], inplace=True)
        mid.fillna(kwargs["fillna"], inplace=True)
        upper.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        lower.fillna(method=kwargs["fill_method"], inplace=True)
        mid.fillna(method=kwargs["fill_method"], inplace=True)
        upper.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    lower.name = f"ACCBL_{length}"
    mid.name = f"ACCBM_{length}"
    upper.name = f"ACCBU_{length}"
    mid.category = upper.category = lower.category = "volatility"

    data = {lower.name: lower, mid.name: mid, upper.name: upper}
    accbandsdf = DataFrame(data)
    accbandsdf.name = f"ACCBANDS_{length}"
    accbandsdf.category = mid.category

    return accbandsdf
