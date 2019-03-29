# -*- coding: utf-8 -*-
import math
import numpy as np
import pandas as pd

from .utils import fibonacci, get_drift, get_offset, pascals_triangle, verify_series, weights



def dema(close, length=None, offset=None, **kwargs):
    """Indicator: Double Exponential Moving Average (DEMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    ema1 = ema(close=close, length=length, **kwargs)
    ema2 = ema(close=ema1, length=length, **kwargs)
    dema = 2 * ema1 - ema2

    # Offset
    if offset != 0:
        dema = dema.shift(offset)

    # Name & Category
    dema.name = f"DEMA_{length}"
    dema.category = 'overlap'

    return dema


def ema(close, length=None, offset=None, **kwargs):
    """Indicator: Exponential Moving Average (EMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = kwargs.pop('min_periods', length)
    adjust = kwargs.pop('adjust', True)
    offset = get_offset(offset)
    sma = kwargs.pop('sma', True)
    ewm = kwargs.pop('ewm', False)

    # Calculate Result
    if ewm:
        # Mathematical Implementation of an Exponential Weighted Moving Average
        ema = close.ewm(span=length, min_periods=min_periods, adjust=adjust).mean()
    else:
        alpha = 2 / (length + 1)
        close = close.copy()

        def ema_(series):
            # Technical Anaylsis Definition of an Exponential Moving Average
            # Slow for large series
            series.iloc[1] = alpha * (series.iloc[1] - series.iloc[0]) + series.iloc[0]
            return series.iloc[1]

        seed = close[0:length].mean() if sma else close.iloc[0]

        close[:length - 1] = np.NaN
        close.iloc[length - 1] = seed
        ma = close[length - 1:].rolling(2, min_periods=2).apply(ema_, raw=False)
        ema = close[:length].append(ma[1:])

    # Offset
    if offset != 0:
        ema = ema.shift(offset)

    # Name & Category
    ema.name = f"EMA_{length}"
    ema.category = 'overlap'

    return ema


def fwma(close, length=None, asc=None, offset=None, **kwargs):
    """Indicator: Fibonacci's Weighted Moving Average (FWMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    asc = asc if asc else True
    offset = get_offset(offset)

    # Calculate Result    
    fibs = fibonacci(n=length, weighted=True)
    fwma = close.rolling(length, min_periods=length).apply(weights(fibs), raw=True)

    # Offset
    if offset != 0:
        fwma = fwma.shift(offset)

    # Name & Category
    fwma.name = f"FWMA_{length}"
    fwma.category = 'overlap'

    return fwma


def hl2(high, low, offset=None, **kwargs):
    """Indicator: HL2 """
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    offset = get_offset(offset)

    # Calculate Result
    hl2 = 0.5 * (high + low)

    # Offset
    if offset != 0:
        hl2 = hl2.shift(offset)

    # Name & Category
    hl2.name = "HL2"
    hl2.category = 'overlap'

    return hl2


def hlc3(high, low, close, offset=None, **kwargs):
    """Indicator: HLC3"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)

    # Calculate Result
    hlc3 = (high + low + close) / 3

    # Offset
    if offset != 0:
        hlc3 = hlc3.shift(offset)

    # Name & Category
    hlc3.name = "HLC3"
    hlc3.category = 'overlap'

    return hlc3


def hma(close, length=None, offset=None, **kwargs):
    """Indicator: Hull Moving Average (HMA)
    
    Use help(df.ta.hma) for specific documentation where 'df' represents
    the DataFrame you are using.
    """
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    half_length = int(length / 2)
    sqrt_length = int(math.sqrt(length))

    wmaf = wma(close=close, length=half_length)
    wmas = wma(close=close, length=length)
    hma = wma(close=2 * wmaf - wmas, length=sqrt_length)

    # Offset
    if offset != 0:
        hma = hma.shift(offset)

    # Name & Category
    hma.name = f"HMA_{length}"
    hma.category = 'overlap'

    return hma


def ichimoku(high, low, close, tenkan=None, kijun=None, senkou=None, offset=None, **kwargs):
    """Indicator: Ichimoku Kinkō Hyō (Ichimoku)"""
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    tenkan = int(tenkan) if tenkan and tenkan > 0 else 9
    kijun = int(kijun) if kijun and kijun > 0 else 26
    senkou = int(senkou) if senkou and senkou > 0 else 52
    offset = get_offset(offset)

    # Calculate Result
    tenkan_sen = midprice(high=high, low=low, length=tenkan)
    kijun_sen = midprice(high=high, low=low, length=kijun)
    span_a = 0.5 * (tenkan_sen + kijun_sen)
    span_b = midprice(high=high, low=low, length=senkou)

    # Copy Span A and B values before their shift
    _span_a = span_a[-kijun:].copy()
    _span_b = span_b[-kijun:].copy()

    span_a = span_a.shift(kijun)
    span_b = span_b.shift(kijun)
    chikou_span = close.shift(-kijun)

    # Offset
    if offset != 0:
        tenkan_sen = tenkan_sen.shift(offset)
        kijun_sen = kijun_sen.shift(offset)
        span_a = span_a.shift(offset)
        span_b = span_b.shift(offset)
        chikou_span = chikou_span.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        span_a.fillna(kwargs['fillna'], inplace=True)
        span_b.fillna(kwargs['fillna'], inplace=True)
        chikou_span.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        span_a.fillna(method=kwargs['fill_method'], inplace=True)
        span_b.fillna(method=kwargs['fill_method'], inplace=True)
        chikou_span.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    span_a.name = f"ISA_{tenkan}"
    span_b.name = f"ISB_{kijun}"
    tenkan_sen.name = f"ITS_{tenkan}"
    kijun_sen.name = f"IKS_{kijun}"
    chikou_span.name = f"ICS_{kijun}"

    chikou_span.category = kijun_sen.category = tenkan_sen.category = 'trend'
    span_b.category = span_a.category = chikou_span

    # Prepare Ichimoku DataFrame
    data = {span_a.name: span_a, span_b.name: span_b, tenkan_sen.name: tenkan_sen, kijun_sen.name: kijun_sen, chikou_span.name: chikou_span}
    ichimokudf = pd.DataFrame(data)
    ichimokudf.name = f"ICHIMOKU_{tenkan}_{kijun}_{senkou}"
    ichimokudf.category = 'overlap'

    # Prepare Span DataFrame
    last = close.index[-1]
    if close.index.dtype == 'int64':
        ext_index = pd.RangeIndex(start=last + 1, stop=last + kijun + 1)
        spandf = pd.DataFrame(index=ext_index, columns=[span_a.name, span_b.name])
        _span_a.index = _span_b.index = ext_index
    else:
        df_freq = close.index.value_counts().mode()[0]
        tdelta = pd.Timedelta(df_freq, unit='d')
        new_dt = pd.date_range(start=last + tdelta, periods=kijun, freq='B')
        spandf = pd.DataFrame(index=new_dt, columns=[span_a.name, span_b.name])
        _span_a.index = _span_b.index = new_dt

    spandf[span_a.name] = _span_a
    spandf[span_b.name] = _span_b
    spandf.name = f"ICHISPAN_{tenkan}_{kijun}"
    spandf.category = 'overlap'

    return ichimokudf, spandf


def linreg(close, length=None, offset=None, **kwargs):
    """Indicator: Linear Regression"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)
    angle = kwargs.pop('angle', False)
    intercept = kwargs.pop('intercept', False)
    degrees = kwargs.pop('degrees', False)
    r = kwargs.pop('r', False)
    slope = kwargs.pop('slope', False)

    # Calculate Result
    x = range(1, length + 1) # [1, 2, ..., n] from 1 to n keeps Sum(xy) low
    x_sum = 0.5 * length * (length + 1)
    x2_sum = x_sum * (2 * length + 1) / 3
    divisor = length * x2_sum - x_sum * x_sum

    def linear_regression(series):
        y_sum = series.sum()
        xy_sum = (x * series).sum()

        m = (length * xy_sum - x_sum * y_sum) / divisor
        if slope:
            return m
        b = (y_sum * x2_sum - x_sum * xy_sum) / divisor
        if intercept:
            return b

        if angle:
            theta = math.atan(m)
            if degrees:
                theta *= 180 / math.pi
            return theta
        
        if r:
            y2_sum = (series * series).sum()
            rn = length * xy_sum - x_sum * y_sum
            rd = math.sqrt(divisor * (length * y2_sum - y_sum * y_sum))
            return rn / rd

        y = m * (length - 1) + b
        return y

    linreg = close.rolling(length, min_periods=length).apply(linear_regression, raw=False)

    # Offset
    if offset != 0:
        linreg = linreg.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        linreg.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        linreg.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    linreg.name = f"LR"
    if slope:
        linreg.name += "m"
    if intercept:
        linreg.name += "b"
    if angle:
        linreg.name += "a"
    if r:
        linreg.name += "r"
    linreg.name += f"_{length}"
    linreg.category = 'overlap'

    return linreg


def midpoint(close, length=None, offset=None, **kwargs):
    """Indicator: Midpoint"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 2
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    lowest = close.rolling(length, min_periods=min_periods).min()
    highest = close.rolling(length, min_periods=min_periods).max()
    midpoint = 0.5 * (lowest + highest)

    # Offset
    if offset != 0:
        midpoint = midpoint.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        midpoint.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        midpoint.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    midpoint.name = f"MIDPOINT_{length}"
    midpoint.category = 'overlap'

    return midpoint


def midprice(high, low, length=None, offset=None, **kwargs):
    """Indicator: Midprice"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    length = int(length) if length and length > 0 else 2
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    lowest_low = low.rolling(length, min_periods=min_periods).min()
    highest_high = high.rolling(length, min_periods=min_periods).max()
    midprice = 0.5 * (lowest_low + highest_high)

    # Offset
    if offset != 0:
        midprice = midprice.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        midprice.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        midprice.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    midprice.name = f"MIDPRICE_{length}"
    midprice.category = 'overlap'

    return midprice


def ohlc4(open_, high, low, close, offset=None, **kwargs):
    """Indicator: OHLC4"""
    # Validate Arguments
    open_ = verify_series(open_)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)

    # Calculate Result
    ohlc4 = 0.25 * (open_ + high + low + close)

    # Offset
    if offset != 0:
        ohlc4 = ohlc4.shift(offset)

    # Name & Category
    ohlc4.name = "OHLC4"
    ohlc4.category = 'overlap'

    return ohlc4


def pwma(close, length=None, asc=None, offset=None, **kwargs):
    """Indicator: Pascals Weighted Moving Average (PWMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    asc = asc if asc else True
    offset = get_offset(offset)

    # Calculate Result
    triangle = pascals_triangle(n=length - 1, weighted=True)
    pwma = close.rolling(length, min_periods=length).apply(weights(triangle), raw=True)

    # Offset
    if offset != 0:
        pwma = pwma.shift(offset)

    # Name & Category
    pwma.name = f"PWMA_{length}"
    pwma.category = 'overlap'

    return pwma


def rma(close, length=None, offset=None, **kwargs):
    """Indicator: wildeR's Moving Average (RMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)
    alpha = (1.0 / length) if length > 0 else 0.5

    # Calculate Result
    rma = close.ewm(alpha=alpha, min_periods=min_periods).mean()

    # Offset
    if offset != 0:
        rma = rma.shift(offset)

    # Name & Category
    rma.name = f"RMA_{length}"
    rma.category = 'overlap'

    return rma


def sma(close, length=None, offset=None, **kwargs):
    """Indicator: Simple Moving Average (SMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    sma = close.rolling(length, min_periods=min_periods).mean()

    # Offset
    if offset != 0:
        sma = sma.shift(offset)

    # Name & Category
    sma.name = f"SMA_{length}"
    sma.category = 'overlap'

    return sma


def t3(close, length=None, a=None, offset=None, **kwargs):
    """Indicator: T3"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    a = float(a) if a and a > 0 and a < 1 else 0.7
    offset = get_offset(offset)

    # Calculate Result
    c1 = -a * a ** 2
    c2 = 3 * a ** 2 + 3 * a ** 3
    c3 = -6 * a ** 2 - 3 * a - 3 * a ** 3
    c4 = a ** 3 + 3 * a ** 2 + 3 * a + 1

    e1 = ema(close=close, length=length, **kwargs)
    e2 = ema(close=e1, length=length, **kwargs)
    e3 = ema(close=e2, length=length, **kwargs)
    e4 = ema(close=e3, length=length, **kwargs)
    e5 = ema(close=e4, length=length, **kwargs)
    e6 = ema(close=e5, length=length, **kwargs)
    t3 = c1 * e6 + c2 * e5 + c3 * e4 + c4 * e3

    # Offset
    if offset != 0:
        t3 = t3.shift(offset)

    # Name & Category
    t3.name = f"T3_{length}_{a}"
    t3.category = 'overlap'

    return t3


def tema(close, length=None, offset=None, **kwargs):
    """Indicator: Triple Exponential Moving Average (TEMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    ema1 = ema(close=close, length=length, **kwargs)
    ema2 = ema(close=ema1, length=length, **kwargs)
    ema3 = ema(close=ema2, length=length, **kwargs)
    tema = 3 * (ema1 - ema2) + ema3

    # Offset
    if offset != 0:
        tema = tema.shift(offset)

    # Name & Category
    tema.name = f"TEMA_{length}"
    tema.category = 'overlap'

    return tema


def trima(close, length=None, offset=None, **kwargs):
    """Indicator: Triangular Moving Average (TRIMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    half_length = round(0.5 * (length + 1))
    sma1 = close.rolling(half_length, min_periods=half_length).mean()
    trima = sma1.rolling(half_length, min_periods=half_length).mean()

    # Offset
    if offset != 0:
        trima = trima.shift(offset)

    # Name & Category
    trima.name = f"TRIMA_{length}"
    trima.category = 'overlap'

    return trima


def vwap(high, low, close, volume, offset=None, **kwargs):
    """Indicator: Volume Weighted Average Price (VWAP)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    volume = verify_series(volume)
    offset = get_offset(offset)

    # Calculate Result
    tp = hlc3(high=high, low=low, close=close)
    tpv = tp * volume
    vwap = tpv.cumsum() / volume.cumsum()

    # Offset
    if offset != 0:
        vwap = vwap.shift(offset)

    # Name & Category
    vwap.name = "VWAP"
    vwap.category = 'overlap'

    return vwap


def vwma(close, volume, length=None, offset=None, **kwargs):
    """Indicator: Volume Weighted Moving Average (VWMA)"""
    # Validate Arguments
    close = verify_series(close)
    volume = verify_series(volume)
    length = int(length) if length and length > 0 else 10
    offset = get_offset(offset)

    # Calculate Result
    pv = close * volume
    vwma = sma(close=pv, length=length) / sma(close=volume, length=length)

    # Offset
    if offset != 0:
        vwma = vwma.shift(offset)

    # Name & Category
    vwma.name = f"VWMA_{length}"
    vwma.category = 'overlap'

    return vwma


def wma(close, length=None, asc=None, offset=None, **kwargs):
    """Indicator: Weighted Moving Average (WMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    asc = asc if asc else True
    offset = get_offset(offset)

    # Calculate Result
    total_weight = 0.5 * length * (length + 1)
    weights_ = pd.Series(np.arange(1, length + 1))
    weights = weights_ if asc else weights_[::-1]

    def linear_weights(w):
        def _compute(x):
            return (w * x).sum() / total_weight
        return _compute

    close_ = close.rolling(length, min_periods=length)
    wma = close_.apply(linear_weights(weights), raw=True)

    # Offset
    if offset != 0:
        wma = wma.shift(offset)

    # Name & Category
    wma.name = f"WMA_{length}"
    wma.category = 'overlap'

    return wma


def zlma(close, length=None, offset=None, mamode=None, **kwargs):
    """Indicator: Zero Lag Moving Average (ZLMA)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)
    mamode = mamode.lower() if mamode else None

    # Calculate Result
    lag = int(0.5 * (length - 1))
    close = 2 * close - close.shift(lag)
    if mamode is None or mamode == 'ema':
        zlma = ema(close, length=length, **kwargs)
        kind = "E"
    if mamode == 'hma':
        zlma = hma(close, length=length, **kwargs)
        kind = "H"
    if mamode == 'sma':
        zlma = sma(close, length=length, **kwargs)
        kind = "S"
    if mamode == 'wma':
        zlma = wma(close, length=length, **kwargs)
        kind = "W"

    # Offset
    if offset != 0:
        zlma = zlma.shift(offset)

    # Name & Category
    zlma.name = f"ZL{kind}MA_{length}"
    zlma.category = 'overlap'

    return zlma



# Overlap Documentation
hl2.__doc__ = \
"""Average of High-Low (HL2)

Equally weighted Average of two series', namely High and Low.

Sources:
    https://www.tradingview.com/study-script-reference/#var_hl2

Calculation:
    HL2 = 0.5 * (high + low)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


ichimoku.__doc__ = \
"""Ichimoku Kinkō Hyō (Ichimoku)

It identifies the trend and look for potential signals within that trend.

Sources:
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ichimoku_cloud

Calculation:
    Default Inputs:
        tenkan=9, kijun=26, senkou=52
    tenkan_sen = midprice(high, low, length=tenkan)
    kijun_sen = midprice(high, low, length=kijun)
    span_a = 0.5 * (tenkan_sen + kijun_sen)
    span_b = midprice(high=high, low=low, length=senkou)

    span_a = span_a.shift(kijun)
    span_b = span_b.shift(kijun)
    chikou_span = close.shift(-kijun)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    tenkan (int): Tenkan period.  Default: 9
    kijun (int): Kijun period.  Default: 26
    senkou (int): Senkou period.  Default: 52
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pandas.Series: New feature generated.
"""



hlc3.__doc__ = \
"""Average of High-Low-Close (HLC3)

Equally weighted Average of three series', namely High, Low, Close.

Sources:
    https://www.tradingview.com/study-script-reference/#var_hlc3

Calculation:
    HLC3 = (high + low + close) / 3.0

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


ohlc4.__doc__ = \
"""Average of Open-High-Low-Close (OHLC4)

Equally weighted Average of four series', namely Open, High, Low, Close.

Sources:
    https://www.tradingview.com/study-script-reference/#var_ohlc4

Calculation:
    OHLC4 = 0.25 * (open + high + low + close)

Args:
    open (pd.Series): Series of 'open's
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


midpoint.__doc__ = \
"""Midpoint (MIDPOINT)

The Midpoint is the average of the highest and lowest closes over a period.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/midpoint-midpnt/

Calculation:
    Default Inputs:
        length=1
    lowest_close  = close.rolling(length).min()
    highest_close = close.rolling(length).max()

    MIDPOINT = 0.5 * (highest_close + lowest_close)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 14
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


midprice.__doc__ = \
"""Midprice (MIDPRICE)

William's Percent R is a momentum oscillator similar to the RSI that
attempts to identify overbought and oversold conditions.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/midprice-midpri/

Calculation:
    Default Inputs:
        length=1
    lowest_low   = low.rolling(length).min()
    highest_high = high.rolling(length).max()

    MIDPRICE = 0.5 * (highest_high + lowest_low)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    length (int): It's period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


dema.__doc__ = \
"""Double Exponential Moving Average (DEMA)

The Double Exponential Moving Average attempts to a smoother average with less
lag than the normal Exponential Moving Average (EMA).

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/double-exponential-moving-average-dema/

Calculation:
    Default Inputs:
        length=10
    EMA = Exponential Moving Average
    ema1 = EMA(close, length)
    ema2 = EMA(ema1, length)

    DEMA = 2 * ema1 - ema2

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


ema.__doc__ = \
"""Exponential Moving Average (EMA)

The Exponential Moving Average is more responsive moving average compared to the
Simple Moving Average (SMA).  The weights are determined by alpha which is
proportional to it's length.  There are several different methods of calculating
EMA.  One method uses just the standard definition of EMA and another uses the
SMA to generate the initial value for the rest of the calculation.

Sources:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_averages
    https://www.investopedia.com/ask/answers/122314/what-exponential-moving-average-ema-formula-and-how-ema-calculated.asp

Calculation:
    Default Inputs:
        length=10
    SMA = Simple Moving Average
    if kwargs['presma']:
        initial = SMA(close, length)
        rest = close[length:]
        close = initial + rest

    EMA = close.ewm(span=length, adjust=adjust).mean()

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    adjust (bool, optional): Default: True
    sma (bool, optional): If True, uses SMA for initial value.
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


fwma.__doc__ = \
"""Fibonacci's Weighted Moving Average (FWMA)

Fibonacci's Weighted Moving Average is similar to a Weighted Moving Average
(WMA) where the weights are based on the Fibonacci Sequence.

Source: Kevin Johnson

Calculation:
    Default Inputs:
        length=10, 

    def weights(w):
        def _compute(x):
            return np.dot(w * x)
        return _compute

    fibs = utils.fibonacci(length - 1)
    FWMA = close.rolling(length)_.apply(weights(fibs), raw=True)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    asc (bool): Recent values weigh more.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


hma.__doc__ = \
"""Hull Moving Average (HMA)

The Hull Exponential Moving Average attempts to reduce or remove lag in moving
averages.

Sources:
    https://alanhull.com/hull-moving-average

Calculation:
    Default Inputs:
        length=10
    WMA = Weighted Moving Average
    half_length = int(0.5 * length)
    sqrt_length = int(math.sqrt(length))

    wmaf = WMA(close, half_length)
    wmas = WMA(close, length)
    HMA = WMA(2 * wmaf - wmas, sqrt_length)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


ichimoku.__doc__ = \
"""Ichimoku Kinkō Hyō (ichimoku)

Developed Pre WWII as a forecasting model for financial markets.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/ichimoku-ich/

Calculation:
    Default Inputs:
        tenkan=9, kijun=26, senkou=52
    MIDPRICE = Midprice
    TENKAN_SEN = MIDPRICE(high, low, close, length=tenkan)
    KIJUN_SEN = MIDPRICE(high, low, close, length=kijun)
    CHIKOU_SPAN = close.shift(-kijun)

    SPAN_A = 0.5 * (TENKAN_SEN + KIJUN_SEN)
    SPAN_A = SPAN_A.shift(kijun)

    SPAN_B = MIDPRICE(high, low, close, length=senkou)
    SPAN_B = SPAN_B.shift(kijun)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    tenkan (int): Tenkan period.  Default: 9
    kijun (int): Kijun period.  Default: 26
    senkou (int): Senkou period.  Default: 52
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: Two DataFrames.
        For the visible period: spanA, spanB, tenkan_sen, kijun_sen,
            and chikou_span columns
        For the forward looking period: spanA and spanB columns
"""


linreg.__doc__ = \
"""Linear Regression Moving Average (linreg)

Linear Regression Moving Average

Source: TA Lib

Calculation:
    Default Inputs:
        length=14
    x = [1, 2, ..., n]
    x_sum = 0.5 * length * (length + 1)
    x2_sum = length * (length + 1) * (2 * length + 1) / 6
    divisor = length * x2_sum - x_sum * x_sum

    lr(series):
        y_sum = series.sum()
        y2_sum = (series* series).sum()
        xy_sum = (x * series).sum()

        m = (length * xy_sum - x_sum * y_sum) / divisor
        b = (y_sum * x2_sum - x_sum * xy_sum) / divisor
        return m * (length - 1) + b

    linreg = close.rolling(length).apply(lr)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method
    angle (bool, optional): Default: False.  If True, returns the angle of the slope in radians
    degrees (bool, optional): Default: False.  If True, returns the angle of the slope in degrees
    intercept (bool, optional): Default: False.  If True, returns the angle of the slope in radians
    r (bool, optional): Default: False.  If True, returns it's correlation 'r'
    slope (bool, optional): Default: False.  If True, returns the slope

Returns:
    pd.Series: New feature generated.
"""


pwma.__doc__ = \
"""Pascal's Weighted Moving Average (PWMA)

Pascal's Weighted Moving Average is similar to a symmetric triangular
window except PWMA's weights are based on Pascal's Triangle.

Source: Kevin Johnson

Calculation:
    Default Inputs:
        length=10, 

    def weights(w):
        def _compute(x):
            return np.dot(w * x)
        return _compute

    triangle = utils.pascals_triangle(length + 1)
    PWMA = close.rolling(length)_.apply(weights(triangle), raw=True)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    asc (bool): Recent values weigh more.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


rma.__doc__ = \
"""wildeR's Moving Average (RMA)

The WildeR's Moving Average is simply an Exponential Moving Average (EMA)
with a modified alpha = 1 / length.

Sources:
    https://alanhull.com/hull-moving-average

Calculation:
    Default Inputs:
        length=10
    EMA = Exponential Moving Average
    alpha = 1 / length
    RMA = EMA(close, alpha=alpha)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


sma.__doc__ = \
"""Simple Moving Average (SMA)

The Simple Moving Average is the classic moving average that is the equally
weighted average over n periods.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/simple-moving-average-sma/

Calculation:
    Default Inputs:
        length=10
    SMA = SUM(close, length) / length

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    adjust (bool): Default: True
    presma (bool, optional): If True, uses SMA for initial value.
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


t3.__doc__ = \
"""Tim Tillson's T3 Moving Average (T3)

Tim Tillson's T3 Moving Average is considered a smoother and more responsive
moving average relative to other moving averages.

Sources:
    http://www.binarytribune.com/forex-trading-indicators/t3-moving-average-indicator/

Calculation:
    Default Inputs:
        length=10, a=0.7
    c1 = -a^3
    c2 = 3a^2 + 3a^3 = 3a^2 * (1 + a)
    c3 = -6a^2 - 3a - 3a^3
    c4 = a^3 + 3a^2 + 3a + 1

    ema1 = EMA(close, length)
    ema2 = EMA(ema1, length)
    ema3 = EMA(ema2, length)
    ema4 = EMA(ema3, length)
    ema5 = EMA(ema4, length)
    ema6 = EMA(ema5, length)
    T3 = c1 * ema6 + c2 * ema5 + c3 * ema4 + c4 * ema3

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    a (float): 0 < a < 1.  Default: 0.7
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    adjust (bool): Default: True
    presma (bool, optional): If True, uses SMA for initial value.
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


tema.__doc__ = \
"""Triple Exponential Moving Average (TEMA)

A less laggy Exponential Moving Average.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/triple-exponential-moving-average-tema/

Calculation:
    Default Inputs:
        length=10
    EMA = Exponential Moving Average
    ema1 = EMA(close, length)
    ema2 = EMA(ema1, length)
    ema3 = EMA(ema2, length)
    TEMA = 3 * (ema1 - ema2) + ema3

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    adjust (bool): Default: True
    presma (bool, optional): If True, uses SMA for initial value.
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


trima.__doc__ = \
"""Triangular Moving Average (TRIMA)

A weighted moving average where the shape of the weights are triangular and the
greatest weight is in the middle of the period.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/triangular-moving-average-trima/
    tma = sma(sma(src, ceil(length / 2)), floor(length / 2) + 1)  # Tradingview
    trima = sma(sma(x, n), n)  # Tradingview

Calculation:
    Default Inputs:
        length=10
    SMA = Simple Moving Average
    half_length = math.round(0.5 * (length + 1))
    SMA1 = SMA(close, half_length)
    TRIMA = SMA(SMA1, half_length)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    adjust (bool): Default: True
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


vwap.__doc__ = \
"""Volume Weighted Average Price (VWAP)

The Volume Weighted Average Price that measures the average typical price
by volume.  It is typically used with intraday charts to identify general
direction.

Sources:
    https://www.tradingview.com/wiki/Volume_Weighted_Average_Price_(VWAP)
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/volume-weighted-average-price-vwap/

Calculation:
    tp = typical_price = hlc3(high, low, close)
    tpv = tp * volume
    VWAP = tpv.cumsum() / volume.cumsum()

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


vwma.__doc__ = \
"""Volume Weighted Moving Average (VWMA)

Volume Weighted Moving Average.

Sources:
    https://www.motivewave.com/studies/volume_weighted_moving_average.htm

Calculation:
    Default Inputs:
        length=10
    SMA = Simple Moving Average
    pv = close * volume
    VWMA = SMA(pv, length) / SMA(volume, length)

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    length (int): It's period.  Default: 10
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


wma.__doc__ = \
"""Weighted Moving Average (WMA)

The Weighted Moving Average where the weights are linearly increasing and
the most recent data has the heaviest weight.

Sources:
    https://en.wikipedia.org/wiki/Moving_average#Weighted_moving_average

Calculation:
    Default Inputs:
        length=10, asc=True
    total_weight = 0.5 * length * (length + 1)
    weights_ = [1, 2, ..., length + 1]  # Ascending
    weights = weights if asc else weights[::-1]

    def linear_weights(w):
        def _compute(x):
            return (w * x).sum() / total_weight
        return _compute

    WMA = close.rolling(length)_.apply(linear_weights(weights), raw=True)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    asc (bool): Recent values weigh more.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


zlma.__doc__ = \
"""Zero Lag Moving Average (ZLMA)

The Zero Lag Moving Average attempts to eliminate the lag associated
with moving averages.  This is an adaption created by John Ehler and Ric Way.

Sources:
    https://en.wikipedia.org/wiki/Zero_lag_exponential_moving_average

Calculation:
    Default Inputs:
        length=10, mamode=EMA
    EMA = Exponential Moving Average
    lag = int(0.5 * (length - 1))
    source = 2 * close - close.shift(lag)
    ZLMA = EMA(source, length)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    mamode (str): Two options: None or 'ema'.  Default: 'ema'
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""