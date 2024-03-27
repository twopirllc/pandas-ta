# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_pos_default, v_series



def donchian(
    high: Series, low: Series,
    lower_length: Int = None, upper_length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Donchian Channels (DC)

    Donchian Channels are used to measure volatility, similar to
    Bollinger Bands and Keltner Channels.

    Sources:
        https://www.tradingview.com/wiki/Donchian_Channels_(DC)

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        lower_length (int): The short period. Default: 20
        upper_length (int): The short period. Default: 20
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: lower, mid, upper columns.
    """
    # Validate
    lower_length = v_pos_default(lower_length, 20)
    upper_length = v_pos_default(upper_length, 20)
    lmin_periods = int(kwargs.pop("lmin_periods", lower_length))
    umin_periods = int(kwargs.pop("umin_periods", upper_length))

    _length = max(lower_length, lmin_periods, upper_length, umin_periods)
    high = v_series(high, _length)
    low = v_series(low, _length)

    if high is None or low is None:
        return

    offset = v_offset(offset)

    # Calculate
    lower = low.rolling(lower_length, min_periods=lmin_periods).min()
    upper = high.rolling(upper_length, min_periods=umin_periods).max()
    mid = 0.5 * (lower + upper)

    # Fill
    if "fillna" in kwargs:
        lower.fillna(kwargs["fillna"], inplace=True)
        mid.fillna(kwargs["fillna"], inplace=True)
        upper.fillna(kwargs["fillna"], inplace=True)

    # Offset
    if offset != 0:
        lower = lower.shift(offset)
        mid = mid.shift(offset)
        upper = upper.shift(offset)

    # Name and Category
    lower.name = f"DCL_{lower_length}_{upper_length}"
    mid.name = f"DCM_{lower_length}_{upper_length}"
    upper.name = f"DCU_{lower_length}_{upper_length}"
    mid.category = upper.category = lower.category = "volatility"

    data = {lower.name: lower, mid.name: mid, upper.name: upper}
    df = DataFrame(data, index=high.index)
    df.name = f"DC_{lower_length}_{upper_length}"
    df.category = mid.category

    return df
