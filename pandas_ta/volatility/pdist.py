# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import non_zero_range, v_drift, v_offset, v_series


def pdist(
    open_: Series, high: Series, low: Series, close: Series,
    drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Price Distance (PDIST)

    Measures the "distance" covered by price movements.

    Sources:
        https://www.prorealcode.com/prorealtime-indicators/pricedistance/

    Args:
        open_ (pd.Series): Series of 'opens's
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    open_ = v_series(open_)
    high = v_series(high)
    low = v_series(low)
    close = v_series(close)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    pdist = 2 * non_zero_range(high, low)
    pdist += non_zero_range(open_, close.shift(drift)).abs()
    pdist -= non_zero_range(close, open_).abs()

    # Offset
    if offset != 0:
        pdist = pdist.shift(offset)

    # Fill
    if "fillna" in kwargs:
        pdist.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        pdist.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    pdist.name = "PDIST"
    pdist.category = "volatility"

    return pdist
