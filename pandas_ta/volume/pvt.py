# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.momentum import roc
from pandas_ta.utils import v_drift, v_offset, v_series



def pvt(
    close: Series, volume: Series, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Price-Volume Trend (PVT)

    The Price-Volume Trend utilizes the Rate of Change with volume to
    and it's cumulative values to determine money flow.

    Sources:
        https://www.tradingview.com/wiki/Price_Volume_Trend_(PVT)

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        drift (int): The diff period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    drift = v_drift(drift)
    _drift = drift + 1
    close = v_series(close, _drift)
    volume = v_series(volume, _drift)

    if close is None or volume is None:
        return

    offset = v_offset(offset)

    # Calculate
    pv = roc(close=close, length=drift) * volume
    pvt = pv.cumsum()

    # Offset
    if offset != 0:
        pvt = pvt.shift(offset)

    # Fill
    if "fillna" in kwargs:
        pvt.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    pvt.name = f"PVT"
    pvt.category = "volume"

    return pvt
