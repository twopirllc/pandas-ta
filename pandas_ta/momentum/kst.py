# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_drift, v_offset, v_pos_default, v_series
from .roc import roc



def kst(
    close: Series, signal: Int = None,
    roc1: Int = None, roc2: Int = None, roc3: Int = None, roc4: Int = None,
    sma1: Int = None, sma2: Int = None, sma3: Int = None, sma4: Int = None,
    drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """'Know Sure Thing' (KST)

    The 'Know Sure Thing' is a momentum based oscillator and based on ROC.

    Sources:
        https://www.tradingview.com/wiki/Know_Sure_Thing_(KST)
        https://www.incrediblecharts.com/indicators/kst.php

    Args:
        close (pd.Series): Series of 'close's
        roc1 (int): ROC 1 period. Default: 10
        roc2 (int): ROC 2 period. Default: 15
        roc3 (int): ROC 3 period. Default: 20
        roc4 (int): ROC 4 period. Default: 30
        sma1 (int): SMA 1 period. Default: 10
        sma2 (int): SMA 2 period. Default: 10
        sma3 (int): SMA 3 period. Default: 10
        sma4 (int): SMA 4 period. Default: 15
        signal (int): It's period. Default: 9
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: kst and kst_signal columns
    """
    # Validate
    roc1 = int(roc1) if roc1 and roc1 > 0 else 10
    roc2 = int(roc2) if roc2 and roc2 > 0 else 15
    roc3 = int(roc3) if roc3 and roc3 > 0 else 20
    roc4 = int(roc4) if roc4 and roc4 > 0 else 30

    sma1 = int(sma1) if sma1 and sma1 > 0 else 10
    sma2 = int(sma2) if sma2 and sma2 > 0 else 10
    sma3 = int(sma3) if sma3 and sma3 > 0 else 10
    sma4 = int(sma4) if sma4 and sma4 > 0 else 15

    signal = v_pos_default(signal, 9)
    _rmax = max(roc1, roc2, roc3, roc4)
    _smax = max(sma1, sma2, sma3, sma4)
    _length = _rmax + _smax
    close = v_series(close, _length)

    if close is None:
        return

    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    rocma1 = roc(close, roc1).rolling(sma1).mean()
    rocma2 = roc(close, roc2).rolling(sma2).mean()
    rocma3 = roc(close, roc3).rolling(sma3).mean()
    rocma4 = roc(close, roc4).rolling(sma4).mean()

    kst = 100 * (rocma1 + 2 * rocma2 + 3 * rocma3 + 4 * rocma4)
    kst_signal = kst.rolling(signal).mean()

    # Offset
    if offset != 0:
        kst = kst.shift(offset)
        kst_signal = kst_signal.shift(offset)

    # Fill
    if "fillna" in kwargs:
        kst.fillna(kwargs["fillna"], inplace=True)
        kst_signal.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    kst.name = f"KST_{roc1}_{roc2}_{roc3}_{roc4}_{sma1}_{sma2}_{sma3}_{sma4}"
    kst_signal.name = f"KSTs_{signal}"
    kst.category = kst_signal.category = "momentum"

    data = {kst.name: kst, kst_signal.name: kst_signal}
    df = DataFrame(data, index=close.index)
    df.name = f"KST_{roc1}_{roc2}_{roc3}_{roc4}_{sma1}_{sma2}_{sma3}_{sma4}_{signal}"
    df.category = "momentum"

    return df
