# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.momentum import roc
from pandas_ta.utils import get_drift, get_offset, verify_series


def pvt(
        close: Series, volume: Series, drift: int = None,
        offset: int = None, **kwargs
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
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    close = verify_series(close)
    volume = verify_series(volume)
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate
    pv = roc(close=close, length=drift) * volume
    pvt = pv.cumsum()

    # Offset
    if offset != 0:
        pvt = pvt.shift(offset)

    # Fill
    if "fillna" in kwargs:
        pvt.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        pvt.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    pvt.name = f"PVT"
    pvt.category = "volume"

    return pvt
