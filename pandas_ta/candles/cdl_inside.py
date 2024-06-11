# -*- coding: utf-8 -*-
from numpy import roll, where
from numba import njit
from pandas import Series
from pandas_ta._typing import Array, DictLike, Int, IntFloat
from pandas_ta.utils import v_bool, v_offset, v_offset, v_scalar, v_series



@njit(cache=True)
def np_cdl_inside(high, low):
    hdiff = where(high - roll(high, 1) < 0, 1, 0)
    ldiff = where(low - roll(low, 1) > 0, 1, 0)
    return hdiff & ldiff


def cdl_inside(
    open_: Series, high: Series, low: Series, close: Series,
    asbool: bool = None, scalar: IntFloat = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Candle Type: Inside Bar

    An Inside Bar is a bar that is engulfed by the prior highs and lows of
    it's previous bar. In other words, the current bar is smaller than it's
    previous bar.

    Set asbool=True if you want to know if it is an Inside Bar. Note by
    default asbool=False so this returns a 0 if it is not an Inside Bar, 1 if
    it is an Inside Bar and close > open, and -1 if it is an Inside Bar
    but close < open.

    Sources:
        https://www.tradingview.com/script/IyIGN1WO-Inside-Bar/

    Args:
        open_ (pd.Series): Series of 'open's
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        asbool (bool): Returns the boolean result. Default: False
        scalar (float): How much to magnify. Default: 100
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature
    """
    # Validate
    open_ = v_series(open_)
    high = v_series(high)
    low = v_series(low)
    close = v_series(close)

    if open_ is None or high is None or low is None or close is None:
        return

    asbool = v_bool(asbool, False)
    scalar = v_scalar(scalar, 100)
    offset = v_offset(offset)

    # Calculate
    np_high, np_low = high.to_numpy(), low.to_numpy()
    np_inside = np_cdl_inside(np_high, np_low)
    inside = Series(np_inside, index=close.index, dtype=bool)

    if not asbool:
        inside = scalar * inside.astype(int)

    # Offset
    if offset != 0:
        inside = inside.shift(offset)

    # Fill
    if "fillna" in kwargs:
        inside.fillna(kwargs["fillna"], inplace=True)
    # Name and Category
    inside.name = f"CDL_INSIDE"
    inside.category = "candles"

    return inside
