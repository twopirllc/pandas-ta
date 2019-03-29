# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from .overlap import hlc3, ema, sma, wma
from .statistics import mad
from .utils import get_drift, get_offset, verify_series



def ao(high, low, fast=None, slow=None, offset=None, **kwargs):
    """Indicator: Awesome Oscillator (AO)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    fast = int(fast) if fast and fast > 0 else 5
    slow = int(slow) if slow and slow > 0 else 34
    if slow < fast:
        fast, slow = slow, fast
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else fast
    offset = get_offset(offset)

    # Calculate Result
    median_price = 0.5 * (high + low)
    fast_sma = median_price.rolling(fast, min_periods=min_periods).mean()
    slow_sma = median_price.rolling(slow, min_periods=min_periods).mean()
    ao = fast_sma - slow_sma

    # Offset
    if offset != 0:
        ao = ao.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        ao.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        ao.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    ao.name = f"AO_{fast}_{slow}"
    ao.category = 'momentum'

    return ao


def apo(close, fast=None, slow=None, offset=None, **kwargs):
    """Indicator: Absolute Price Oscillator (APO)"""
    # Validate Arguments
    close = verify_series(close)
    fast = int(fast) if fast and fast > 0 else 12
    slow = int(slow) if slow and slow > 0 else 26
    if slow < fast:
        fast, slow = slow, fast
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else fast
    offset = get_offset(offset)

    # Calculate Result
    fastma = ema(close, length=fast, **kwargs)
    slowma = ema(close, length=slow, **kwargs)
    apo = fastma - slowma

    # Offset
    if offset != 0:
        apo = apo.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        apo.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        apo.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    apo.name = f"APO_{fast}_{slow}"
    apo.category = 'momentum'

    return apo


def bop(open_, high, low, close, offset=None, **kwargs):
    """Indicator: Balance of Power (BOP)"""
    # Validate Arguments
    open_ = verify_series(open_)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)

    # Calculate Result
    close_open_range = close - open_
    high_low_range = high - low
    bop = close_open_range / high_low_range

    # Offset
    if offset != 0:
        bop = bop.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        bop.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        bop.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    bop.name = f"BOP"
    bop.category = 'momentum'

    return bop


def cci(high, low, close, length=None, c=None, offset=None, **kwargs):
    """Indicator: Commodity Channel Index (CCI)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 20
    c = float(c) if c and c > 0 else 0.015
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    typical_price = hlc3(high=high, low=low, close=close)
    mean_typical_price = sma(typical_price, length=length)
    mad_typical_price = mad(typical_price, length=length)

    cci = typical_price - mean_typical_price
    cci /= c * mad_typical_price

    # Offset
    if offset != 0:
        cci = cci.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        cci.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        cci.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    cci.name = f"CCI_{length}_{c}"
    cci.category = 'momentum'

    return cci


def cmo(close, length=None, drift=None, offset=None, **kwargs):
    """Indicator: Chande Momentum Oscillator (CMO)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    negative = close.diff(drift)
    positive = negative.copy()

    positive[positive < 0] = 0  # Make negatives 0 for the postive series
    negative[negative > 0] = 0  # Make postives 0 for the negative series

    pos_sum = positive.rolling(length).sum()
    neg_sum = negative.abs().rolling(length).sum()
    
    cmo = 100 * (pos_sum - neg_sum) / (pos_sum + neg_sum)

    # Offset
    if offset != 0:
        cmo = cmo.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        cmo.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        cmo.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    cmo.name = f"CMO_{length}"
    cmo.category = 'momentum'

    return cmo


def coppock(close, length=None, fast=None, slow=None, offset=None, **kwargs):
    """Indicator: Coppock Curve (COPC)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    fast = int(fast) if fast and fast > 0 else 11
    slow = int(slow) if slow and slow > 0 else 14
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    total_roc = roc(close, fast) + roc(close, slow)
    coppock = wma(total_roc, length)

    # Offset
    if offset != 0:
        coppock = coppock.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        coppock.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        coppock.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    coppock.name = f"COPC_{fast}_{slow}_{length}"
    coppock.category = 'momentum'

    return coppock



def kst(close, roc1=None, roc2=None, roc3=None, roc4=None, sma1=None, sma2=None, sma3=None, sma4=None, signal=None, drift=None, offset=None, **kwargs):
    """Indicator: 'Know Sure Thing'"""
    # Validate arguments
    close = verify_series(close)
    roc1 = int(roc1) if roc1 and roc1 > 0 else 10
    roc2 = int(roc2) if roc2 and roc2 > 0 else 15
    roc3 = int(roc3) if roc3 and roc3 > 0 else 20
    roc4 = int(roc4) if roc4 and roc4 > 0 else 30

    sma1 = int(sma1) if sma1 and sma1 > 0 else 10
    sma2 = int(sma2) if sma2 and sma2 > 0 else 10
    sma3 = int(sma3) if sma3 and sma3 > 0 else 10
    sma4 = int(sma4) if sma4 and sma4 > 0 else 15

    signal = int(signal) if signal and signal > 0 else 9
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    rocma1 = roc(close, roc1).rolling(sma1).mean()
    rocma2 = roc(close, roc2).rolling(sma2).mean()
    rocma3 = roc(close, roc3).rolling(sma3).mean()
    rocma4 = roc(close, roc4).rolling(sma4).mean()

    kst = 100 * (rocma1 + 2 * rocma2 + 3 * rocma3 + 4 * rocma4)
    kst_signal = kst.rolling(signal).mean()

    # Offset
    if offset != 0:
        kst = kst.shift(offset)
        kst_signal = kst_signal.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        kst.fillna(kwargs['fillna'], inplace=True)
        kst_signal.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        kst.fillna(method=kwargs['fill_method'], inplace=True)
        kst_signal.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    kst.name = f"KST_{roc1}_{roc2}_{roc3}_{roc4}_{sma1}_{sma2}_{sma3}_{sma4}"
    kst_signal.name = f"KSTS_{signal}"
    kst.category = kst_signal.category = 'momentum'

    # Prepare DataFrame to return
    data = {kst.name: kst, kst_signal.name: kst_signal}
    kstdf = pd.DataFrame(data)
    kstdf.name = f"KST_{roc1}_{roc2}_{roc3}_{roc4}_{sma1}_{sma2}_{sma3}_{sma4}_{signal}"
    kstdf.category = 'momentum'

    return kstdf


def macd(close, fast=None, slow=None, signal=None, offset=None, **kwargs):
    """Indicator: Moving Average, Convergence/Divergence (MACD)"""
    # Validate arguments
    close = verify_series(close)
    fast = int(fast) if fast and fast > 0 else 12
    slow = int(slow) if slow and slow > 0 else 26
    signal = int(signal) if signal and signal > 0 else 9
    if slow < fast:
        fast, slow = slow, fast
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else fast
    offset = get_offset(offset)

    # Calculate Result
    fastma = ema(close, length=fast, **kwargs)
    slowma = ema(close, length=slow, **kwargs)

    macd = fastma - slowma
    signalma = ema(close=macd, length=signal, **kwargs)
    histogram = macd - signalma

    # Offset
    if offset != 0:
        macd = macd.shift(offset)
        histogram = histogram.shift(offset)
        signalma = signalma.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        macd.fillna(kwargs['fillna'], inplace=True)
        histogram.fillna(kwargs['fillna'], inplace=True)
        signalma.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        macd.fillna(method=kwargs['fill_method'], inplace=True)
        histogram.fillna(method=kwargs['fill_method'], inplace=True)
        signalma.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    macd.name = f"MACD_{fast}_{slow}_{signal}"
    histogram.name = f"MACDH_{fast}_{slow}_{signal}"
    signalma.name = f"MACDS_{fast}_{slow}_{signal}"
    macd.category = histogram.category = signalma.category = 'momentum'

    # Prepare DataFrame to return
    data = {macd.name: macd, histogram.name: histogram, signalma.name: signalma}
    macddf = pd.DataFrame(data)
    macddf.name = f"MACD_{fast}_{slow}_{signal}"
    macddf.category = 'momentum'

    return macddf


def mom(close, length=None, offset=None, **kwargs):
    """Indicator: Momentum (MOM)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    offset = get_offset(offset)

    # Calculate Result
    mom = close.diff(length)

    # Offset
    if offset != 0:
        mom = mom.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        mom.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        mom.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    mom.name = f"MOM_{length}"
    mom.category = 'momentum'

    return mom


def ppo(close, fast=None, slow=None, signal=None, offset=None, **kwargs):
    """Indicator: Percentage Price Oscillator (PPO)"""
    # Validate Arguments
    close = verify_series(close)
    fast = int(fast) if fast and fast > 0 else 12
    slow = int(slow) if slow and slow > 0 else 26
    signal = int(signal) if signal and signal > 0 else 9
    if slow < fast:
        fast, slow = slow, fast
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else fast
    offset = get_offset(offset)

    # Calculate Result
    fastma = close.rolling(fast, min_periods=min_periods).mean()
    slowma = close.rolling(slow, min_periods=min_periods).mean()

    ppo = 100 * (fastma - slowma) / slowma
    signalma = ema(close=ppo, length=signal, **kwargs)
    histogram = ppo - signalma

    # Offset
    if offset != 0:
        ppo = ppo.shift(offset)
        signalma = signalma.shift(offset)
        histogram = histogram.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        ppo.fillna(kwargs['fillna'], inplace=True)
        histogram.fillna(kwargs['fillna'], inplace=True)
        signalma.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        ppo.fillna(method=kwargs['fill_method'], inplace=True)
        histogram.fillna(method=kwargs['fill_method'], inplace=True)
        signalma.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    ppo.name = f"PPO_{fast}_{slow}_{signal}"
    histogram.name = f"PPOH_{fast}_{slow}_{signal}"
    signalma.name = f"PPOS_{fast}_{slow}_{signal}"
    ppo.category = histogram.category = signalma.category = 'momentum'

    # Prepare DataFrame to return
    data = {ppo.name: ppo, histogram.name: histogram, signalma.name: signalma}
    ppodf = pd.DataFrame(data)
    ppodf.name = f"PPO_{fast}_{slow}_{signal}"
    ppodf.category = 'momentum'

    return ppodf


def roc(close, length=None, offset=None, **kwargs):
    """Indicator: Rate of Change (ROC)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    roc = 100 * mom(close=close, length=length) / close.shift(length)

    # Offset
    if offset != 0:
        roc = roc.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        roc.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        roc.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    roc.name = f"ROC_{length}"
    roc.category = 'momentum'

    return roc


def rsi(close, length=None, drift=None, offset=None, **kwargs):
    """Indicator: Relative Strength Index (RSI)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    negative = close.diff(drift)
    positive = negative.copy()

    positive[positive < 0] = 0  # Make negatives 0 for the postive series
    negative[negative > 0] = 0  # Make postives 0 for the negative series

    positive_avg = positive.ewm(com=length, adjust=False).mean()
    negative_avg = negative.ewm(com=length, adjust=False).mean().abs()

    rsi = 100 * positive_avg / (positive_avg + negative_avg)

    # Offset
    if offset != 0:
        rsi = rsi.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        rsi.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        rsi.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    rsi.name = f"RSI_{length}"
    rsi.category = 'momentum'

    return rsi


def stoch(high, low, close, fast_k=None, slow_k=None, slow_d=None, offset=None, **kwargs):
    """Indicator: Stochastic Oscillator (STOCH)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    fast_k = fast_k if fast_k and fast_k > 0 else 14
    slow_k = slow_k if slow_k and slow_k > 0 else 5
    slow_d = slow_d if slow_d and slow_d > 0 else 3
    offset = get_offset(offset)

    # Calculate Result
    lowest_low   =  low.rolling(slow_k).min()
    highest_high = high.rolling(slow_k).max()

    fastk = 100 * (close - lowest_low) / (highest_high - lowest_low)
    fastd = sma(fastk, length=slow_d)

    slowk = sma(fastk, length=slow_k)
    slowd = sma(slowk, length=slow_d)

    # Offset
    if offset != 0:
        fastk = fastk.shift(offset)
        fastd = fastd.shift(offset)
        slowk = slowk.shift(offset)
        slowd = slowd.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        fastk.fillna(kwargs['fillna'], inplace=True)
        fastd.fillna(kwargs['fillna'], inplace=True)
        slowk.fillna(kwargs['fillna'], inplace=True)
        slowd.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        fastk.fillna(method=kwargs['fill_method'], inplace=True)
        fastd.fillna(method=kwargs['fill_method'], inplace=True)
        slowk.fillna(method=kwargs['fill_method'], inplace=True)
        slowd.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    fastk.name = f"STOCHF_{fast_k}"
    fastd.name = f"STOCHF_{slow_d}"
    slowk.name = f"STOCH_{slow_k}"
    slowd.name = f"STOCH_{slow_d}"
    fastk.category = fastd.category = slowk.category = slowd.category = 'momentum'

    # Prepare DataFrame to return
    data = {fastk.name: fastk, fastd.name: fastd, slowk.name: slowk, slowd.name: slowd}
    stochdf = pd.DataFrame(data)
    stochdf.name = f"STOCH_{fast_k}_{slow_k}_{slow_d}"
    stochdf.category = 'momentum'

    return stochdf


def trix(close, length=None, drift=None, offset=None, **kwargs):
    """Indicator: Trix (TRIX)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 30
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    ema1 = ema(close=close, length=length, **kwargs)
    ema2 = ema(close=ema1, length=length, **kwargs)
    ema3 = ema(close=ema2, length=length, **kwargs)
    trix = 100 * ema3.pct_change(drift)

    # Offset
    if offset != 0:
        trix = trix.shift(offset)

    # Name & Category
    trix.name = f"TRIX_{length}"
    trix.category = 'momentum'

    return trix


def tsi(close, fast=None, slow=None, drift=None, offset=None, **kwargs):
    """Indicator: True Strength Index (TSI)"""
    # Validate Arguments
    close = verify_series(close)
    fast = int(fast) if fast and fast > 0 else 13
    slow = int(slow) if slow and slow > 0 else 25
    if slow < fast:
        fast, slow = slow, fast
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    diff = close.diff(drift)
    slow_ema = ema(close=diff, length=slow, **kwargs)
    fast_slow_ema = ema(close=slow_ema, length=fast, **kwargs)

    _ma = ema(close=diff, length=slow, **kwargs)
    ma = ema(close=_ma, length=fast, **kwargs)

    tsi = 100 * fast_slow_ema / ma

    # Offset
    if offset != 0:
        tsi = tsi.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        tsi.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        tsi.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    tsi.name = f"TSI_{fast}_{slow}"
    tsi.category = 'momentum'

    return tsi


def uo(high, low, close, fast=None, medium=None, slow=None, fast_w=None, medium_w=None, slow_w=None, drift=None, offset=None, **kwargs):
    """Indicator: Ultimate Oscillator (UO)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    drift = get_drift(drift)
    offset = get_offset(offset)

    fast = int(fast) if fast and fast > 0 else 7
    fast_w = float(fast_w) if fast_w and fast_w > 0 else 4.0

    medium = int(medium) if medium and medium > 0 else 14
    medium_w = float(medium_w) if medium_w and medium_w > 0 else 2.0

    slow = int(slow) if slow and slow > 0 else 28
    slow_w = float(slow_w) if slow_w and slow_w > 0 else 1.0

    # Calculate Result
    tdf = pd.DataFrame({'high': high, 'low': low, f"close_{drift}": close.shift(drift)})
    max_h_or_pc = tdf.loc[:, ['high', f"close_{drift}"]].max(axis=1)
    min_l_or_pc = tdf.loc[:, ['low', f"close_{drift}"]].min(axis=1)
    del tdf

    bp = close - min_l_or_pc
    tr = max_h_or_pc - min_l_or_pc

    fast_avg = bp.rolling(fast).sum() / tr.rolling(fast).sum()
    medium_avg = bp.rolling(medium).sum() / tr.rolling(medium).sum()
    slow_avg = bp.rolling(slow).sum() / tr.rolling(slow).sum()

    total_weight =  fast_w + medium_w + slow_w
    weights = (fast_w * fast_avg) + (medium_w * medium_avg) + (slow_w * slow_avg)
    uo = 100 * weights / total_weight

    # Offset
    if offset != 0:
        uo = uo.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        uo.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        uo.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    uo.name = f"UO_{fast}_{medium}_{slow}"
    uo.category = 'momentum'

    return uo


def willr(high, low, close, length=None, offset=None, **kwargs):
    """Indicator: William's Percent R (WILLR)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    lowest_low = low.rolling(length, min_periods=min_periods).min()
    highest_high = high.rolling(length, min_periods=min_periods).max()

    willr = 100 * ((close - lowest_low) / (highest_high - lowest_low) - 1)

    # Offset
    if offset != 0:
        willr = willr.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        willr.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        willr.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    willr.name = f"WILLR_{length}"
    willr.category = 'momentum'

    return willr




ao.__doc__ = \
"""Awesome Oscillator (AO)

The Awesome Oscillator is an indicator used to measure a security's momentum.
AO is generally used to affirm trends or to anticipate possible reversals.

Sources:
    https://www.tradingview.com/wiki/Awesome_Oscillator_(AO)
    https://www.ifcm.co.uk/ntx-indicators/awesome-oscillator

Calculation:
    Default Inputs:
        fast=5, slow=34
    SMA = Simple Moving Average
    median = (high + low) / 2
    AO = SMA(median, fast) - SMA(median, slow)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    fast (int): The short period.  Default: 5
    slow (int): The long period.   Default: 34
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


apo.__doc__ = \
"""Absolute Price Oscillator (APO)

The Absolute Price Oscillator is an indicator used to measure a security's
momentum.  It is simply the difference of two Exponential Moving Averages
(EMA) of two different periods.  Note: APO and MACD lines are equivalent.

Sources:
    https://www.investopedia.com/terms/p/ppo.asp

Calculation:
    Default Inputs:
        fast=12, slow=26
    EMA = Exponential Moving Average
    APO = EMA(close, fast) - EMA(close, slow)

Args:
    close (pd.Series): Series of 'close's
    fast (int): The short period.  Default: 12
    slow (int): The long period.   Default: 26
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


bop.__doc__ = \
"""Balance of Power (BOP)

Balance of Power measure the market strength of buyers against sellers.

Sources:
    http://www.worden.com/TeleChartHelp/Content/Indicators/Balance_of_Power.htm

Calculation:
    BOP = (close - open) / (high - low)

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


cci.__doc__ = \
"""Commodity Channel Index (CCI)

Commodity Channel Index is a momentum oscillator used to primarily identify
overbought and oversold levels relative to a mean.

Sources:
    https://www.tradingview.com/wiki/Commodity_Channel_Index_(CCI)

Calculation:
    Default Inputs:
        length=20, c=0.015
    SMA = Simple Moving Average
    MAD = Mean Absolute Deviation
    tp = typical_price = hlc3 = (high + low + close) / 3
    mean_tp = SMA(tp, length)
    mad_tp = MAD(tp, length)
    CCI = (tp - mean_tp) / (c * mad_tp)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 20
    c (float):  Scaling Constant.  Default: 0.015
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


cmo.__doc__ = \
"""Chande Momentum Oscillator (CMO)

Attempts to capture the momentum of an asset with overbought at 50 and
oversold at -50.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/chande-momentum-oscillator-cmo/

Calculation:
    Default Inputs:
        drift=1
    if close.diff(drift) > 0:
        PSUM = SUM(close - prev_close)
    else:
        NSUM = ABS(SUM(close - prev_close))
    CMO = 100 * (PSUM - NSUM) / (PSUM + NSUM)

Args:
    close (pd.Series): Series of 'close's
    drift (int): The short period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


coppock.__doc__ = \
"""Coppock Curve (COPC)

Coppock Curve (originally called the "Trendex Model") is a momentum indicator
is designed for use on a monthly time scale.  Although designed for monthly
use, a daily calculation over the same period can be made, converting the
periods to 294-day and 231-day rate of changes, and a 210-day weighted
moving average.

Sources:
    https://en.wikipedia.org/wiki/Coppock_curve

Calculation:
    Default Inputs:
        length=10, fast=11, slow=14
    SMA = Simple Moving Average
    MAD = Mean Absolute Deviation
    tp = typical_price = hlc3 = (high + low + close) / 3
    mean_tp = SMA(tp, length)
    mad_tp = MAD(tp, length)
    CCI = (tp - mean_tp) / (c * mad_tp)

Args:
    close (pd.Series): Series of 'close's
    length (int): WMA period.  Default: 10
    fast (int): Fast ROC period.  Default: 11
    slow (int): Slow ROC period.  Default: 14
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""



kst.__doc__ = \
"""'Know Sure Thing' (KST)

The 'Know Sure Thing' is a momentum based oscillator and based on ROC.

Sources:
    https://www.tradingview.com/wiki/Know_Sure_Thing_(KST)
    https://www.incrediblecharts.com/indicators/kst.php

Calculation:
    Default Inputs:
        roc1=10, roc2=15, roc3=20, roc4=30,
        sma1=10, sma2=10, sma3=10, sma4=15, signal=9, drift=1
    ROC = Rate of Change
    SMA = Simple Moving Average
    rocsma1 = SMA(ROC(close, roc1), sma1)
    rocsma2 = SMA(ROC(close, roc2), sma2)
    rocsma3 = SMA(ROC(close, roc3), sma3)
    rocsma4 = SMA(ROC(close, roc4), sma4)

    KST = 100 * (rocsma1 + 2 * rocsma2 + 3 * rocsma3 + 4 * rocsma4)
    KST_Signal = SMA(KST, signal)

Args:
    close (pd.Series): Series of 'close's
    roc1 (int): ROC 1 period.  Default: 10
    roc2 (int): ROC 2 period.  Default: 15
    roc3 (int): ROC 3 period.  Default: 20
    roc4 (int): ROC 4 period.  Default: 30
    sma1 (int): SMA 1 period.  Default: 10
    sma2 (int): SMA 2 period.  Default: 10
    sma3 (int): SMA 3 period.  Default: 10
    sma4 (int): SMA 4 period.  Default: 15
    signal (int): It's period.  Default: 9
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: kst and kst_signal columns
"""


macd.__doc__ = \
"""Moving Average Convergence Divergence (MACD)

The MACD is a popular indicator to that is used to identify a security's trend.
While APO and MACD are the same calculation, MACD also returns two more series
called Signal and Histogram.  The Signal is an EMA of MACD and the Histogram is
the difference of MACD and Signal.

Sources:
    https://www.tradingview.com/wiki/MACD_(Moving_Average_Convergence/Divergence)

Calculation:
    Default Inputs:
        fast=12, slow=26, signal=9
    EMA = Exponential Moving Average
    MACD = EMA(close, fast) - EMA(close, slow)
    Signal = EMA(MACD, signal)
    Histogram = MACD - Signal

Args:
    close (pd.Series): Series of 'close's
    fast (int): The short period.  Default: 12
    slow (int): The long period.   Default: 26
    signal (int): The signal period.   Default: 9
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: macd, histogram, signal columns.
"""


mom.__doc__ = \
"""Momentum (MOM)

Momentum is an indicator used to measure a security's speed (or strength) of
movement.  Or simply the change in price.

Sources:
    http://www.onlinetradingconcepts.com/TechnicalAnalysis/Momentum.html

Calculation:
    Default Inputs:
        length=1
    MOM = close.diff(length)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


ppo.__doc__ = \
"""Percentage Price Oscillator (PPO)

The Percentage Price Oscillator is similar to MACD in measuring momentum.

Sources:
    https://www.tradingview.com/wiki/MACD_(Moving_Average_Convergence/Divergence)

Calculation:
    Default Inputs:
        fast=12, slow=26
    SMA = Simple Moving Average
    EMA = Exponential Moving Average
    fast_sma = SMA(close, fast)
    slow_sma = SMA(close, slow)
    PPO = 100 * (fast_sma - slow_sma) / slow_sma
    Signal = EMA(PPO, signal)
    Histogram = PPO - Signal

Args:
    close(pandas.Series): Series of 'close's
    fast(int): The short period.  Default: 12
    slow(int): The long period.   Default: 26
    signal(int): The signal period.   Default: 9
    offset(int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: ppo, histogram, signal columns
"""


roc.__doc__ = \
"""Rate of Change (ROC)

Rate of Change is an indicator is also referred to as Momentum (yeah, confusingly).
It is a pure momentum oscillator that measures the percent change in price with the
previous price 'n' (or length) periods ago.

Sources:
    https://www.tradingview.com/wiki/Rate_of_Change_(ROC)

Calculation:
    Default Inputs:
        length=1
    MOM = Momentum
    ROC = 100 * MOM(close, length) / close.shift(length)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


rsi.__doc__ = \
"""Relative Strength Index (RSI)

The Relative Strength Index is popular momentum oscillator used to measure the
velocity as well as the magnitude of directional price movements.

Sources:
    https://www.tradingview.com/wiki/Relative_Strength_Index_(RSI)

Calculation:
    Default Inputs:
        length=14, drift=1
    ABS = Absolute Value
    EMA = Exponential Moving Average
    positive = close if close.diff(drift) > 0 else 0
    negative = close if close.diff(drift) < 0 else 0
    pos_avg = EMA(positive, length)
    neg_avg = ABS(EMA(negative, length))
    RSI = 100 * pos_avg / (pos_avg + neg_avg)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


stoch.__doc__ = \
"""Stochastic (STOCH)

Stochastic Oscillator is a range bound momentum indicator.  It displays the location
of the close relative to the high-low range over a period.

Sources:
    https://www.tradingview.com/wiki/Stochastic_(STOCH)

Calculation:
    Default Inputs:
        fast_k=14, slow_k=5, slow_d=3
    SMA = Simple Moving Average
    lowest_low   = low for last fast_k periods
    highest_high = high for last fast_k periods

    FASTK = 100 * (close - lowest_low) / (highest_high - lowest_low)
    FASTD = SMA(FASTK, slow_d)

    SLOWK = SMA(FASTK, slow_k)
    SLOWD = SMA(SLOWK, slow_d)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    fast_k (int): The Fast %K period.  Default: 14
    slow_k (int): The Slow %K period.  Default: 5
    slow_d (int): The Slow %D period.  Default: 3
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: fastk, fastd, slowk, slowd columns.
"""

trix.__doc__ = \
"""Trix (TRIX)

TRIX is a momentum oscillator to identify divergences.

Sources:
    https://www.tradingview.com/wiki/TRIX

Calculation:
    Default Inputs:
        length=18, drift=1
    EMA = Exponential Moving Average
    ROC = Rate of Change
    ema1 = EMA(close, length)
    ema2 = EMA(ema1, length)
    ema3 = EMA(ema2, length)
    TRIX = 100 * ROC(ema3, drift)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 18
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


tsi.__doc__ = \
"""True Strength Index (TSI)

The True Strength Index is a momentum indicator used to identify short-term
swings while in the direction of the trend as well as determining overbought
and oversold conditions.

Sources:
    https://www.investopedia.com/terms/t/tsi.asp

Calculation:
    Default Inputs:
        fast=13, slow=25, drift=1
    EMA = Exponential Moving Average
    diff = close.diff(drift)

    slow_ema = EMA(diff, slow)
    fast_slow_ema = EMA(slow_ema, slow)

    abs_diff_slow_ema = absolute_diff_ema = EMA(ABS(diff), slow)
    abema = abs_diff_fast_slow_ema = EMA(abs_diff_slow_ema, fast)

    TSI = 100 * fast_slow_ema / abema

Args:
    close (pd.Series): Series of 'close's
    fast (int): The short period.  Default: 13
    slow (int): The long period.   Default: 25
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


uo.__doc__ = \
"""Ultimate Oscillator (UO)

The Ultimate Oscillator is a momentum indicator over three different
periods.  It attempts to correct false divergence trading signals.

Sources:
    https://www.tradingview.com/wiki/Ultimate_Oscillator_(UO)

Calculation:
    Default Inputs:
        fast=7, medium=14, slow=28,
        fast_w=4.0, medium_w=2.0, slow_w=1.0, drift=1
    min_low_or_pc  = close.shift(drift).combine(low, min)
    max_high_or_pc = close.shift(drift).combine(high, max)

    bp = buying pressure = close - min_low_or_pc
    tr = true range = max_high_or_pc - min_low_or_pc

    fast_avg = SUM(bp, fast) / SUM(tr, fast)
    medium_avg = SUM(bp, medium) / SUM(tr, medium)
    slow_avg = SUM(bp, slow) / SUM(tr, slow)

    total_weight = fast_w + medium_w + slow_w
    weights = (fast_w * fast_avg) + (medium_w * medium_avg) + (slow_w * slow_avg)
    UO = 100 * weights / total_weight

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    fast (int): The Fast %K period.  Default: 7
    medium (int): The Slow %K period.  Default: 14
    slow (int): The Slow %D period.  Default: 28
    fast_w (float): The Fast %K period.  Default: 4.0
    medium_w (float): The Slow %K period.  Default: 2.0
    slow_w (float): The Slow %D period.  Default: 1.0
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


willr.__doc__ = \
"""William's Percent R (WILLR)

William's Percent R is a momentum oscillator similar to the RSI that
attempts to identify overbought and oversold conditions.

Sources:
    https://www.tradingview.com/wiki/Williams_%25R_(%25R)

Calculation:
    Default Inputs:
        length=20
    lowest_low   = low.rolling(length).min()
    highest_high = high.rolling(length).max()

    WILLR = 100 * ((close - lowest_low) / (highest_high - lowest_low) - 1)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 14
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""