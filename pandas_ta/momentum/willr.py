# -*- coding: utf-8 -*-
from pandas_ta import Imports
from pandas_ta.utils import get_offset, verify_series
from pandas import Series


def willr(high: Series, low: Series, close: Series, length: int = None, talib: bool = None, offset: int = None,
          **kwargs) -> Series:
    """William's Percent R (WILLR)

    William's Percent R is a momentum oscillator similar to the RSI that
    attempts to identify overbought and oversold conditions.

    Sources:
        https://www.tradingview.com/wiki/Williams_%25R_(%25R)

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        talib (bool): If TA Lib is installed and talib is True, Returns the TA Lib
            version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate arguments
    length = int(length) if length and length > 0 else 14
    min_periods = int(kwargs["min_periods"]) if "min_periods" in kwargs and kwargs["min_periods"] is not None else length
    _length = max(length, min_periods)
    high = verify_series(high, _length)
    low = verify_series(low, _length)
    close = verify_series(close, _length)
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if high is None or low is None or close is None: return

    # Calculate Result
    if Imports["talib"] and mode_tal:
        from talib import WILLR
        willr = WILLR(high, low, close, length)
    else:
        lowest_low = low.rolling(length, min_periods=min_periods).min()
        highest_high = high.rolling(length, min_periods=min_periods).max()

        willr = 100 * ((close - lowest_low) / (highest_high - lowest_low) - 1)

    # Offset
    if offset != 0:
        willr = willr.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        willr.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        willr.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    willr.name = f"WILLR_{length}"
    willr.category = "momentum"

    return willr
