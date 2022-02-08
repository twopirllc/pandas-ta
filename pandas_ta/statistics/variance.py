# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.maps import Imports
from pandas_ta.utils import get_offset, verify_series


def variance(
    close: Series, length: int = None,
    ddof: int = None, talib: bool = None,
    offset: int = None, **kwargs
) -> Series:
    """Rolling Variance

    Calculates the Variance over a rolling period.

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 30
        ddof (int): Delta Degrees of Freedom.
                    The divisor used in calculations is N - ddof,
                    where N represents the number of elements.
                    The 'talib' argument must be false for 'ddof' to work.
                    Default: 1
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Note: TA Lib does not have a 'ddof' argument.
            Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if isinstance(length, int) and length > 1 else 30
    ddof = int(ddof) if isinstance(ddof, int) and ddof >= 0 and ddof < length else 1
    if "min_periods" in kwargs and kwargs["min_periods"] is not None:
        min_periods = int(kwargs["min_periods"])
    else:
        min_periods = length
    close = verify_series(close, max(length, min_periods))
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if close is None:
        return

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import VAR
        variance = VAR(close, length)
    else:
        variance = close.rolling(length, min_periods=min_periods).var(ddof)

    # Offset
    if offset != 0:
        variance = variance.shift(offset)

    # Fill
    if "fillna" in kwargs:
        variance.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        variance.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    variance.name = f"VAR_{length}"
    variance.category = "statistics"

    return variance
