# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from .momentum import roc
from .overlap import *
from .utils import get_drift, get_offset, signed_series, verify_series


def ad(high, low, close, volume, open_=None, offset=None, **kwargs):
    """Indicator: Accumulation/Distribution (AD)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    volume = verify_series(volume)
    offset = get_offset(offset)

    # Calculate Result
    if open_ is not None:
        open_ = verify_series(open_)
        ad = close - open_  # AD with Open
    else:                
        ad = 2 * close - high - low  # AD with High, Low, Close

    hl_range = high - low
    ad *= volume / hl_range
    ad = ad.cumsum()

    # Offset
    if offset != 0:
        ad = ad.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        ad.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        ad.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    ad.name = f"AD"
    ad.category = 'volume'

    return ad


def adosc(high, low, close, volume, open_=None, fast=None, slow=None, offset=None, **kwargs):
    """Indicator: Accumulation/Distribution Oscillator"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    volume = verify_series(volume)
    fast = int(fast) if fast and fast > 0 else 12
    slow = int(slow) if slow and slow > 0 else 26
    if slow < fast:
        fast, slow = slow, fast
    offset = get_offset(offset)

    # Calculate Result
    ad_ = ad(high=high, low=low, close=close, volume=volume, open_=open_)
    fast_ad = ema(close=ad_, length=fast, **kwargs)
    slow_ad = ema(close=ad_, length=slow, **kwargs)
    adosc = fast_ad - slow_ad

    # Offset
    if offset != 0:
        adosc = adosc.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        adosc.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        adosc.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    adosc.name = f"ADOSC_{fast}_{slow}"
    adosc.category = 'volume'

    return adosc


def cmf(high, low, close, volume, open_=None, length=None, offset=None, **kwargs):
    """Indicator: Chaikin Money Flow (CMF)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    volume = verify_series(volume)
    length = int(length) if length and length > 0 else 20
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    if open_ is not None:
        open_ = verify_series(open_)
        ad = close - open_  # AD with Open
    else:                
        ad = 2 * close - high - low  # AD with High, Low, Close

    hl_range = high - low
    ad *= volume / hl_range
    cmf = ad.rolling(length, min_periods=min_periods).sum() / volume.rolling(length, min_periods=min_periods).sum()

    # Offset
    if offset != 0:
        cmf = cmf.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        cmf.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        cmf.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    cmf.name = f"CMF_{length}"
    cmf.category = 'volume'

    return cmf


def efi(close, volume, length=None, drift=None, mamode=None, offset=None, **kwargs):
    """Indicator: Elder's Force Index (EFI)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    length = int(length) if length and length > 0 else 13
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    drift = get_drift(drift)
    mamode = mamode.lower() if mamode else None
    offset = get_offset(offset)

    # Calculate Result
    pv_diff = close.diff(drift) * volume

    if mamode == 'sma':
        efi = pv_diff.rolling(length, min_periods=min_periods).mean()
    else:
        efi = pv_diff.ewm(span=length, min_periods=min_periods).mean()

    # Offset
    if offset != 0:
        efi = efi.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        efi.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        efi.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    efi.name = f"EFI_{length}"
    efi.category = 'volume'

    return efi


def eom(high, low, close, volume, length=None, divisor=None, drift=None, offset=None, **kwargs):
    """Indicator: Ease of Movement (EOM)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    volume = verify_series(volume)
    length = int(length) if length and length > 0 else 14
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    divisor = divisor if divisor and divisor > 0 else 100000000
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    hl_range = high - low
    distance = hl2(high=high, low=low) - hl2(high=high.shift(drift), low=low.shift(drift))
    box_ratio = (volume / divisor) / hl_range
    eom = distance / box_ratio
    eom = eom.rolling(length, min_periods=min_periods).mean()

    # Offset
    if offset != 0:
        eom = eom.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        eom.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        eom.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    eom.name = f"EOM_{length}_{divisor}"
    eom.category = 'volume'

    return eom


def mfi(high, low, close, volume, length=None, drift=None, offset=None, **kwargs):
    """Indicator: Money Flow Index (MFI)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    volume = verify_series(volume)
    length = int(length) if length and length > 0 else 14
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    typical_price = hlc3(high=high, low=low, close=close)
    raw_money_flow = typical_price * volume

    tdf = pd.DataFrame({'diff': 0, 'rmf': raw_money_flow, '+mf': 0, '-mf': 0})

    tdf.loc[(typical_price.diff(drift) > 0), 'diff'] =  1
    tdf.loc[tdf['diff'] ==  1, '+mf'] = raw_money_flow

    tdf.loc[(typical_price.diff(drift) < 0), 'diff'] = -1
    tdf.loc[tdf['diff'] == -1, '-mf'] = raw_money_flow

    psum = tdf['+mf'].rolling(length).sum()
    nsum = tdf['-mf'].rolling(length).sum()
    tdf['mr'] = psum / nsum
    mfi = 100 * psum / (psum + nsum)
    tdf['mfi'] = mfi

    # Offset
    if offset != 0:
        mfi = mfi.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        mfi.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        mfi.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    mfi.name = f"MFI_{length}"
    mfi.category = 'volume'

    return mfi


def nvi(close, volume, length=None, initial=None, offset=None, **kwargs):
    """Indicator: Negative Volume Index (NVI)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    length = int(length) if length and length > 0 else 1
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    initial = int(initial) if initial and initial > 0 else 1000
    offset = get_offset(offset)

    # Calculate Result
    roc_ = roc(close=close, length=length)
    signed_volume = signed_series(volume, initial=1)
    nvi = signed_volume[signed_volume < 0].abs() * roc_
    nvi.fillna(0, inplace=True)
    nvi.iloc[0]= initial
    nvi = nvi.cumsum()

    # Offset
    if offset != 0:
        nvi = nvi.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        nvi.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        nvi.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    nvi.name = f"NVI_{length}"
    nvi.category = 'volume'

    return nvi


def obv(close, volume, offset=None, **kwargs):
    """Indicator: On Balance Volume (OBV)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    offset = get_offset(offset)

    # Calculate Result
    signed_volume = signed_series(close, initial=1) * volume
    obv = signed_volume.cumsum()

    # Offset
    if offset != 0:
        obv = obv.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        obv.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        obv.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    obv.name = f"OBV"
    obv.category = 'volume'

    return obv


def pvi(close, volume, length=None, initial=None, offset=None, **kwargs):
    """Indicator: Positive Volume Index (PVI)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    length = int(length) if length and length > 0 else 1
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    initial = int(initial) if initial and initial > 0 else 1000
    offset = get_offset(offset)

    # Calculate Result
    roc_ = roc(close=close, length=length)
    signed_volume = signed_series(volume, initial=1)
    pvi = signed_volume[signed_volume > 0].abs() * roc_
    pvi.fillna(0, inplace=True)
    pvi.iloc[0]= initial
    pvi = pvi.cumsum()

    # Offset
    if offset != 0:
        pvi = pvi.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        pvi.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        pvi.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    pvi.name = f"PVI_{length}"
    pvi.category = 'volume'

    return pvi


def pvol(close, volume, offset=None, **kwargs):
    """Indicator: Price-Volume (PVOL)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    offset = get_offset(offset)
    signed = kwargs.pop('signed', False)

    # Calculate Result
    if signed:
        pvol = signed_series(close, 1) * close * volume
    else:
        pvol = close * volume

    # Offset
    if offset != 0:
        pvol = pvol.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        pvol.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        pvol.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    pvol.name = f"PVOL"
    pvol.category = 'volume'

    return pvol


def pvt(close, volume, drift=None, offset=None, **kwargs):
    """Indicator: Price-Volume Trend (PVT)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    pv = roc(close=close, length=drift) * volume
    pvt = pv.cumsum()

    # Offset
    if offset != 0:
        pvt = pvt.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        pvt.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        pvt.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    pvt.name = f"PVT"
    pvt.category = 'volume'

    return pvt


def vp(close, volume, width=None, **kwargs):
    """Indicator: Volume Profile (VP)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    width = int(width) if width and width > 0 else 10
    sort_close = kwargs.pop('sort_close', False)

    # Setup
    signed_volume = signed_series(volume, initial=1)
    pos_volume = signed_volume[signed_volume > 0] * volume
    neg_volume = signed_volume[signed_volume < 0] * -volume
    vp = pd.concat([close, pos_volume, neg_volume], axis=1)

    close_col = f"{vp.columns[0]}"
    high_price_col = f"high_{close_col}"
    low_price_col = f"low_{close_col}"
    mean_price_col = f"mean_{close_col}"
    mid_price_col = f"mid_{close_col}"

    volume_col = f"{vp.columns[1]}"
    pos_volume_col = f"pos_{volume_col}"
    neg_volume_col = f"neg_{volume_col}"
    total_volume_col = f"total_{volume_col}"
    vp.columns = [close_col, pos_volume_col, neg_volume_col]

    # sort_close: Sort by close before splitting into ranges. Default: False
    # If False, it sorts by date index or chronological versus by price
    if sort_close:
        vp.sort_values(by=[close_col], inplace=True)

    # Calculate Result
    vp_ranges = np.array_split(vp, width)
    result = ({
        low_price_col: r[close_col].min(),
        mean_price_col: r[close_col].mean(),
        high_price_col: r[close_col].max(),
        pos_volume_col: r[pos_volume_col].sum(),
        neg_volume_col: r[neg_volume_col].sum(),
    } for r in vp_ranges)
    vpdf = pd.DataFrame(result)
    vpdf[total_volume_col] = vpdf[pos_volume_col] + vpdf[neg_volume_col]

    # Handle fills
    if 'fillna' in kwargs:
        vpdf.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        vpdf.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    vpdf.name = f"VP_{width}"
    vpdf.category = 'volume'

    return vpdf



# Volume Documentation
ad.__doc__ = \
"""Accumulation/Distribution (AD)

Accumulation/Distribution indicator utilizes the relative position
of the close to it's High-Low range with volume.  Then it is cumulated.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/accumulationdistribution-ad/

Calculation:
    CUM = Cumulative Sum
    if 'open':
        AD = close - open
    else:
        AD = 2 * close - high - low

    hl_range = high - low
    AD = AD * volume / hl_range
    AD = CUM(AD)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    open (pd.Series): Series of 'open's
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


adosc.__doc__ = \
"""Accumulation/Distribution Oscillator or Chaikin Oscillator

Accumulation/Distribution Oscillator indicator utilizes 
Accumulation/Distribution and treats it similarily to MACD
or APO.

Sources:
    https://www.investopedia.com/articles/active-trading/031914/understanding-chaikin-oscillator.asp

Calculation:
    Default Inputs:
        fast=12, slow=26
    AD = Accum/Dist
    ad = AD(high, low, close, open)
    fast_ad = EMA(ad, fast)
    slow_ad = EMA(ad, slow)
    ADOSC = fast_ad - slow_ad

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    open (pd.Series): Series of 'open's
    volume (pd.Series): Series of 'volume's
    fast (int): The short period.  Default: 12
    slow (int): The long period.   Default: 26
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


cmf.__doc__ = \
"""Chaikin Money Flow (CMF)

Chailin Money Flow measures the amount of money flow volume over a specific
period in conjunction with Accumulation/Distribution.

Sources:
    https://www.tradingview.com/wiki/Chaikin_Money_Flow_(CMF)
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chaikin_money_flow_cmf

Calculation:
    Default Inputs:
        length=20
    if 'open':
        ad = close - open
    else:
        ad = 2 * close - high - low
    
    hl_range = high - low
    ad = ad * volume / hl_range
    CMF = SUM(ad, length) / SUM(volume, length)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    open (pd.Series): Series of 'open's
    volume (pd.Series): Series of 'volume's
    length (int): The short period.  Default: 20
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


efi.__doc__ = \
"""Elder's Force Index (EFI)

Elder's Force Index measures the power behind a price movement using price
and volume as well as potential reversals and price corrections.

Sources:
    https://www.tradingview.com/wiki/Elder%27s_Force_Index_(EFI)
    https://www.motivewave.com/studies/elders_force_index.htm

Calculation:
    Default Inputs:
        length=20, drift=1, mamode=None
    EMA = Exponential Moving Average
    SMA = Simple Moving Average

    pv_diff = close.diff(drift) * volume
    if mamode == 'sma':
        EFI = SMA(pv_diff, length)
    else:
        EFI = EMA(pv_diff, length)

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    length (int): The short period.  Default: 13
    drift (int): The diff period.   Default: 1
    mamode (str): Two options: None or 'sma'.  Default: None
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


eom.__doc__ = \
"""Ease of Movement (EOM)

Ease of Movement is a volume based oscillator that is designed to measure the
relationship between price and volume flucuating across a zero line.

Sources:
    https://www.tradingview.com/wiki/Ease_of_Movement_(EOM)
    https://www.motivewave.com/studies/ease_of_movement.htm
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ease_of_movement_emv

Calculation:
    Default Inputs:
        length=14, divisor=100000000, drift=1
    SMA = Simple Moving Average    
    hl_range = high - low
    distance = 0.5 * (high - high.shift(drift) + low - low.shift(drift))
    box_ratio = (volume / divisor) / hl_range
    eom = distance / box_ratio
    EOM = SMA(eom, length)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    length (int): The short period.  Default: 14
    drift (int): The diff period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


mfi.__doc__ = \
"""Money Flow Index (MFI)

Money Flow Index is an oscillator indicator that is used to measure buying and
selling pressure by utilizing both price and volume.

Sources:
    https://www.tradingview.com/wiki/Money_Flow_(MFI)

Calculation:
    Default Inputs:
        length=14, drift=1
    tp = typical_price = hlc3 = (high + low + close) / 3
    rmf = raw_money_flow = tp * volume

    pmf = pos_money_flow = SUM(rmf, length) if tp.diff(drift) > 0 else 0
    nmf = neg_money_flow = SUM(rmf, length) if tp.diff(drift) < 0 else 0

    MFR = money_flow_ratio = pmf / nmf
    MFI = money_flow_index = 100 * pmf / (pmf + nmf)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    length (int): The sum period.  Default: 14
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


nvi.__doc__ = \
"""Negative Volume Index (NVI)

The Negative Volume Index is a cumulative indicator that uses volume change in
an attempt to identify where smart money is active.

Sources:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:negative_volume_inde
    https://www.motivewave.com/studies/negative_volume_index.htm

Calculation:
    Default Inputs:
        length=1, initial=1000
    ROC = Rate of Change

    roc = ROC(close, length)
    signed_volume = signed_series(volume, initial=1)
    nvi = signed_volume[signed_volume < 0].abs() * roc_
    nvi.fillna(0, inplace=True)
    nvi.iloc[0]= initial
    nvi = nvi.cumsum()

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    length (int): The short period.  Default: 13
    initial (int): The short period.  Default: 1000
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


obv.__doc__ = \
"""On Balance Volume (OBV)

On Balance Volume is a cumulative indicator to measure buying and selling
pressure.

Sources:
    https://www.tradingview.com/wiki/On_Balance_Volume_(OBV)
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/on-balance-volume-obv/
    https://www.motivewave.com/studies/on_balance_volume.htm

Calculation:
    signed_volume = signed_series(close, initial=1) * volume
    obv = signed_volume.cumsum()

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


pvi.__doc__ = \
"""Positive Volume Index (PVI)

The Positive Volume Index is a cumulative indicator that uses volume change in
an attempt to identify where smart money is active.  Used in conjunction with NVI.

Sources:
    https://www.investopedia.com/terms/p/pvi.asp

Calculation:
    Default Inputs:
        length=1, initial=1000
    ROC = Rate of Change

    roc = ROC(close, length)
    signed_volume = signed_series(volume, initial=1)
    pvi = signed_volume[signed_volume > 0].abs() * roc_
    pvi.fillna(0, inplace=True)
    pvi.iloc[0]= initial
    pvi = pvi.cumsum()

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    length (int): The short period.  Default: 13
    initial (int): The short period.  Default: 1000
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


pvol.__doc__ = \
"""Price-Volume (PVOL)

Returns a series of the product of price and volume.

Calculation:
    if signed:
        pvol = signed_series(close, 1) * close * volume
    else:
        pvol = close * volume

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    signed (bool): Keeps the sign of the difference in 'close's.  Default: True
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


pvt.__doc__ = \
"""Price-Volume Trend (PVT)

The Price-Volume Trend utilizes the Rate of Change with volume to
and it's cumulative values to determine money flow.

Sources:
    https://www.tradingview.com/wiki/Price_Volume_Trend_(PVT)

Calculation:
    Default Inputs:
        drift=1
    ROC = Rate of Change
    pv = ROC(close, drift) * volume
    PVT = pv.cumsum()

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    drift (int): The diff period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""

vp.__doc__ = \
"""Volume Profile (VP)

Calculates the Volume Profile by slicing price into ranges.  Note: Value Area is not calculated.

Sources:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:volume_by_price
    https://www.tradingview.com/wiki/Volume_Profile
    http://www.ranchodinero.com/volume-tpo-essentials/
    https://www.tradingtechnologies.com/blog/2013/05/15/volume-at-price/

Calculation:
    Default Inputs:
        width=10
    
    vp = pd.concat([close, pos_volume, neg_volume], axis=1)
    vp_ranges = np.array_split(vp, width)
    result = ({high_close, low_close, mean_close, neg_volume, pos_volume} foreach range in vp_ranges)
    vpdf = pd.DataFrame(result)
    vpdf['total_volume'] = vpdf['pos_volume'] + vpdf['neg_volume']

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    width (int): How many ranges to distrubute price into.  Default: 10

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method
    sort_close (value, optional): Whether to sort by close before splitting into ranges.  Default: False

Returns:
    pd.DataFrame: New feature generated.
"""