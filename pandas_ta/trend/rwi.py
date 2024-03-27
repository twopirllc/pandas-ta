# -*- coding: utf-8 -*-
from numpy import isnan
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.volatility import atr
from pandas_ta.utils import (
    v_drift,
    v_mamode,
    v_offset,
    v_pos_default,
    v_series,
    v_talib
)



def rwi(
    high: Series, low: Series, close: Series,
    length: Int = None, mamode: str = None, talib: bool = None,
    drift: Int = None, offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Random Walk Index (RWI)

    This indicator aims to differntiate whether the price is following a specific trend
    or is doing a random walk

    Sources:
        https://www.technicalindicators.net/indicators-technical-analysis/168-rwi-random-walk-index

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        mamode (str): See ```help(ta.ma)```. Default: 'rma'
        talib (bool): If TA Lib is installed and talib is True, Returns the
            TA Lib version. Default: True
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: high, low columns.
    """
    # Validate
    length = v_pos_default(length, 14)
    _length = length + 1
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return

    mamode = v_mamode(mamode, "rma")
    mode_tal = v_talib(talib)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    atr_ = atr(
        high=high, low=low, close=close,
        length=length, mamode=mamode, talib=mode_tal
    )
    if all(isnan(atr_)):
        return  # Emergency Break

    denom = atr_ * (length ** 0.5)
    rwi_high = (high - low.shift(length)) / denom
    rwi_low = (high.shift(length) - low) / denom

    # Offset
    if offset != 0:
        rwi_high = rwi_high.shift(offset)
        rwi_low = rwi_low.shift(offset)

    # Fill
    if "fillna" in kwargs:
        rwi_high.fillna(kwargs["fillna"], inplace=True)
        rwi_low.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    rwi_high.name = f"RWIh_{length}"
    rwi_low.name = f"RWIl_{length}"
    rwi_high.category = rwi_low.category = "trend"

    # Prepare DataFrame to return
    data = {rwi_high.name: rwi_high, rwi_low.name: rwi_low}
    df = DataFrame(data, index=close.index)
    df.name = f"RWI_{length}"
    df.category = "trend"

    return df
