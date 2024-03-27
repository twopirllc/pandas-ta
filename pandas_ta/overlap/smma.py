# -*- coding: utf-8 -*-
from numpy import nan
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.utils import (
    v_mamode,
    v_offset,
    v_pos_default,
    v_series,
    v_talib
)



def smma(
    close: Series, length: Int = None,
    mamode: str = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """SMoothed Moving Average (SMMA)

    The SMoothed Moving Average (SMMA) is bootstrapped by default with a
    Simple Moving Average (SMA). It tries to reduce noise rather than reduce
    lag. The SMMA takes all prices into account and uses a long lookback
    period. Old prices are never removed from the calculation, but they have
    only a minimal impact on the Moving Average due to a low assigned
    weight. By reducing the noise it removes fluctuations and plots the
    prevailing trend. The SMMA can be used to confirm trends and define
    areas of support and resistance.
    A core component of Bill Williams Alligator indicator.

    Sources:
        https://www.tradingview.com/scripts/smma/
        https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=173&Name=Moving_Average_-_Smoothed

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        mamode (str): See ``help(ta.ma)``. Default: 'sma'
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 7)
    if "min_periods" in kwargs and kwargs["min_periods"] is not None:
        min_periods = int(kwargs["min_periods"])
    else:
        min_periods = length
    close = v_series(close, max(length, min_periods))

    if close is None:
        return

    mamode = v_mamode(mamode, "sma")
    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    m = close.size
    smma = close.copy()
    smma[:length - 1] = nan
    smma.iloc[length - 1] = ma(mamode, close[0:length], length=length, talib=mode_tal).iloc[-1]

    for i in range(length, m):
        smma.iat[i] = ((length - 1) * smma.iat[i - 1] + smma.iat[i]) / length

    # Offset
    if offset != 0:
        smma = smma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        smma.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    smma.name = f"SMMA_{length}"
    smma.category = "overlap"

    return smma
