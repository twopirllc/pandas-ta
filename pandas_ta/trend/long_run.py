# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_pos_default, v_series
from .decreasing import decreasing
from .increasing import increasing



def long_run(
    fast: Series, slow: Series, length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Long Run

    Long Run was developed by Kevin Johnson that returns a binary Series
    where '1' is a trend and '0' is not a trend given 'fast' and 'slow' signal
    over a certain period length.

    It is recommended to use 'smooth' signals for 'fast' and 'slow' for the
    comparison to reduce unnecessary noise. For indicators using long_run, see
    Archer Moving Average Trend (```help(ta.amat)```) and Archer On Balance
    Volume (```help(ta.aobv)```). Both use Moving Averages for 'fast' and 'slow'
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
    # potential bottom or bottom
    pb = increasing(fast, length) & decreasing(slow, length)
    # fast and slow are increasing
    bi = increasing(fast, length) & increasing(slow, length)
    long_run = pb | bi

    # Offset
    if offset != 0:
        long_run = long_run.shift(offset)

    # Fill
    if "fillna" in kwargs:
        long_run.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    long_run.name = f"LR_{length}"
    long_run.category = "trend"

    return long_run
