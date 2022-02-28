# -*- coding: utf-8 -*-
from numpy import fabs
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import non_zero_range, v_drift, v_offset
from pandas_ta.utils import v_pos_default, v_series


def vhf(
    close: Series, length: Int = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Vertical Horizontal Filter (VHF)

    VHF was created by Adam White to identify trending and ranging markets.

    Sources:
        https://www.incrediblecharts.com/indicators/vertical_horizontal_filter.php

    Args:
        source (pd.Series): Series of prices (usually close).
        length (int): The period length. Default: 28
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 28)
    close = v_series(close, length)

    if close is None:
        return

    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    hcp = close.rolling(length).max()
    lcp = close.rolling(length).min()
    diff = fabs(close.diff(drift))
    vhf = fabs(non_zero_range(hcp, lcp)) / diff.rolling(length).sum()

    # Offset
    if offset != 0:
        vhf = vhf.shift(offset)

    # Fill
    if "fillna" in kwargs:
        vhf.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        vhf.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    vhf.name = f"VHF_{length}"
    vhf.category = "trend"

    return vhf
