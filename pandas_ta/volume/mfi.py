# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.overlap import hlc3
from pandas_ta.utils import v_drift, v_offset, v_pos_default, v_series, v_talib


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
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 14)
    high = v_series(high, length)
    low = v_series(low, length)
    close = v_series(close, length)
    volume = v_series(volume, length)

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
        typical_price = hlc3(high=high, low=low, close=close, talib=mode_tal)
        raw_money_flow = typical_price * volume

        tdf = DataFrame(
            {"diff": 0, "rmf": raw_money_flow, "+mf": 0, "-mf": 0}
        )

        tdf.loc[(typical_price.diff(drift) > 0), "diff"] = 1
        tdf.loc[tdf["diff"] == 1, "+mf"] = raw_money_flow

        tdf.loc[(typical_price.diff(drift) < 0), "diff"] = -1
        tdf.loc[tdf["diff"] == -1, "-mf"] = raw_money_flow

        psum = tdf["+mf"].rolling(length).sum()
        nsum = tdf["-mf"].rolling(length).sum()
        tdf["mr"] = psum / nsum
        mfi = 100 * psum / (psum + nsum)
        tdf["mfi"] = mfi

    # Offset
    if offset != 0:
        mfi = mfi.shift(offset)

    # Fill
    if "fillna" in kwargs:
        mfi.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        mfi.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    mfi.name = f"MFI_{length}"
    mfi.category = "volume"

    return mfi
