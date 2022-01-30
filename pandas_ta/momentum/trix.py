# -*- coding: utf-8 -*-
# from numpy import isnan
from pandas import DataFrame, Series
from pandas_ta.overlap.ema import ema
from pandas_ta.utils import get_drift, get_offset, verify_series


def trix(
    close: Series, length: int = None, signal: int = None,
    scalar: float = None, drift: int = None,
    offset: int = None, **kwargs
) -> Series:
    """Trix (TRIX)

    TRIX is a momentum oscillator to identify divergences.

    Sources:
        https://www.tradingview.com/wiki/TRIX

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 18
        signal (int): It's period. Default: 9
        scalar (float): How much to magnify. Default: 100
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 30
    signal = int(signal) if signal and signal > 0 else 9
    scalar = float(scalar) if scalar else 100
    _length = 3 * length - 2
    close = verify_series(close, _length)
    drift = get_drift(drift)
    offset = get_offset(offset)

    if close is None:
        return

    # Calculate
    ema1 = ema(close=close, length=length, **kwargs)
    # if all(isnan(ema1)): return  # Emergency Break

    ema2 = ema(close=ema1, length=length, **kwargs)
    # if all(isnan(ema2)): return  # Emergency Break

    ema3 = ema(close=ema2, length=length, **kwargs)
    # if all(isnan(ema3)): return  # Emergency Break

    trix = scalar * ema3.pct_change(drift)
    trix_signal = trix.rolling(signal).mean()

    # Offset
    if offset != 0:
        trix = trix.shift(offset)
        trix_signal = trix_signal.shift(offset)

    # Fill
    if "fillna" in kwargs:
        trix.fillna(kwargs["fillna"], inplace=True)
        trix_signal.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        trix.fillna(method=kwargs["fill_method"], inplace=True)
        trix_signal.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    trix.name = f"TRIX_{length}_{signal}"
    trix_signal.name = f"TRIXs_{length}_{signal}"
    trix.category = trix_signal.category = "momentum"

    data = {trix.name: trix, trix_signal.name: trix_signal}
    df = DataFrame(data, index=close.index)
    df.name = f"TRIX_{length}_{signal}"
    df.category = "momentum"

    return df
