# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.momentum import roc
from pandas_ta.utils import signed_series, v_offset, v_pos_default, v_series


def pvi(
    close: Series, volume: Series, length: Int = None, initial: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Positive Volume Index (PVI)

    The Positive Volume Index is a cumulative indicator that uses volume
    change in an attempt to identify where smart money is active. Used in
    conjunction with NVI.

    Sources:
        https://www.investopedia.com/terms/p/pvi.asp

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        length (int): The short period. Default: 13
        initial (int): The short period. Default: 1000
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 1)
    close = v_series(close, length)
    volume = v_series(volume, length)

    if close is None or volume is None:
        return

    initial = v_pos_default(initial, 1000)
    offset = v_offset(offset)

    # Calculate
    signed_volume = signed_series(volume, 1)
    _roc = roc(close=close, length=length)
    pvi = _roc * signed_volume[signed_volume > 0].abs()
    pvi.fillna(0, inplace=True)
    pvi.iloc[0] = initial
    pvi = pvi.cumsum()

    # Offset
    if offset != 0:
        pvi = pvi.shift(offset)

    # Fill
    if "fillna" in kwargs:
        pvi.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        pvi.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    pvi.name = f"PVI_{length}"
    pvi.category = "volume"

    return pvi
