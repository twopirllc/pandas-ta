# -*- coding: utf-8 -*-
from pandas_ta.utils import get_offset, verify_series


def ohlc4(open_, high, low, close, offset=None, **kwargs):
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
    # Validate Arguments
    open_ = verify_series(open_)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)

    # Calculate Result
    ohlc4 = 0.25 * (open_ + high + low + close)

    # Offset
    if offset != 0:
        ohlc4 = ohlc4.shift(offset)

    # Name & Category
    ohlc4.name = "OHLC4"
    ohlc4.category = "overlap"

    return ohlc4
