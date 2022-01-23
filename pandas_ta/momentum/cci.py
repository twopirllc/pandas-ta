# -*- coding: utf-8 -*-
from pandas_ta import Imports
from pandas_ta.overlap import hlc3, sma
from pandas_ta.statistics.mad import mad
from pandas_ta.utils import get_offset, verify_series
from pandas import Series


def cci(high: Series, low: Series, close: Series, length: int = None, c: float = None,
        talib: bool = None, offset: int = None, **kwargs) -> Series:
    """Commodity Channel Index (CCI)

    Commodity Channel Index is a momentum oscillator used to primarily identify
    overbought and oversold levels relative to a mean.

    Sources:
        https://www.tradingview.com/wiki/Commodity_Channel_Index_(CCI)

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        c (float): Scaling Constant. Default: 0.015
        talib (bool): If TA Lib is installed and talib is True, Returns the TA Lib
            version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate Arguments
    length = int(length) if length and length > 0 else 14
    c = float(c) if c and c > 0 else 0.015
    high = verify_series(high, length)
    low = verify_series(low, length)
    close = verify_series(close, length)
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if high is None or low is None or close is None: return

    # Calculate Result
    if Imports["talib"] and mode_tal:
        from talib import CCI
        cci = CCI(high, low, close, length)
    else:
        typical_price = hlc3(high=high, low=low, close=close, talib=mode_tal)
        mean_typical_price = sma(typical_price, length=length, talib=mode_tal)
        mad_typical_price = mad(typical_price, length=length)

        cci = typical_price - mean_typical_price
        cci /= c * mad_typical_price

    # Offset
    if offset != 0:
        cci = cci.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        cci.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        cci.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    cci.name = f"CCI_{length}_{c}"
    cci.category = "momentum"

    return cci
