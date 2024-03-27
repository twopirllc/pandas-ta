# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.maps import Imports
from pandas_ta.overlap import ema
from pandas_ta.utils import v_offset, v_pos_default, v_series, v_talib
from pandas_ta.volume import ad



def adosc(
    high: Series, low: Series, close: Series, volume: Series,
    open_: Series = None, fast: Int = None, slow: Int = None,
    talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Accumulation/Distribution Oscillator or Chaikin Oscillator

    Accumulation/Distribution Oscillator indicator utilizes
    Accumulation/Distribution and treats it similarly to MACD
    or APO.

    Sources:
        https://www.investopedia.com/articles/active-trading/031914/understanding-chaikin-oscillator.asp

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        open_ (pd.Series): Series of 'open's
        volume (pd.Series): Series of 'volume's
        fast (int): The short period. Default: 12
        slow (int): The long period. Default: 26
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    fast = v_pos_default(fast, 3)
    slow = v_pos_default(slow, 10)
    _length = max(fast, slow)
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)
    volume = v_series(volume, _length)

    if high is None or low is None or close is None or volume is None:
        return

    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import ADOSC
        adosc = ADOSC(high, low, close, volume, fast, slow)
    else:
        # remove length so it doesn't override ema length
        if "length" in kwargs:
            kwargs.pop("length")

        ad_ = ad(
            high=high, low=low, close=close, volume=volume,
            open_=open_, talib=mode_tal
        )
        fast_ad = ema(close=ad_, length=fast, **kwargs, talib=mode_tal)
        slow_ad = ema(close=ad_, length=slow, **kwargs, talib=mode_tal)
        adosc = fast_ad - slow_ad

    # Offset
    if offset != 0:
        adosc = adosc.shift(offset)

    # Fill
    if "fillna" in kwargs:
        adosc.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    adosc.name = f"ADOSC_{fast}_{slow}"
    adosc.category = "volume"

    return adosc
