# -*- coding: utf-8 -*-
from numpy import sqrt
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.overlap import sma
from pandas_ta.utils import v_offset, v_pos_default, v_series



def ui(
    close: Series, length: Int = None, scalar: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Ulcer Index (UI)

    The Ulcer Index by Peter Martin measures the downside volatility with
    the use of the Quadratic Mean, which has the effect of emphasising
    large drawdowns.

    Sources:
        https://library.tradingtechnologies.com/trade/chrt-ti-ulcer-index.html
        https://en.wikipedia.org/wiki/Ulcer_index
        http://www.tangotools.com/ui/ui.htm

    Args:
        high (pd.Series): Series of 'high's
        close (pd.Series): Series of 'close's
        length (int): The short period.  Default: 14
        scalar (float): A positive float to scale the bands. Default: 100
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        everget (value, optional): TradingView's Evergets SMA instead of SUM
            calculation. Default: False
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature
    """
    # Validate
    length = v_pos_default(length, 14)
    scalar = v_pos_default(scalar, 100)
    close = v_series(close, 2 * length - 1)

    if close is None:
        return

    offset = v_offset(offset)

    # Calculate
    highest_close = close.rolling(length).max()
    downside = scalar * (close - highest_close) / highest_close
    d2 = downside * downside

    everget = kwargs.pop("everget", False)
    if everget:
        # Everget uses SMA instead of SUM for calculation
        _ui = sma(d2, length)
    else:
        _ui = d2.rolling(length).sum()
    ui = sqrt(_ui / length)

    # Offset
    if offset != 0:
        ui = ui.shift(offset)

    # Fill
    if "fillna" in kwargs:
        ui.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    ui.name = f"UI{'' if not everget else 'e'}_{length}"
    ui.category = "volatility"

    return ui
