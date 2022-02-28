# -*- coding: utf-8 -*-
from numpy import nan
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.utils import v_bool, v_offset, v_pos_default, v_series, v_talib

try:
    from numba import njit
except ImportError:
    def njit(_): return _

# Almost there
# @njit
# def np_ema(x: np.ndarray, n: int):
#     m = x.size
#     result = np.zeros(m)
#     a = 1 / (n + 1)
#     for i in range(1, m):
#         result[i] = a * x[i - 1] + (1 - a) * x[i]
#     result[0] = np.nan
#     return result
#     # return np_prepend(result, n - 1)


def ema(
    close: Series, length: Int = None,
    talib: bool = None, presma: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Exponential Moving Average (EMA)

    The Exponential Moving Average is a more responsive moving average
    compared to the Simple Moving Average (SMA). The weights are determined
    by alpha which is proportional to it's length.  There are several
    different methods of calculating EMA. One method uses just the standard
    definition of EMA and another uses the SMA to generate the initial value
    for the rest of the calculation.

    Sources:
        https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_averages
        https://www.investopedia.com/ask/answers/122314/what-exponential-moving-average-ema-formula-and-how-ema-calculated.asp

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        presma (bool, optional): If True, uses SMA for initial value like
            TA Lib. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        adjust (bool, optional): Default: False
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 10)
    close = v_series(close, length)

    if close is None:
        return

    mode_tal = v_talib(talib)
    presma = v_bool(presma, True)
    offset = v_offset(offset)
    adjust = kwargs.setdefault("adjust", False)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import EMA
        ema = EMA(close, length)
    else:
        if presma:  # TA Lib implementation
            close = close.copy()
            sma_nth = close[0:length].mean()
            close[:length - 1] = nan
            close.iloc[length - 1] = sma_nth
        ema = close.ewm(span=length, adjust=adjust).mean()

    # Offset
    if offset != 0:
        ema = ema.shift(offset)

    # Fill
    if "fillna" in kwargs:
        ema.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ema.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    ema.name = f"EMA_{length}"
    ema.category = "overlap"

    return ema
