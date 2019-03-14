# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from .overlap import ema, hlc3, sma
from .statistics import variance, stdev
from .utils import *



def accbands(high, low, close, length=None, c=None, drift=None, mamode=None, offset=None, **kwargs):
    """Indicator: Acceleration Bands (ACCBANDS)
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/acceleration-bands-abands/
    """
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 20
    c = float(c) if c and c > 0 else 4
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    mamode = mamode.lower() if mamode else 'sma'
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    hl_ratio  = (high - low) / (high + low)
    hl_ratio *= c
    _lower = low * (1 - hl_ratio)
    _upper = high * (1 + hl_ratio)

    if mamode is None or mamode == 'sma':
        lower = _lower.rolling(length, min_periods=min_periods).mean()
        mid   = close.rolling(length, min_periods=min_periods).mean()
        upper = _upper.rolling(length, min_periods=min_periods).mean()
    elif mamode == 'ema':
        lower = _lower.ewm(span=length, min_periods=min_periods).mean()
        mid   = close.ewm(span=length, min_periods=min_periods).mean()
        upper = _upper.ewm(span=length, min_periods=min_periods).mean()

    # Offset
    if offset != 0:
        lower = lower.shift(offset)
        mid = mid.shift(offset)
        upper = upper.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        lower.fillna(kwargs['fillna'], inplace=True)
        mid.fillna(kwargs['fillna'], inplace=True)
        upper.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        lower.fillna(method=kwargs['fill_method'], inplace=True)
        mid.fillna(method=kwargs['fill_method'], inplace=True)
        upper.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    lower.name = f"ACCBL_{length}"
    mid.name = f"ACCBM_{length}"
    upper.name = f"ACCBU_{length}"
    mid.category = upper.category = lower.category = 'volatility'

    # Prepare DataFrame to return
    data = {lower.name: lower, mid.name: mid, upper.name: upper}
    accbandsdf = pd.DataFrame(data)
    accbandsdf.name = f"ACCBANDS_{length}"
    accbandsdf.category = 'volatility'

    return accbandsdf


def atr(high, low, close, length=None, mamode=None, drift=None, offset=None, **kwargs):
    """Indicator: Average True Range (ATR)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    mamode = mamode.lower() if mamode else 'ema'
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    tr = true_range(high=high, low=low, close=close, drift=drift)
    if mamode == 'ema':
        atr = tr.ewm(span=length, min_periods=min_periods).mean()
    else:
        atr = tr.rolling(length, min_periods=min_periods).mean()

    # Offset
    if offset != 0:
        atr = atr.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        atr.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        atr.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    atr.name = f"ATR_{length}"
    atr.category = 'volatility'

    return atr


def bbands(close, length=None, std=None, mamode=None, offset=None, **kwargs):
    """Indicator: Bollinger Bands (BBANDS)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 20
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    std = float(std) if std and std > 0 else 2
    mamode = mamode.lower() if mamode else 'ema'
    offset = get_offset(offset)

    # Calculate Result
    standard_deviation = stdev(close=close, length=length)
    # std = variance(close=close, length=length).apply(np.sqrt)

    if mamode is None or mamode == 'sma':
        mid = close.rolling(length, min_periods=min_periods).mean()
    elif mamode == 'ema':
        mid = close.ewm(span=length, min_periods=min_periods).mean()

    lower = mid - std * standard_deviation
    upper = mid + std * standard_deviation

    # Offset
    if offset != 0:
        lower = lower.shift(offset)
        mid = mid.shift(offset)
        upper = upper.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        lower.fillna(kwargs['fillna'], inplace=True)
        mid.fillna(kwargs['fillna'], inplace=True)
        upper.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        lower.fillna(method=kwargs['fill_method'], inplace=True)
        mid.fillna(method=kwargs['fill_method'], inplace=True)
        upper.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    lower.name = f"BBL_{length}"
    mid.name = f"BBM_{length}"
    upper.name = f"BBU_{length}"
    mid.category = upper.category = lower.category = 'volatility'

    # Prepare DataFrame to return
    data = {lower.name: lower, mid.name: mid, upper.name: upper}
    bbandsdf = pd.DataFrame(data)
    bbandsdf.name = f"BBANDS_{length}"
    bbandsdf.category = 'volatility'

    return bbandsdf


def donchian(close, length=None, offset=None, **kwargs):
    """Indicator: Donchian Channels (DC)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 20
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    lower = close.rolling(length, min_periods=min_periods).min()
    upper = close.rolling(length, min_periods=min_periods).max()
    mid = 0.5 * (lower + upper)

    # Handle fills
    if 'fillna' in kwargs:
        lower.fillna(kwargs['fillna'], inplace=True)
        mid.fillna(kwargs['fillna'], inplace=True)
        upper.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        lower.fillna(method=kwargs['fill_method'], inplace=True)
        mid.fillna(method=kwargs['fill_method'], inplace=True)
        upper.fillna(method=kwargs['fill_method'], inplace=True)

    # Offset
    if offset != 0:
        lower = lower.shift(offset)
        mid = mid.shift(offset)
        upper = upper.shift(offset)

    # Name and Categorize it
    lower.name = f"DCL_{length}"
    mid.name = f"DCM_{length}"
    upper.name = f"DCU_{length}"
    mid.category = upper.category = lower.category = 'volatility'

    # Prepare DataFrame to return
    data = {lower.name: lower, mid.name: mid, upper.name: upper}
    dcdf = pd.DataFrame(data)
    dcdf.name = f"DC_{length}"
    dcdf.category = 'volatility'

    return dcdf


def kc(high, low, close, length=None, scalar=None, mamode=None, offset=None, **kwargs):
    """Indicator: Keltner Channels (KC)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 20
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    scalar = float(scalar) if scalar and scalar > 0 else 2
    mamode = mamode.lower() if mamode else None
    offset = get_offset(offset)

    # Calculate Result
    std = variance(close=close, length=length).apply(np.sqrt)

    if mamode == 'ema':
        basis = close.ewm(span=length, min_periods=min_periods).mean()
        band = atr(high=high, low=low, close=close)
    else:
        hl_range = high - low
        typical_price = hlc3(high=high, low=low, close=close)
        basis = typical_price.rolling(length, min_periods=min_periods).mean()
        band = hl_range.rolling(length, min_periods=min_periods).mean()

    lower = basis - scalar * band
    upper = basis + scalar * band

    # Offset
    if offset != 0:
        lower = lower.shift(offset)
        basis = basis.shift(offset)
        upper = upper.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        lower.fillna(kwargs['fillna'], inplace=True)
        basis.fillna(kwargs['fillna'], inplace=True)
        upper.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        lower.fillna(method=kwargs['fill_method'], inplace=True)
        basis.fillna(method=kwargs['fill_method'], inplace=True)
        upper.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    lower.name = f"KCL_{length}"
    basis.name = f"KCB_{length}"
    upper.name = f"KCU_{length}"
    basis.category = upper.category = lower.category = 'volatility'

    # Prepare DataFrame to return
    data = {lower.name: lower, basis.name: basis, upper.name: upper}
    kcdf = pd.DataFrame(data)
    kcdf.name = f"KC_{length}"
    kcdf.category = 'volatility'

    return kcdf


def massi(high, low, fast=None, slow=None, offset=None, **kwargs):
    """Indicator: Mass Index (MASSI)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    fast = int(fast) if fast and fast > 0 else 9
    slow = int(slow) if slow and slow > 0 else 25
    if slow < fast:
        fast, slow = slow, fast
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else fast
    offset = get_offset(offset)

    # Calculate Result
    hl_range = high - low
    hl_ema1 = ema(close=hl_range, length=fast)
    hl_ema2 = ema(close=hl_ema1, length=fast)

    hl_ratio = hl_ema1 / hl_ema2
    massi = hl_ratio.rolling(slow, min_periods=slow).sum()

    # Offset
    if offset != 0:
        massi = massi.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        massi.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        massi.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    massi.name = f"MASSI_{fast}_{slow}"
    massi.category = 'volatility'

    return massi


def natr(high, low, close, length=None, mamode=None, drift=None, offset=None, **kwargs):
    """Indicator: Normalized Average True Range (NATR)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    mamode = mamode.lower() if mamode else 'ema'
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    natr = (100 / close) * atr(high=high, low=low, close=close, length=length, mamode=mamode, drift=drift, offset=offset, **kwargs)

    # Offset
    if offset != 0:
        natr = natr.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        natr.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        natr.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    natr.name = f"NATR_{length}"
    natr.category = 'volatility'

    return natr


def true_range(high, low, close, drift=None, offset=None, **kwargs):
    """Indicator: True Range"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    prev_close = close.shift(drift)
    ranges = [high - low, high - prev_close, low - prev_close]
    true_range = pd.DataFrame(ranges).T
    true_range = true_range.abs().max(axis=1)

    # Offset
    if offset != 0:
        true_range = true_range.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        true_range.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        true_range.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    true_range.name = f"TRUERANGE_{drift}"
    true_range.category = 'volatility'

    return true_range



# Volatility Documentation
accbands.__doc__ = \
"""Acceleration Bands (ACCBANDS)

Acceleration Bands created by Price Headley plots upper and lower envelope
bands around a simple moving average.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/acceleration-bands-abands/

Calculation:
    Default Inputs:
        length=10, c=4
    EMA = Exponential Moving Average
    SMA = Simple Moving Average
    HL_RATIO = c * (high - low) / (high + low)
    LOW = low * (1 - HL_RATIO)
    HIGH = high * (1 + HL_RATIO)

    if 'ema':
        LOWER = EMA(LOW, length)
        MID = EMA(close, length)
        UPPER = EMA(HIGH, length)
    else:
        LOWER = SMA(LOW, length)
        MID = SMA(close, length)
        UPPER = SMA(HIGH, length)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    c (int): Multiplier.  Default: 4
    mamode (str): Two options: None or 'ema'.  Default: 'ema'
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: lower, mid, upper columns.
"""


atr.__doc__ = \
"""Average True Range (ATR)

Averge True Range is used to measure volatility, especially
volatility caused by gaps or limit moves.

Sources:
    https://www.tradingview.com/wiki/Average_True_Range_(ATR)

Calculation:
    Default Inputs:
        length=14, drift=1
    SMA = Simple Moving Average
    EMA = Exponential Moving Average
    TR = True Range
    tr = TR(high, low, close, drift)
    if 'ema':
        ATR = EMA(tr, length)
    else:
        ATR = SMA(tr, length)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 14
    mamode (str): Two options: None or 'ema'.  Default: 'ema'
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


bbands.__doc__ = \
"""Bollinger Bands (BBANDS)

A popular volatility indicator.

Sources:
    https://www.tradingview.com/wiki/Bollinger_Bands_(BB)

Calculation:
    Default Inputs:
        length=20, std=2
    EMA = Exponential Moving Average
    SMA = Simple Moving Average
    STDEV = Standard Deviation
    stdev = STDEV(close, length)
    if 'ema':
        MID = EMA(close, length)
    else:
        MID = SMA(close, length)
    
    LOWER = MID - std * stdev
    UPPER = MID + std * stdev

Args:
    close (pd.Series): Series of 'close's
    length (int): The short period.  Default: 20
    std (int): The long period.   Default: 2
    mamode (str): Two options: None or 'ema'.  Default: 'ema'
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: lower, mid, upper columns.
"""


donchian.__doc__ = \
"""Donchian Channels (DC)

Donchian Channels are used to measure volatility, similar to 
Bollinger Bands and Keltner Channels.

Sources:
    https://www.tradingview.com/wiki/Donchian_Channels_(DC)

Calculation:
    Default Inputs:
        length=20
    LOWER = close.rolling(length).min()
    UPPER = close.rolling(length).max()
    MID = 0.5 * (LOWER + UPPER)

Args:
    close (pd.Series): Series of 'close's
    length (int): The short period.  Default: 20
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: lower, mid, upper columns.
"""


kc.__doc__ = \
"""Keltner Channels (KC)

A popular volatility indicator similar to Bollinger Bands and
Donchian Channels.

Sources:
    https://www.tradingview.com/wiki/Keltner_Channels_(KC)

Calculation:
    Default Inputs:
        length=20, scalar=2
    ATR = Average True Range
    EMA = Exponential Moving Average
    SMA = Simple Moving Average
    if 'ema':
        BASIS = EMA(close, length)
        BAND = ATR(high, low, close)
    else:
        hl_range = high - low
        tp = typical_price = hlc3(high, low, close)
        BASIS = SMA(tp, length)
        BAND = SMA(hl_range, length)
    
    LOWER = BASIS - scalar * BAND
    UPPER = BASIS + scalar * BAND

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): The short period.  Default: 20
    scalar (float): A positive float to scale the bands.   Default: 2
    mamode (str): Two options: None or 'ema'.  Default: 'ema'
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: lower, basis, upper columns.
"""


massi.__doc__ = \
"""Mass Index (MASSI)

The Mass Index is a non-directional volatility indicator that utilitizes the
High-Low Range to identify trend reversals based on range expansions.

Sources:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:mass_index
    mi = sum(ema(high - low, 9) / ema(ema(high - low, 9), 9), length)

Calculation:
    Default Inputs:
        fast: 9, slow: 25
    EMA = Exponential Moving Average
    hl = high - low
    hl_ema1 = EMA(hl, fast)
    hl_ema2 = EMA(hl_ema1, fast)
    hl_ratio = hl_ema1 / hl_ema2
    MASSI = SUM(hl_ratio, slow)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    fast (int): The short period.  Default: 9
    slow (int): The long period.   Default: 25
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


natr.__doc__ = \
"""Normalized Average True Range (NATR)

Normalized Average True Range attempt to normalize the average
true range.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/normalized-average-true-range-natr/

Calculation:
    Default Inputs:
        length=20
    ATR = Average True Range
    NATR = (100 / close) * ATR(high, low, close)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): The short period.  Default: 20
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature
"""


true_range.__doc__ = \
"""True Range

An method to expand a classical range (high minus low) to include
possible gap scenarios.

Sources:
    https://www.macroption.com/true-range/

Calculation:
    Default Inputs:
        drift=1
    ABS = Absolute Value
    prev_close = close.shift(drift)
    TRUE_RANGE = ABS([high - low, high - prev_close, low - prev_close]) 

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    drift (int): The shift period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature
"""