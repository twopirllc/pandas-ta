# -*- coding: utf-8 -*-
from numpy import sign
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import (
    nb_idiff,
    v_drift,
    v_offset,
    v_pos_default,
    v_scalar,
    v_series
)



def psl(
    close: Series, open_: Series = None,
    length: Int = None, scalar: IntFloat = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Psychological Line (PSL)

    The Psychological Line is an oscillator-type indicator that compares the
    number of the rising periods to the total number of periods. In other
    words, it is the percentage of bars that close above the previous
    bar over a given period.

    Sources:
        https://www.quantshare.com/item-851-psychological-line

    Args:
        close (pd.Series): Series of 'close's
        open_ (pd.Series, optional): Series of 'open's
        length (int): It's period. Default: 12
        scalar (float): How much to magnify. Default: 100
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 12)
    close = v_series(close, length)

    if close is None:
        return

    scalar = v_scalar(scalar, 100)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    if open_ is not None:
        open_ = v_series(open_)
        diff = sign(close - open_)
    else:
        diff = sign(close.diff(drift))

    diff.fillna(0, inplace=True)
    diff[diff <= 0] = 0  # Set negative values to zero

    psl = scalar * diff.rolling(length).sum() / length

    # Offset
    if offset != 0:
        psl = psl.shift(offset)

    # Fill
    if "fillna" in kwargs:
        psl.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"_{length}"
    psl.name = f"PSL{_props}"
    psl.category = "momentum"

    return psl
