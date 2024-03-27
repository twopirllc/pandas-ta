# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.momentum import roc
from pandas_ta.utils import signed_series, v_offset, v_pos_default, v_series



def nvi(
    close: Series, volume: Series, length: Int = None, initial: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Negative Volume Index (NVI)

    The Negative Volume Index is a cumulative indicator that uses volume
    change in an attempt to identify where smart money is active. Used in
    conjunction with PVI.

    Sources:
        https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:negative_volume_inde
        https://www.motivewave.com/studies/negative_volume_index.htm

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        length (int): The short period. Default: 13
        initial (int): The short period. Default: 1000
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 1)
    close = v_series(close, length + 1)
    volume = v_series(volume, length + 1)

    if close is None or volume is None:
        return

    initial = v_pos_default(initial, 1000)
    offset = v_offset(offset)

    # Calculate
    roc_ = roc(close=close, length=length)
    signed_volume = signed_series(volume, 1)
    nvi = signed_volume[signed_volume < 0].abs() * roc_
    nvi.fillna(0, inplace=True)
    nvi.iloc[0] = initial
    nvi = nvi.cumsum()

    # Offset
    if offset != 0:
        nvi = nvi.shift(offset)

    # Fill
    if "fillna" in kwargs:
        nvi.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    nvi.name = f"NVI_{length}"
    nvi.category = "volume"

    return nvi
