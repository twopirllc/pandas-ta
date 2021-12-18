# -*- coding: utf-8 -*-
from .decreasing import decreasing
from .increasing import increasing
from pandas_ta.utils import get_offset, verify_series


def long_run(fast, slow, length=None, offset=None, **kwargs):
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
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate Arguments
    length = int(length) if length and length > 0 else 2
    fast = verify_series(fast, length)
    slow = verify_series(slow, length)
    offset = get_offset(offset)

    if fast is None or slow is None: return

    # Calculate Result
    pb = increasing(fast, length) & decreasing(slow, length)  # potential bottom or bottom
    bi = increasing(fast, length) & increasing(slow, length)  # fast and slow are increasing
    long_run = pb | bi

    # Offset
    if offset != 0:
        long_run = long_run.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        long_run.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        long_run.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    long_run.name = f"LR_{length}"
    long_run.category = "trend"

    return long_run
