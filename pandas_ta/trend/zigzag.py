# -*- coding: utf-8 -*-
# from numpy import isnan, nan, zeros
from numba import njit
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import (
    v_bool,
    v_offset,
    v_pos_default,
    v_series,
)



def zigzag(
    high: Series, low: Series, close: Series = None,
    pivot_leg: int = None, price_deviation: IntFloat = None,
    retrace: bool = None, last_extreme: bool = None,
    offset: Int = None, **kwargs: DictLike
):
    """ Zigzag (ZIGZAG)

    Zigzag attempts to filter out smaller price movments while highlighting
    trend direction. It does not predict future trends, but it does identify
    swing highs and lows. When 'price_deviation' is set to 10, it will ignore
    all price movements less than 10%; only price movements greater than 10%
    would be shown.

    Note: Zigzag lines are not permanent and a price reversal will create a
        new line.

    Sources:
        https://www.tradingview.com/support/solutions/43000591664-zig-zag/#:~:text=Definition,trader%20visual%20the%20price%20action.
        https://school.stockcharts.com/doku.php?id=technical_indicators:zigzag

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's. Default: None
        pivot_leg (int): Number of legs > 2. Default: 10
        price_deviation (float): Price Deviation Percentage for a reversal.
            Default: 5
        retrace (bool): Default: False
        last_extreme (bool): Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: swing, and swing_type (high or low).
    """
    # Validate
    pivot_leg = _length = v_pos_default(pivot_leg, 10)
    high = v_series(high, _length + 1)
    low = v_series(low, _length + 1)

    if high is None or low is None:
        return

    if close is not None:
        close = v_series(close, _length + 1)
        np_close = close.values
        if close is None:
            return

    price_deviation = v_pos_default(price_deviation, 5.0)
    retrace = v_bool(retrace, False)
    last_extreme = v_bool(last_extreme, True)
    offset = v_offset(offset)

    # Calculation
    np_high, np_low = high.values, low.values
    highest_high = high.rolling(window=pivot_leg, center=True, min_periods=0).max()
    lowest_low = low.rolling(window=pivot_leg, center=True, min_periods=0).min()

    # Fix and fill working code

    # Offset
    # if offset != 0:

    # Fill
    # if "fillna" in kwargs:

    # Name and Category
