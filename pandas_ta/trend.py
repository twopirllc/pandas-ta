# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from .momentum import roc
from .overlap import dema, ema, hma, midprice, rma, sma
from .utils import get_drift, get_offset, verify_series, zero
from .volatility.true_range import true_range
from .volatility.atr import atr



def adx(high, low, close, length=None, drift=None, offset=None, **kwargs):
    """Indicator: ADX"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = length if length and length > 0 else 14
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    _atr = atr(high=high, low=low, close=close, length=length)

    up = high - high.shift(drift)
    dn = low.shift(drift) - low

    pos = ((up > dn) & (up > 0)) * up
    neg = ((dn > up) & (dn > 0)) * dn

    pos = pos.apply(zero)
    neg = neg.apply(zero)

    dmp = (100 / _atr) * rma(close=pos, length=length)
    dmn = (100 / _atr) * rma(close=neg, length=length)

    dx = 100 * (dmp - dmn).abs() / (dmp + dmn)
    adx = rma(close=dx, length=length)

    # Offset
    if offset != 0:
        dmp = dmp.shift(offset)
        dmn = dmn.shift(offset)
        adx = adx.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        adx.fillna(kwargs['fillna'], inplace=True)
        dmp.fillna(kwargs['fillna'], inplace=True)
        dmn.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        adx.fillna(method=kwargs['fill_method'], inplace=True)
        dmp.fillna(method=kwargs['fill_method'], inplace=True)
        dmn.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    adx.name = f"ADX_{length}"
    dmp.name = f"DMP_{length}"
    dmn.name = f"DMN_{length}"

    adx.category = dmp.category = dmn.category = 'trend'

    # Prepare DataFrame to return
    data = {adx.name: adx, dmp.name: dmp, dmn.name: dmn}
    adxdf = pd.DataFrame(data)
    adxdf.name = f"ADX_{length}"
    adxdf.category = 'trend'

    return adxdf


def amat(close=None, fast=None, slow=None, mamode=None, lookback=None, offset=None, **kwargs):
    """Indicator: Archer Moving Averages Trends (AMAT)"""
    # Validate Arguments
    close = verify_series(close)
    fast = int(fast) if fast and fast > 0 else 8
    slow = int(slow) if slow and slow > 0 else 21
    lookback = int(lookback) if lookback and lookback > 0 else 2
    mamode = mamode.upper() if mamode else 'EMA'
    offset = get_offset(offset)

    # Calculate Result
    if mamode == 'EMA':
        fast_ma = ema(close=close, length=fast, **kwargs)
        slow_ma = ema(close=close, length=slow, **kwargs)
    elif mamode == 'HMA':
        fast_ma = hma(close=close, length=fast, **kwargs)
        slow_ma = hma(close=close, length=slow, **kwargs)
    elif mamode == 'LINREG':
        fast_ma = linreg(close=close, length=fast, **kwargs)
        slow_ma = linreg(close=close, length=slow, **kwargs)
    elif mamode == 'RMA':
        fast_ma = rma(close=close, length=fast, **kwargs)
        slow_ma = rma(close=close, length=slow, **kwargs)
    elif mamode == 'SMA':
        fast_ma = sma(close=close, length=fast, **kwargs)
        slow_ma = sma(close=close, length=slow, **kwargs)
    elif mamode == 'WMA':
        fast_ma = wma(close=close, length=fast, **kwargs)
        slow_ma = wma(close=close, length=slow, **kwargs)

    mas_long = long_run(fast_ma, slow_ma, length=lookback)
    mas_short = short_run(fast_ma, slow_ma, length=lookback)

    # Offset
    if offset != 0:
        mas_long = mas_long.shift(offset)
        mas_short = mas_short.shift(offset)

    # # Handle fills
    if 'fillna' in kwargs:
        mas_long.fillna(kwargs['fillna'], inplace=True)
        mas_short.fillna(kwargs['fillna'], inplace=True)

    if 'fill_method' in kwargs:
        mas_long.fillna(method=kwargs['fill_method'], inplace=True)
        mas_short.fillna(method=kwargs['fill_method'], inplace=True)

    # Prepare DataFrame to return
    amatdf = pd.DataFrame({
        f"AMAT_{mas_long.name}": mas_long,
        f"AMAT_{mas_short.name}": mas_short
    })

    # Name and Categorize it
    amatdf.name = f"AMAT_{mamode}_{fast}_{slow}_{lookback}"
    amatdf.category = 'trend'

    return amatdf


def aroon(close, length=None, offset=None, **kwargs):
    """Indicator: Aroon Oscillator"""
    # Validate Arguments
    close = verify_series(close)
    length = length if length and length > 0 else 14
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    def maxidx(x):
        return 100 * (int(np.argmax(x)) + 1) / length

    def minidx(x):
        return 100 * (int(np.argmin(x)) + 1) / length

    _close = close.rolling(length, min_periods=min_periods)
    aroon_up = _close.apply(maxidx, raw=True)
    aroon_down = _close.apply(minidx, raw=True)

    # Handle fills
    if 'fillna' in kwargs:
        aroon_up.fillna(kwargs['fillna'], inplace=True)
        aroon_down.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        aroon_up.fillna(method=kwargs['fill_method'], inplace=True)
        aroon_down.fillna(method=kwargs['fill_method'], inplace=True)

    # Offset
    if offset != 0:
        aroon_up = aroon_up.shift(offset)
        aroon_down = aroon_down.shift(offset)

    # Name and Categorize it
    aroon_up.name = f"AROONU_{length}"
    aroon_down.name = f"AROOND_{length}"

    aroon_down.category = aroon_up.category = 'trend'

    # Prepare DataFrame to return
    data = {aroon_down.name: aroon_down, aroon_up.name: aroon_up}
    aroondf = pd.DataFrame(data)
    aroondf.name = f"AROON_{length}"
    aroondf.category = 'trend'

    return aroondf


def decreasing(close, length=None, asint=True, offset=None, **kwargs):
    """Indicator: Decreasing"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    decreasing = close.diff(length) < 0
    if asint:
        decreasing = decreasing.astype(int)

    # Offset
    if offset != 0:
        decreasing = decreasing.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        decreasing.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        decreasing.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    decreasing.name = f"DEC_{length}"
    decreasing.category = 'trend'

    return decreasing


def dpo(close, length=None, centered=True, offset=None, **kwargs):
    """Indicator: Detrend Price Oscillator (DPO)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 1
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    drift = int(0.5 * length) + 1  # int((0.5 * length) + 1)
    dpo = close.shift(drift) - close.rolling(length, min_periods=min_periods).mean()
    if centered:
        dpo = dpo.shift(-drift)

    # Offset
    if offset != 0:
        dpo = dpo.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        dpo.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        dpo.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    dpo.name = f"DPO_{length}"
    dpo.category = 'trend'

    return dpo


def increasing(close, length=None, asint=True, offset=None, **kwargs):
    """Indicator: Increasing"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    increasing = close.diff(length) > 0
    if asint:
        increasing = increasing.astype(int)

    # Offset
    if offset != 0:
        increasing = increasing.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        increasing.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        increasing.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    increasing.name = f"INC_{length}"
    increasing.category = 'trend'

    return increasing


def long_run(fast, slow, length=None, offset=None, **kwargs):
    """Indicator: Long Run"""
    # Validate Arguments
    fast = verify_series(fast)
    slow = verify_series(slow)
    length = int(length) if length and length > 0 else 2
    offset = get_offset(offset)

    # Calculate Result
    pb = increasing(fast, length) & decreasing(slow, length)  # potential bottom or bottom
    bi = increasing(fast, length) & increasing(slow, length)  # fast and slow are increasing
    long_run = pb | bi

    # Offset
    if offset != 0:
        long_run = long_run.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        long_run.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        long_run.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    long_run.name = f"LR_{length}"
    long_run.category = 'trend'

    return long_run


def qstick(open_, close, length=None, offset=None, **kwargs):
    """Indicator: Q Stick"""
    # Validate Arguments
    open_ = verify_series(open_)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    offset = get_offset(offset)
    ma = kwargs.pop('ma', 'sma') if 'ma' in kwargs else 'sma'

    # Calculate Result
    diff = close - open_

    if ma in [None, 'sma']: qstick = sma(diff, length=length)
    if ma == 'dema': qstick = dema(diff, length=length, **kwargs)
    if ma == 'ema': qstick = ema(diff, length=length, **kwargs)
    if ma == 'hma': qstick = hma(diff, length=length)
    if ma == 'rma': qstick = rma(diff, length=length)

    # Offset
    if offset != 0:
        qstick = qstick.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        qstick.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        qstick.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    qstick.name = f"QS_{length}"
    qstick.category = 'trend'

    return qstick


def short_run(fast, slow, length=None, offset=None, **kwargs):
    """Indicator: Short Run"""
    # Validate Arguments
    fast = verify_series(fast)
    slow = verify_series(slow)
    length = int(length) if length and length > 0 else 2
    offset = get_offset(offset)

    # Calculate Result
    pt = decreasing(fast, length) & increasing(slow, length)  # potential top or top
    bd = decreasing(fast, length) & decreasing(slow, length)  # fast and slow are decreasing
    short_run = pt | bd

    # Offset
    if offset != 0:
        short_run = short_run.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        short_run.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        short_run.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    short_run.name = f"SR_{length}"
    short_run.category = 'trend'

    return short_run


def vortex(high, low, close, length=None, drift=None, offset=None, **kwargs):
    """Indicator: Vortex"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = length if length and length > 0 else 14
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    tr = true_range(high=high, low=low, close=close)
    tr_sum = tr.rolling(length, min_periods=min_periods).sum()

    vmp = (high - low.shift(drift)).abs()
    vmm = (low - high.shift(drift)).abs()

    vip = vmp.rolling(length, min_periods=min_periods).sum() / tr_sum
    vim = vmm.rolling(length, min_periods=min_periods).sum() / tr_sum

    # Offset
    if offset != 0:
        vip = vip.shift(offset)
        vim = vim.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        vip.fillna(kwargs['fillna'], inplace=True)
        vim.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        vip.fillna(method=kwargs['fill_method'], inplace=True)
        vim.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    vip.name = f"VTXP_{length}"
    vim.name = f"VTXM_{length}"
    vip.category = vim.category = 'trend'

    # Prepare DataFrame to return
    data = {vip.name: vip, vim.name: vim}
    vtxdf = pd.DataFrame(data)
    vtxdf.name = f"VTX_{length}"
    vtxdf.category = 'trend'

    return vtxdf



# Trend Documentation
adx.__doc__ = \
"""Average Directional Movement (ADX)

Average Directional Movement is meant to quantify trend strength by measuring
the amount of movement in a single direction.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/average-directional-movement-adx/

Calculation:
    DMI ADX TREND 2.0 by @TraderR0BERT, NETWORTHIE.COM
        //Created by @TraderR0BERT, NETWORTHIE.COM, last updated 01/26/2016
        //DMI Indicator
        //Resolution input option for higher/lower time frames
        study(title="DMI ADX TREND 2.0", shorttitle="ADX TREND 2.0")

        adxlen = input(14, title="ADX Smoothing")
        dilen = input(14, title="DI Length")
        thold = input(20, title="Threshold")

        threshold = thold

        //Script for Indicator
        dirmov(len) =>
            up = change(high)
            down = -change(low)
            truerange = rma(tr, len)
            plus = fixnan(100 * rma(up > down and up > 0 ? up : 0, len) / truerange)
            minus = fixnan(100 * rma(down > up and down > 0 ? down : 0, len) / truerange)
            [plus, minus]

        adx(dilen, adxlen) =>
            [plus, minus] = dirmov(dilen)
            sum = plus + minus
            adx = 100 * rma(abs(plus - minus) / (sum == 0 ? 1 : sum), adxlen)
            [adx, plus, minus]

        [sig, up, down] = adx(dilen, adxlen)
        osob=input(40,title="Exhaustion Level for ADX, default = 40")
        col = sig >= sig[1] ? green : sig <= sig[1] ? red : gray

        //Plot Definitions Current Timeframe
        p1 = plot(sig, color=col, linewidth = 3, title="ADX")
        p2 = plot(sig, color=col, style=circles, linewidth=3, title="ADX")
        p3 = plot(up, color=blue, linewidth = 3, title="+DI")
        p4 = plot(up, color=blue, style=circles, linewidth=3, title="+DI")
        p5 = plot(down, color=fuchsia, linewidth = 3, title="-DI")
        p6 = plot(down, color=fuchsia, style=circles, linewidth=3, title="-DI")
        h1 = plot(threshold, color=black, linewidth =3, title="Threshold")

        trender = (sig >= up or sig >= down) ? 1 : 0
        bgcolor(trender>0?black:gray, transp=85)

        //Alert Function for ADX crossing Threshold
        Up_Cross = crossover(up, threshold)
        alertcondition(Up_Cross, title="DMI+ cross", message="DMI+ Crossing Threshold")
        Down_Cross = crossover(down, threshold)
        alertcondition(Down_Cross, title="DMI- cross", message="DMI- Crossing Threshold")

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 14
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: adx, dmp, dmn columns.
"""


aroon.__doc__ = \
"""Aroon (AROON)

Aroon attempts to identify if a security is trending and how strong.

Sources:
    https://www.tradingview.com/wiki/Aroon
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/aroon-ar/

Calculation:
    Default Inputs:
        length=1
    def maxidx(x):
        return 100 * (int(np.argmax(x)) + 1) / length

    def minidx(x):
        return 100 * (int(np.argmin(x)) + 1) / length

    _close = close.rolling(length, min_periods=min_periods)
    aroon_up = _close.apply(maxidx, raw=True)
    aroon_down = _close.apply(minidx, raw=True)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: aroon_up, aroon_down columns.
"""


decreasing.__doc__ = \
"""Decreasing

Returns True or False if the series is decreasing over a periods.  By default,
it returns True and False as 1 and 0 respectively with kwarg 'asint'.

Sources:

Calculation:
    decreasing = close.diff(length) < 0
    if asint:
        decreasing = decreasing.astype(int)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    asint (bool): Returns as binary.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


dpo.__doc__ = \
"""Detrend Price Oscillator (DPO)

Is an indicator designed to remove trend from price and make it easier to
identify cycles.

Sources:
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:detrended_price_osci

Calculation:
    Default Inputs:
        length=1, centered=True
    SMA = Simple Moving Average
    drift = int(0.5 * length) + 1
    
    DPO = close.shift(drift) - SMA(close, length)
    if centered:
        DPO = DPO.shift(-drift)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    centered (bool): Shift the dpo back by int(0.5 * length) + 1.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


increasing.__doc__ = \
"""Increasing

Returns True or False if the series is increasing over a periods.  By default,
it returns True and False as 1 and 0 respectively with kwarg 'asint'.

Sources:

Calculation:
    increasing = close.diff(length) > 0
    if asint:
        increasing = increasing.astype(int)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    asint (bool): Returns as binary.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


qstick.__doc__ = \
"""Q Stick

The Q Stick indicator, developed by Tushar Chande, attempts to quantify and identify
trends in candlestick charts.

Sources:
    https://library.tradingtechnologies.com/trade/chrt-ti-qstick.html

Calculation:
    Default Inputs:
        length=10
    xMA is one of: sma (default), dema, ema, hma, rma
    qstick = xMA(close - open, length)

Args:
    open (pd.Series): Series of 'open's
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    ma (str): The type of moving average to use.  Default: None, which is 'sma'
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


vortex.__doc__ = \
"""Vortex

Two oscillators that capture positive and negative trend movement.

Sources:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:vortex_indicator

Calculation:
    Default Inputs:
        length=14, drift=1
    TR = True Range
    SMA = Simple Moving Average
    tr = TR(high, low, close)
    tr_sum = tr.rolling(length).sum()

    vmp = (high - low.shift(drift)).abs()
    vmn = (low - high.shift(drift)).abs()

    VIP = vmp.rolling(length).sum() / tr_sum
    VIM = vmn.rolling(length).sum() / tr_sum

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): ROC 1 period.  Default: 14
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: vip and vim columns
"""