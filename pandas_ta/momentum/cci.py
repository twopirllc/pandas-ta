# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.maps import Imports
from pandas_ta.overlap import hlc3, sma
from pandas_ta.statistics import mad
from pandas_ta.utils import v_offset, v_pos_default, v_series, v_talib



def cci(
    high: Series, low: Series, close: Series, length: Int = None,
    c: IntFloat = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Commodity Channel Index (CCI)

    Commodity Channel Index is a momentum oscillator used to primarily
    identify overbought and oversold levels relative to a mean.

    Sources:
        https://www.tradingview.com/wiki/Commodity_Channel_Index_(CCI)

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        c (float): Scaling Constant. Default: 0.015
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 14)
    high = v_series(high, length)
    low = v_series(low, length)
    close = v_series(close, length)

    if high is None or low is None or close is None:
        return

    c = v_pos_default(c, 0.015)
    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import CCI
        cci = CCI(high, low, close, length)
    else:
        typical_price = hlc3(high=high, low=low, close=close, talib=mode_tal)
        mean_typical_price = sma(typical_price, length=length, talib=mode_tal)
        mad_typical_price = mad(typical_price, length=length)

        cci = typical_price - mean_typical_price / (c * mad_typical_price)

    # Offset
    if offset != 0:
        cci = cci.shift(offset)

    # Fill
    if "fillna" in kwargs:
        cci.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    cci.name = f"CCI_{length}_{c}"
    cci.category = "momentum"

    return cci
