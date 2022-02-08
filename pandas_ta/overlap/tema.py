# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.maps import Imports
from pandas_ta.utils import get_offset, verify_series
from .ema import ema


def tema(
    close: Series, length: int = None, talib: bool = None,
    offset: int = None, **kwargs
) -> Series:
    """Triple Exponential Moving Average (TEMA)

    A less laggy Exponential Moving Average.

    Sources:
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/triple-exponential-moving-average-tema/

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        talib (bool): If TA Lib is installed and talib is True, Returns the TA Lib
            version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        adjust (bool): Default: True
        presma (bool, optional): If True, uses SMA for initial value.
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 10
    close = verify_series(close, length)
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if close is None:
        return

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
    if "fill_method" in kwargs:
        tema.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    tema.name = f"TEMA_{length}"
    tema.category = "overlap"

    return tema
