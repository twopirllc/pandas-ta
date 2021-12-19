# -*- coding: utf-8 -*-
from pandas_ta.utils import get_offset, pascals_triangle, verify_series, weights
from pandas import Series


def pwma(close: Series, length: int = None, asc: bool = None, offset: bool = None, **kwargs) -> Series:
    """Pascal's Weighted Moving Average (PWMA)

    Pascal's Weighted Moving Average is similar to a symmetric triangular window
    except PWMA's weights are based on Pascal's Triangle.

    Source: Kevin Johnson

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period.  Default: 10
        asc (bool): Recent values weigh more. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate Arguments
    length = int(length) if length and length > 0 else 10
    asc = asc if asc else True
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None: return

    # Calculate Result
    triangle = pascals_triangle(n=length - 1, weighted=True)
    pwma = close.rolling(length, min_periods=length).apply(weights(triangle), raw=True)

    # Offset
    if offset != 0:
        pwma = pwma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        pwma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        pwma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    pwma.name = f"PWMA_{length}"
    pwma.category = "overlap"

    return pwma
