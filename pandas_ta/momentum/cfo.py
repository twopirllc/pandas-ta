# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.overlap import linreg
from pandas_ta.utils import get_drift, get_offset, verify_series


def cfo(
    close: Series, length: int = None,
    scalar: float = None, drift: int = None,
    offset: int = None, **kwargs
) -> Series:
    """Chande Forcast Oscillator (CFO)

    The Forecast Oscillator calculates the percentage difference between
    the actual price and the Time Series Forecast (the endpoint of a
    linear regression line).

    Sources:
        https://www.fmlabs.com/reference/default.htm?url=ForecastOscillator.htm

    Args:
        close (pd.Series): Series of 'close's
        length (int): The period. Default: 9
        scalar (float): How much to magnify. Default: 100
        drift (int): The short period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 9
    scalar = float(scalar) if scalar else 100
    close = verify_series(close, length)
    drift = get_drift(drift)
    offset = get_offset(offset)

    if close is None:
        return

    # Calculate
    # Finding linear regression of Series
    cfo = scalar * (close - linreg(close, length=length, tsf=True))
    cfo /= close

    # Offset
    if offset != 0:
        cfo = cfo.shift(offset)

    # Fill
    if "fillna" in kwargs:
        cfo.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        cfo.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    cfo.name = f"CFO_{length}"
    cfo.category = "momentum"

    return cfo
