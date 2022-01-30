# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.utils import get_offset, signed_series, verify_series


def pvol(
    close: Series, volume: Series,
    offset: int = None, **kwargs
) -> Series:
    """Price-Volume (PVOL)

    Returns a series of the product of price and volume.

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        signed (bool): Keeps the sign of the difference in 'close's. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    close = verify_series(close)
    volume = verify_series(volume)
    offset = get_offset(offset)
    signed = kwargs.pop("signed", False)

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
    if "fill_method" in kwargs:
        pvol.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    pvol.name = f"PVOL"
    pvol.category = "volume"

    return pvol
