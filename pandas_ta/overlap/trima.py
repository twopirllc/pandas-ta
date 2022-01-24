# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.maps import Imports
from pandas_ta.utils import get_offset, verify_series
from .sma import sma


def trima(
        close: Series, length: int = None, talib: bool = None,
        offset: int = None, **kwargs
    ) -> Series:
    """Triangular Moving Average (TRIMA)

    A weighted moving average where the shape of the weights are triangular and the
    greatest weight is in the middle of the period.

    Sources:
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/triangular-moving-average-trima/
        tma = sma(sma(src, ceil(length / 2)), floor(length / 2) + 1)  # Tradingview
        trima = sma(sma(x, n), n)  # Tradingview

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        talib (bool): If TA Lib is installed and talib is True, Returns the TA Lib
            version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        adjust (bool): Default: True
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

    if close is None: return

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import TRIMA
        trima = TRIMA(close, length)
    else:
        half_length = round(0.5 * (length + 1))
        sma1 = sma(close, length=half_length, talib=mode_tal)
        trima = sma(sma1, length=half_length, talib=mode_tal)

    # Offset
    if offset != 0:
        trima = trima.shift(offset)

    # Fill
    if "fillna" in kwargs:
        trima.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        trima.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    trima.name = f"TRIMA_{length}"
    trima.category = "overlap"

    return trima
