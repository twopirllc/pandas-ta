# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.ma import ma
from pandas_ta.utils import get_drift, get_offset, verify_series


def efi(
        close: Series, volume: Series, length: int = None,
        mamode: str = None, drift: int = None,
        offset: int = None, **kwargs
    ) -> Series:
    """Elder's Force Index (EFI)

    Elder's Force Index measures the power behind a price movement using price
    and volume as well as potential reversals and price corrections.

    Sources:
        https://www.tradingview.com/wiki/Elder%27s_Force_Index_(EFI)
        https://www.motivewave.com/studies/elders_force_index.htm

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        length (int): The short period. Default: 13
        drift (int): The diff period. Default: 1
        mamode (str): See ```help(ta.ma)```. Default: 'ema'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 13
    mamode = mamode if isinstance(mamode, str) else "ema"
    close = verify_series(close, length)
    volume = verify_series(volume, length)
    drift = get_drift(drift)
    offset = get_offset(offset)

    if close is None or volume is None: return

    # Calculate
    pv_diff = close.diff(drift) * volume
    efi = ma(mamode, pv_diff, length=length)

    # Offset
    if offset != 0:
        efi = efi.shift(offset)

    # Fill
    if "fillna" in kwargs:
        efi.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        efi.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    efi.name = f"EFI_{length}"
    efi.category = "volume"

    return efi
