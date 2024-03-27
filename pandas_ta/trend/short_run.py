# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_pos_default, v_series
from .decreasing import decreasing
from .increasing import increasing



def short_run(
    fast: Series, slow: Series, length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Short Run

    Short Run was developed by Kevin Johnson that returns a binary Series
    where '1' is a trend and '0' is not a trend given 'fast' and 'slow' signal
    over a certain period length.

    It is recommended to use 'smooth' signals for 'fast' and 'slow' for the
    comparison to reduce unnecessary noise. For indicators using long_run, see
    Archer Moving Average Trend (``help(ta.amat)``) and Archer On Balance
    Volume (``help(ta.aobv)``). Both use Moving Averages for 'fast' and 'slow'
    signals.

    Sources:
        It is part of the Converging and Diverging Conditional logic in:
        https://www.tradingview.com/script/Z2mq63fE-Trade-Archer-Moving-Averages-v1-4F/

    Args:
        fast (pd.Series): Series of 'fast' values.
        slow (pd.Series): Series of 'slow' values.
        length (int): The period length. Default: 2
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 2)
    fast = v_series(fast, length)
    slow = v_series(slow, length)

    if fast is None or slow is None:
        return

    offset = v_offset(offset)

    # Calculate
    # potential top or top
    pt = decreasing(fast, length) & increasing(slow, length)
    # fast and slow are decreasing
    bd = decreasing(fast, length) & decreasing(slow, length)
    short_run = pt | bd

    # Offset
    if offset != 0:
        short_run = short_run.shift(offset)

    # Fill
    if "fillna" in kwargs:
        short_run.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    short_run.name = f"SR_{length}"
    short_run.category = "trend"

    return short_run
