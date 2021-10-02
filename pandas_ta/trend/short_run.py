# -*- coding: utf-8 -*-
from .decreasing import decreasing
from .increasing import increasing
from pandas_ta.utils import get_offset, verify_series


def short_run(fast, slow, length=None, offset=None, **kwargs):
    """Short Run

    Short Run was developed by Kevin Johnson that returns a binary Series
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

    Calculation:
        Default Inputs:
            length=2
        INC = increasing
        DEC = decreasing
        BDEC = Both decreasing
        PTOP = Potential Top

        BDEC = DEC(fast, length) & DEC(slow, length)
        PTOP = DEC(fast, length) & INC(slow, length)
        SR = BDEC | PTOP

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
    pt = decreasing(fast, length) & increasing(slow, length)  # potential top or top
    bd = decreasing(fast, length) & decreasing(slow, length)  # fast and slow are decreasing
    short_run = pt | bd

    # Offset
    if offset != 0:
        short_run = short_run.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        short_run.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        short_run.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    short_run.name = f"SR_{length}"
    short_run.category = "trend"

    return short_run
