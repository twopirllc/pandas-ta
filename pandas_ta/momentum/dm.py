# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.maps import Imports
from pandas_ta.utils import (
    v_drift,
    v_mamode,
    v_offset,
    v_pos_default,
    v_series,
    v_talib,
    zero
)



def dm(
    high: Series, low: Series, length: Int = None,
    mamode: str = None, talib: bool = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Directional Movement (DM)

    The Directional Movement was developed by J. Welles Wilder in 1978
    attempts to determine which direction the price of an asset is moving.
    It compares prior highs and lows to yield to two series +DM and -DM.

    Sources:
        https://www.tradingview.com/pine-script-reference/#fun_dmi
        https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=24&Name=Directional_Movement_Index

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        mamode (str): See ``help(ta.ma)``.  Default: 'rma'
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: DMP (+DM) and DMN (-DM) columns.
    """
    # Validate
    length = v_pos_default(length, 14)
    high = v_series(high, length)
    low = v_series(low, length)

    if high is None or low is None:
        return

    mamode = v_mamode(mamode, "rma")
    mode_tal = v_talib(talib)
    drift = v_drift(drift)
    offset = v_offset(offset)

    if Imports["talib"] and mode_tal and high.size and low.size:
        from talib import MINUS_DM, PLUS_DM
        pos = PLUS_DM(high, low, length)
        neg = MINUS_DM(high, low, length)
    else:
        up = high - high.shift(drift)
        dn = low.shift(drift) - low

        pos_ = ((up > dn) & (up > 0)) * up
        neg_ = ((dn > up) & (dn > 0)) * dn

        pos_ = pos_.apply(zero)
        neg_ = neg_.apply(zero)

        # Not the same values as TA Lib's -+DM (Good First Issue)
        pos = ma(mamode, pos_, length=length, talib=mode_tal)
        neg = ma(mamode, neg_, length=length, talib=mode_tal)

    # Offset
    if offset != 0:
        pos = pos.shift(offset)
        neg = neg.shift(offset)

    # Fill
    if "fillna" in kwargs:
        pos.fillna(kwargs["fillna"], inplace=True)
        neg.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"_{length}"
    data = {f"DMP{_props}": pos, f"DMN{_props}": neg}
    df = DataFrame(data, index=high.index)
    df.name = f"DM{_props}"
    df.category = "momentum"

    return df
