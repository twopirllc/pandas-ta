# -*- coding: utf-8 -*-
from numpy import where as npWhere
from pandas import DataFrame
from pandas_ta.overlap import hlc3, ma
from pandas_ta.utils import get_drift, get_offset, non_zero_range, verify_series


def kvo(high, low, close, volume, fast=None, slow=None, length_sig=None, mamode=None, drift=None, offset=None, **kwargs):
    """Indicator: Klinger Volume Oscillator (KVO)"""
    # Validate arguments
    fast = int(fast) if fast and fast > 0 else 34
    slow = int(slow) if slow and slow > 0 else 55
    length_sig = int(length_sig) if length_sig and length_sig > 0 else 13
    mamode = mamode.lower() if mamode and isinstance(mamode, str) else "ema"
    _length = max(fast, slow, length_sig)
    high = verify_series(high, _length)
    low = verify_series(low, _length)
    close = verify_series(close, _length)
    volume = verify_series(volume, _length)
    drift = get_drift(drift)
    offset = get_offset(offset)

    if high is None or low is None or close is None or volume is None: return

    # Calculate Result
    mom = hlc3(high, low, close).diff(drift)
    trend = npWhere(mom > 0, 1, 0) + npWhere(mom < 0, -1, 0)
    dm = non_zero_range(high, low)

    m = high.size
    cm = [0] * m
    for i in range(1, m):
        cm[i] = (cm[i - 1] + dm[i]) if trend[i] == trend[i - 1] else (dm[i - 1] + dm[i])

    vf = 100 * volume * trend * abs(2 * dm / cm - 1)

    kvo = ma(mamode, vf, length=fast) - ma(mamode, vf, length=slow)
    kvo_signal = ma(mamode, kvo, length=length_sig)

    # Offset
    if offset != 0:
        kvo = kvo.shift(offset)
        kvo_signal = kvo_signal.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        kvo.fillna(kwargs["fillna"], inplace=True)
        kvo_signal.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        kvo.fillna(method=kwargs["fill_method"], inplace=True)
        kvo_signal.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    kvo.name = f"KVO_{fast}_{slow}"
    kvo_signal.name = f"KVOSig_{length_sig}"
    kvo.category = kvo_signal.category = "volume"

    # Prepare DataFrame to return
    data = {kvo.name: kvo, kvo_signal.name: kvo_signal}
    kvoandsig = DataFrame(data)
    kvoandsig.name = f"KVO_{fast}_{slow}_{length_sig}"
    kvoandsig.category = kvo.category

    return kvoandsig


kvo.__doc__ = \
"""Klinger Volume Oscillator (KVO)

This indicator was developed by Stephen J. Klinger. It is designed to predict
price reversals in a market by comparing volume to price.

Sources:
    https://www.tradingview.com/script/Qnn7ymRK-Klinger-Volume-Oscillator/
    https://www.daytrading.com/klinger-volume-oscillator

Calculation:
    Default Inputs:
        fast=34, slow=55, length_sig=13, drift=1
    MOM = HLC3.diff(drift)
    NEG_TREND = -1 if MOM < 0 else 0
    POS_TREND =  1 if MOM > 0 else 0
    TREND = POS_TREND + NEG_TREND
    DM = high - low
    CM = [CMt-1 + DMt if TRENDt == TRENDt-1 else DMt-1 + DMt]

    vf = 100 * volume * TREND * abs(2 * dm / cm - 1)
    kvo = ema(vf, fast) - ema(vf, slow)
    kvo_signal = ema(kvo, length_sig)


Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    fast (int): The fast period. Default: 34
    long (int): The long period. Default: 55
    length_sig (int): The signal period. Default: 13
    mamode (str): "sma", "ema", "wma" or "rma". Default: "ema"
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: kvo and kvo_signal columns.
"""
