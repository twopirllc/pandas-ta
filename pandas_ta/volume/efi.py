# -*- coding: utf-8 -*-
from ..utils import get_drift, get_offset, verify_series

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