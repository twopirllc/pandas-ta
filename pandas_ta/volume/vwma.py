# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.overlap import sma
from pandas_ta.utils import v_offset, v_pos_default, v_series



def vwma(
    close: Series, volume: Series, length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Volume Weighted Moving Average (VWMA)

    Volume Weighted Moving Average.

    Sources:
        https://www.motivewave.com/studies/volume_weighted_moving_average.htm

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        length (int): It's period. Default: 10
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 10)
    close = v_series(close, length)
    volume = v_series(volume, length)

    if close is None or volume is None:
        return

    offset = v_offset(offset)

    # Calculate
    pv = close * volume
    vwma = sma(close=pv, length=length) / sma(close=volume, length=length)

    # Offset
    if offset != 0:
        vwma = vwma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        vwma.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    vwma.name = f"VWMA_{length}"
    vwma.category = "overlap"

    return vwma
