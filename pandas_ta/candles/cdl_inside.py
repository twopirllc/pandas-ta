# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import candle_color, v_offset, v_series


def cdl_inside(
    open_: Series, high: Series, low: Series, close: Series,
    asbool: bool = False,
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
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature
    """
    # Validate
    open_ = v_series(open_)
    high = v_series(high)
    low = v_series(low)
    close = v_series(close)
    offset = v_offset(offset)

    # Calculate
    inside = (high.diff() < 0) & (low.diff() > 0)

    if not asbool:
        inside *= candle_color(open_, close)

    # Offset
    if offset != 0:
        inside = inside.shift(offset)

    # Fill
    if "fillna" in kwargs:
        inside.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        inside.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    inside.name = f"CDL_INSIDE"
    inside.category = "candles"

    return inside
