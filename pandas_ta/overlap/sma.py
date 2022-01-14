# -*- coding: utf-8 -*-
from pandas_ta import Imports, np, pd
from pandas_ta.utils import get_offset, np_prepend, verify_series

try:
    from numba import njit
except ImportError:
    njit = lambda _: _


@njit
def np_sma(x: np.ndarray, n: int):
    """https://github.com/numba/numba/issues/4119"""
    result = np.convolve(np.ones(n) / n, x)[n - 1:1 - n]
    return np_prepend(result, n - 1)

## SMA: Alternative Implementations
# @njit
# def np_sma(x: np.ndarray, n: int):
#     result = np.convolve(x, np.ones(n), mode="valid") / n
#     return np_prepend(result, n - 1)


# @njit
# def np_sma(x: np.ndarray, n: int):
#     csum = np.cumsum(x, dtype=float)
#     csum[n:] = csum[n:] - csum[:-n]
#     result = csum[n - 1:] / n
#     return np_prepend(result, n - 1)


def sma(close, length=None, talib=None, offset=None, **kwargs):
    """Simple Moving Average (SMA)

    The Simple Moving Average is the classic moving average that is the equally
    weighted average over n periods.

    Sources:
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/simple-moving-average-sma/

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
    # Validate Arguments
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs["min_periods"]) if "min_periods" in kwargs and kwargs["min_periods"] is not None else length
    close = verify_series(close, max(length, min_periods))
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if close is None: return

    # Calculate Result
    if Imports["talib"] and mode_tal:
        from talib import SMA
        sma = SMA(close, length)
    else:
        np_close = close.values
        sma = np_sma(np_close, length)
        sma = pd.Series(sma, index=close.index)

    # Offset
    if offset != 0:
        sma = sma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        sma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        sma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    sma.name = f"SMA_{length}"
    sma.category = "overlap"

    return sma
