# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.utils import v_offset, v_pos_default, v_series, v_talib
from .ema import ema



def tema(
    close: Series, length: Int = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Triple Exponential Moving Average (TEMA)

    A less laggy Exponential Moving Average.

    Sources:
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/triple-exponential-moving-average-tema/

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        adjust (bool): Default: True
        presma (bool, optional): If True, uses SMA for initial value.
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 10)
    close = v_series(close, 3 * length)

    if close is None:
        return

    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import TEMA
        tema = TEMA(close, length)
    else:
        ema1 = ema(close=close, length=length, talib=mode_tal, **kwargs)
        ema2 = ema(close=ema1, length=length, talib=mode_tal, **kwargs)
        ema3 = ema(close=ema2, length=length, talib=mode_tal, **kwargs)
        tema = 3 * (ema1 - ema2) + ema3

    # Offset
    if offset != 0:
        tema = tema.shift(offset)

    # Fill
    if "fillna" in kwargs:
        tema.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    tema.name = f"TEMA_{length}"
    tema.category = "overlap"

    return tema
