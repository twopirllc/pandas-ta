# -*- coding: utf-8 -*-
from numpy import nan as npNaN
from pandas_ta.overlap import ma
from pandas_ta.utils import get_offset, verify_series


def smma(close, length=None, mamode=None, talib=None, offset=None, **kwargs):
    """Indicator: SMoothed Moving Average (SMMA)"""
    # Validate Arguments
    length = int(length) if length and length > 0 else 7
    min_periods = int(kwargs["min_periods"]) if "min_periods" in kwargs and kwargs["min_periods"] is not None else length
    close = verify_series(close, max(length, min_periods))
    offset = get_offset(offset)
    mamode = mamode.lower() if isinstance(mamode, str) else "sma"
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if close is None: return

    # Calculate Result
    m = close.size
    smma = close.copy()
    smma[:length - 1] = npNaN
    smma.iloc[length - 1] = ma(mamode, close[0:length], length=length, talib=mode_tal)[-1]

    for i in range(length, m):
        smma.iloc[i] = ((length - 1) * smma.iloc[i - 1] + smma.iloc[i]) / length

    # Offset
    if offset != 0:
        smma = smma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        smma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        smma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    smma.name = f"SMMA_{length}"
    smma.category = "overlap"

    return smma


smma.__doc__ = \
"""SMoothed Moving Average (SMMA)

The SMoothed Moving Average (SMMA) is bootstrapped by default with a Simple
Moving Average (SMA). It tries to reduce noise rather than reduce lag. The
SMMA takes all prices into account and uses a long lookback period. Old prices
are never removed from the calculation, but they have only a minimal impact on
the Moving Average due to a low assigned weight. By reducing the noise it
removes fluctuations and plots the prevailing trend. The SMMA can be used to
confirm trends and define areas of support and resistance. A core component of
Bill William's Alligator indicator.

Sources:
    https://www.tradingview.com/scripts/smma/
    https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=173&Name=Moving_Average_-_Smoothed

Calculation:
    Default Inputs:
        length=10, mamode="sma"
    MA = Moving Average

    SMMA[0:length] = MA(mamode, close, length)
    SMMA[:length] = ((length - 1) * SMMA[i] + close[i]) / length

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period. Default: 10
    mamode (str): See ```help(ta.ma)```. Default: 'sma'
    talib (bool): If TA Lib is installed and talib is True, Returns the TA Lib
        version. Default: True
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    adjust (bool): Default: True
    presma (bool, optional): If True, uses SMA for initial value.
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
