# -*- coding: utf-8 -*-
from numpy import zeros_like
from numba import njit
from pandas import Series
from pandas_ta._typing import Array, DictLike, Int
from pandas_ta.utils import v_offset, v_pos_default, v_series, v_str



# Exponential Decay - https://tulipindicators.org/edecay
@njit(cache=True)
def nb_exponential_decay(x, n):
    m, rate = x.size, 1.0 - (1.0 / n)

    result = zeros_like(x, dtype="float")
    result[0] = x[0]

    for i in range(1, m):
        result[i] = max(0, x[i], result[i - 1] * rate)

    return result


# Linear Decay -https://tulipindicators.org/decay
@njit(cache=True)
def nb_linear_decay(x, n):
    m, rate = x.size, 1.0 / n

    result = zeros_like(x, dtype="float")
    result[0] = x[0]

    for i in range(1, m):
        result[i] = max(0, x[i], result[i - 1] - rate)

    return result


def decay(
    close: Series, length: Int = None, mode: str = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Decay

    Creates a decay moving forward from prior signals like crosses.
    The default is "linear".
    Exponential is optional as "exponential" or "exp".

    Sources:
        https://tulipindicators.org/decay

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 1
        mode (str): If 'exp' then "exponential" decay. Default: 'linear'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    close = v_series(close, length)

    if close is None:
        return

    length = v_pos_default(length, 1)
    mode = v_str(mode, "linear")
    offset = v_offset(offset)

    # Calculate
    _mode, np_close = "L", close.to_numpy()

    if mode in ["exp", "exponential"]:
        _mode = "EXP"
        result = nb_exponential_decay(np_close, length)
    else:  # "linear"
        result = nb_linear_decay(np_close, length)

    result = Series(result, index=close.index)

    # Offset
    if offset != 0:
        result = result.shift(offset)

    # Fill
    if "fillna" in kwargs:
        result.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    result.name = f"{_mode}DECAY_{length}"
    result.category = "trend"

    return result
