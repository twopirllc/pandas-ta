# -*- coding: utf-8 -*-
from numpy import copy, cos, exp
from pandas import Series
from pandas_ta._typing import Array, DictLike, Int, IntFloat
from pandas_ta.utils import v_bool, v_offset, v_pos_default, v_series


try:
    from numba import njit
except ImportError:
    def njit(_): return _


@njit
def np_ssf(x: Array, n: Int, pi: IntFloat, sqrt2: IntFloat):
    """Ehler's Super Smoother Filter
    http://traders.com/documentation/feedbk_docs/2014/01/traderstips.html
    """
    m, ratio, result = x.size, sqrt2 / n, copy(x)
    a = exp(-pi * ratio)
    b = 2 * a * cos(180 * ratio)
    c = a * a - b + 1

    for i in range(2, m):
        result[i] = 0.5 * c * (x[i] + x[i - 1]) + b * result[i - 1] \
            - a * a * result[i - 2]

    return result


@njit
def np_ssf_everget(x: Array, n: Int, pi: IntFloat, sqrt2: IntFloat):
    """John F. Ehler's Super Smoother Filter by Everget (2 poles), Tradingview
    https://www.tradingview.com/script/VdJy0yBJ-Ehlers-Super-Smoother-Filter/
    """
    m, arg, result = x.size, pi * sqrt2 / n, copy(x)
    a = exp(-arg)
    b = 2 * a * cos(arg)

    for i in range(2, m):
        result[i] = 0.5 * (a * a - b + 1) * (x[i] + x[i - 1]) \
            + b * result[i - 1] - a * a * result[i - 2]

    return result


def ssf(
    close: Series, length: Int = None,
    everget: bool = None, pi: IntFloat = None, sqrt2: IntFloat = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Ehler's Super Smoother Filter (SSF) © 2013

    John F. Ehlers's solution to reduce lag and remove aliasing noise with
    his research in Aerospace analog filter design. This implementation had
    two poles. Since SSF is a (Resursive) Digital Filter, the number of
    poles determine how many prior recursive SSF bars to include in the
    filter design.

    For Everget's calculation on TradingView, set arguments:
        pi = np.pi, sqrt2 = np.sqrt(2)

    Sources:
        http://traders.com/documentation/feedbk_docs/2014/01/traderstips.html
        https://www.tradingview.com/script/VdJy0yBJ-Ehlers-Super-Smoother-Filter/
        https://www.mql5.com/en/code/588

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 20
        everget (bool): Everget's implementation of ssf that uses pi
            instead of 180 for the b factor of ssf. Default: False
        pi (float): The value of PI to use. The default is Ehler's
            truncated value 3.14159. Adjust the value for more precision.
            Default: 3.14159
        sqrt2 (float): The value of sqrt(2) to use. The default is Ehler's
            truncated value 1.414. Adjust the value for more precision.
            Default: 1.414
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 20)
    close = v_series(close, length)

    if close is None:
        return

    pi = v_pos_default(pi, 3.14159)
    sqrt2 = v_pos_default(sqrt2, 1.414)
    everget = v_bool(everget, False)
    offset = v_offset(offset)

    # Calculate
    np_close = close.values
    if everget:
        ssf = np_ssf_everget(np_close, length, pi, sqrt2)
    else:
        ssf = np_ssf(np_close, length, pi, sqrt2)
    ssf = Series(ssf, index=close.index)

    # Offset
    if offset != 0:
        ssf = ssf.shift(offset)

    # Fill
    if "fillna" in kwargs:
        ssf.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ssf.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    ssf.name = f"SSF{'e' if everget else ''}_{length}"
    ssf.category = "overlap"

    return ssf
