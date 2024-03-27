# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    recent_maximum_index,
    recent_minimum_index,
    v_offset,
    v_pos_default,
    v_scalar,
    v_series,
    v_talib
)



def aroon(
    high: Series, low: Series,
    length: Int = None, scalar: IntFloat = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Aroon & Aroon Oscillator (AROON)

    Aroon attempts to identify if a security is trending and how strong.

    Sources:
        https://www.tradingview.com/wiki/Aroon
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/aroon-ar/

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        length (int): It's period. Default: 14
        scalar (float): How much to magnify. Default: 100
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: aroon_up, aroon_down, aroon_osc columns.
    """
    # Validate
    length = v_pos_default(length, 14)
    high = v_series(high, length + 1)
    low = v_series(low, length + 1)

    if high is None or low is None:
        return

    scalar = v_scalar(scalar, 100)
    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import AROON, AROONOSC
        aroon_down, aroon_up = AROON(high, low, length)
        aroon_osc = AROONOSC(high, low, length)
    else:
        periods_from_hh = high.rolling(length + 1) \
            .apply(recent_maximum_index,raw=True)
        periods_from_ll = low.rolling(length + 1) \
            .apply(recent_minimum_index,raw=True)

        aroon_up = aroon_down = scalar
        aroon_up *= 1 - (periods_from_hh / length)
        aroon_down *= 1 - (periods_from_ll / length)
        aroon_osc = aroon_up - aroon_down

    # Offset
    if offset != 0:
        aroon_up = aroon_up.shift(offset)
        aroon_down = aroon_down.shift(offset)
        aroon_osc = aroon_osc.shift(offset)

    # Fill
    if "fillna" in kwargs:
        aroon_up.fillna(kwargs["fillna"], inplace=True)
        aroon_down.fillna(kwargs["fillna"], inplace=True)
        aroon_osc.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    aroon_up.name = f"AROONU_{length}"
    aroon_down.name = f"AROOND_{length}"
    aroon_osc.name = f"AROONOSC_{length}"

    aroon_down.category = aroon_up.category = aroon_osc.category = "trend"

    data = {
        aroon_down.name: aroon_down,
        aroon_up.name: aroon_up,
        aroon_osc.name: aroon_osc
    }
    df = DataFrame(data, index=high.index)
    df.name = f"AROON_{length}"
    df.category = aroon_down.category

    return df
