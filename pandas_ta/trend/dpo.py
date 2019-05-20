# -*- coding: utf-8 -*-
from ..utils import get_offset, verify_series

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