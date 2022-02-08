# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.utils import get_offset, verify_series


def ohlc4(
    open_: Series, high: Series, low: Series, close: Series,
    offset: int = None, **kwargs
) -> Series:
    """OHLC4

    OHLC4 is the average of open, high, low and close.

    Args:
        open_ (pd.Series): Series of 'open's
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        offset (int): How many periods to offset the result. Default: 0

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    open_ = verify_series(open_)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)

    # Calculate
    ohlc4 = Series(
        0.25 * (open_.values + high.values + low.values + close.values),
        index=close.index
    )

    # Offset
    if offset != 0:
        ohlc4 = ohlc4.shift(offset)

    # Name and Category
    ohlc4.name = "OHLC4"
    ohlc4.category = "overlap"

    return ohlc4
