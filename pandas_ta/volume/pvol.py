# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import signed_series, v_bool, v_offset, v_series



def pvol(
    close: Series, volume: Series, signed: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Price-Volume (PVOL)

    Returns a series of the product of price and volume.

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        signed (bool): Keeps the sign of the difference in 'close's.
            Default: False
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    close = v_series(close)
    volume = v_series(volume)
    signed = v_bool(signed, False)
    offset = v_offset(offset)

    # Calculate
    pvol = close * volume
    if signed:
        pvol *= signed_series(close, 1)

    # Offset
    if offset != 0:
        pvol = pvol.shift(offset)

    # Fill
    if "fillna" in kwargs:
        pvol.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    pvol.name = f"PVOL"
    pvol.category = "volume"

    return pvol
