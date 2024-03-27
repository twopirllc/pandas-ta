# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.utils import (
    non_zero_range,
    v_mamode,
    v_offset,
    v_pos_default,
    v_series
)



def qstick(
    open_: Series, close: Series, length: Int = None, mamode: str = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Q Stick

    The Q Stick indicator, developed by Tushar Chande, attempts to quantify
    and identify trends in candlestick charts.

    Sources:
        https://library.tradingtechnologies.com/trade/chrt-ti-qstick.html

    Args:
        open (pd.Series): Series of 'open's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 1
        mamode (str): See ``help(ta.ma)``. Default: "sma"
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 10)
    open_ = v_series(open_, length)
    close = v_series(close, length)

    if open_ is None or close is None:
        return

    mamode = v_mamode(mamode, "sma")
    offset = v_offset(offset)

    # Calculate
    diff = non_zero_range(close, open_)
    qstick = ma(mamode, diff, length=length, **kwargs)

    # Offset
    if offset != 0:
        qstick = qstick.shift(offset)

    # Fill
    if "fillna" in kwargs:
        qstick.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    qstick.name = f"QS_{length}"
    qstick.category = "trend"

    return qstick
