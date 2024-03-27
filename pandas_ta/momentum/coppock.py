# -*- coding: utf-8 -*-
# from numpy import isnan
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.overlap import wma
from pandas_ta.utils import v_offset, v_pos_default, v_series
from .roc import roc



def coppock(
    close: Series, length: Int = None, fast: Int = None, slow: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Coppock Curve (COPC)

    Coppock Curve (originally called the "Trendex Model") is a momentum
    indicator is designed for use on a monthly time scale. Although designed
    for monthly use, a daily calculation over the same period can be made,
    converting the periods to 294-day and 231-day rate of changes,
    and a 210-day WMA.

    Sources:
        https://en.wikipedia.org/wiki/Coppock_curve

    Args:
        close (pd.Series): Series of 'close's
        length (int): WMA period. Default: 10
        fast (int): Fast ROC period. Default: 11
        slow (int): Slow ROC period. Default: 14
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 10)
    fast = v_pos_default(fast, 11)
    slow = v_pos_default(slow, 14)
    _length = length + fast + slow
    close = v_series(close, _length)

    if close is None:
        return

    offset = v_offset(offset)

    # Calculate
    total_roc = roc(close, fast) + roc(close, slow)
    coppock = wma(total_roc, length)

    # Offset
    if offset != 0:
        coppock = coppock.shift(offset)

    # Fill
    if "fillna" in kwargs:
        coppock.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    coppock.name = f"COPC_{fast}_{slow}_{length}"
    coppock.category = "momentum"

    return coppock
