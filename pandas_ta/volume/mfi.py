# -*- coding: utf-8 -*-
from sys import float_info as sflt
from numpy import convolve, maximum, nan, ones, roll, where
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.overlap import hlc3
from pandas_ta.utils import (
    nb_non_zero_range,
    v_drift,
    v_offset,
    v_pos_default,
    v_series,
    v_talib
)



def mfi(
    high: Series, low: Series, close: Series, volume: Series,
    length: Int = None, talib: bool = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Money Flow Index (MFI)

    Money Flow Index is an oscillator indicator that is used to measure
    buying and selling pressure by utilizing both price and volume.

    Sources:
        https://www.tradingview.com/wiki/Money_Flow_(MFI)

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        length (int): The sum period. Default: 14
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 14)
    _length = length + 1
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)
    volume = v_series(volume, _length)

    if high is None or low is None or close is None or volume is None:
        return

    mode_tal = v_talib(talib)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import MFI
        mfi = MFI(high, low, close, volume, length)
    else:
        m, _ones = close.size, ones(length)

        tp = (high.to_numpy() + low.to_numpy() + close.to_numpy()) / 3.0
        smf = tp * volume.to_numpy() * where(tp > roll(tp, shift=drift), 1, -1)

        pos, neg = maximum(smf, 0), maximum(-smf, 0)
        avg_gain, avg_loss = convolve(pos, _ones)[:m], convolve(neg, _ones)[:m]

        _mfi = (100.0 * avg_gain) / (avg_gain + avg_loss + sflt.epsilon)
        _mfi[:length] = nan

        mfi = Series(_mfi, index=close.index)

    # Offset
    if offset != 0:
        mfi = mfi.shift(offset)

    # Fill
    if "fillna" in kwargs:
        mfi.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    mfi.name = f"MFI_{length}"
    mfi.category = "volume"

    return mfi
