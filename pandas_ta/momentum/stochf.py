# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    non_zero_range,
    tal_ma,
    v_mamode,
    v_offset,
    v_pos_default,
    v_series,
    v_talib
)



def stochf(
    high: Series, low: Series, close: Series,
    k: Int = None, d: Int = None,
    mamode: str = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Fast Stochastic (STOCHF)

    The Fast Stochastic Oscillator (STOCHF) was developed by George Lane
    in the 1950's. This STOCHF is more volatile than STOCH (help(ta.stoch))
    and it's calculation is similar to STOCH.

    Sources:
        https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=333&Name=KD_-_Fast
        https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/fast-stochastic-indicator/

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        k (int): The Fast %K period. Default: 14
        d (int): The Slow %D period. Default: 3
        mamode (str): See ``help(ta.ma)``. Default: 'sma'
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: Fast %K, %D columns.
    """
    # Validate
    k = v_pos_default(k, 14)
    d = v_pos_default(d, 3)
    _length = k + d - 1
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return

    mamode = v_mamode(mamode, "sma")
    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import STOCHF
        stochf_ = STOCHF(high, low, close, k, d, tal_ma(mamode))
        stochf_k, stochf_d = stochf_[0], stochf_[1]
    else:
        lowest_low = low.rolling(k).min()
        highest_high = high.rolling(k).max()

        stochf_k = 100 * (close - lowest_low) \
            / non_zero_range(highest_high, lowest_low)
        stochfk_fvi = stochf_k.loc[stochf_k.first_valid_index():, ]
        stochf_d = ma(mamode, stochfk_fvi, length=d, talib=mode_tal)

    # Offset
    if offset != 0:
        stochf_k = stochf_k.shift(offset)
        stochf_d = stochf_d.shift(offset)

    # Fill
    if "fillna" in kwargs:
        stochf_k.fillna(kwargs["fillna"], inplace=True)
        stochf_d.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _name = "STOCHF"
    _props = f"_{k}_{d}"
    stochf_k.name = f"{_name}k{_props}"
    stochf_d.name = f"{_name}d{_props}"
    stochf_k.category = stochf_d.category = "momentum"

    data = {stochf_k.name: stochf_k, stochf_d.name: stochf_d}
    df = DataFrame(data, index=close.index)
    df.name = f"{_name}{_props}"
    df.category = stochf_k.category

    return df
