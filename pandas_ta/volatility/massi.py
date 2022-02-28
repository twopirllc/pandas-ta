# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.overlap import ema
from pandas_ta.utils import non_zero_range, v_offset, v_pos_default, v_series


def massi(
    high: Series, low: Series, fast: Int = None, slow: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Mass Index (MASSI)

    The Mass Index is a non-directional volatility indicator that
    utilitizes the High-Low Range to identify trend reversals based on
    range expansions.

    Sources:
        https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:mass_index

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        fast (int): The short period. Default: 9
        slow (int): The long period. Default: 25
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    fast = v_pos_default(fast, 9)
    slow = v_pos_default(slow, 25)
    if slow < fast:
        fast, slow = slow, fast
    _length = max(fast, slow)
    high = v_series(high, _length)
    low = v_series(low, _length)

    if high is None or low is None:
        return

    offset = v_offset(offset)
    if "length" in kwargs:
        kwargs.pop("length")

    # Calculate
    high_low_range = non_zero_range(high, low)
    hl_ema1 = ema(close=high_low_range, length=fast, **kwargs)
    hl_ema2 = ema(close=hl_ema1, length=fast, **kwargs)

    hl_ratio = hl_ema1 / hl_ema2
    massi = hl_ratio.rolling(slow, min_periods=slow).sum()

    # Offset
    if offset != 0:
        massi = massi.shift(offset)

    # Fill
    if "fillna" in kwargs:
        massi.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        massi.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    massi.name = f"MASSI_{fast}_{slow}"
    massi.category = "volatility"

    return massi
