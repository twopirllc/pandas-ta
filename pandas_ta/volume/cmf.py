# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import non_zero_range, v_offset, v_pos_default, v_series



def cmf(
    high: Series, low: Series, close: Series, volume: Series,
    open_: Series = None, length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Chaikin Money Flow (CMF)

    Chaikin Money Flow measures the amount of money flow volume over a
    specific period in conjunction with Accumulation/Distribution.

    Sources:
        https://www.tradingview.com/wiki/Chaikin_Money_Flow_(CMF)
        https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chaikin_money_flow_cmf

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        open_ (pd.Series): Series of 'open's. Default: None
        length (int): The short period. Default: 20
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 20)
    if "min_periods" in kwargs and kwargs["min_periods"] is not None:
        min_periods = int(kwargs["min_periods"])
    else:
        min_periods = length
    _length = max(length, min_periods)
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)
    volume = v_series(volume, _length)

    if high is None or low is None or close is None or volume is None:
        return

    offset = v_offset(offset)

    # Calculate
    if open_ is not None:
        open_ = v_series(open_)
        ad = non_zero_range(close, open_)  # AD with Open
    else:
        ad = 2 * close - (high + low)  # AD with High, Low, Close

    ad *= volume / non_zero_range(high, low)
    cmf = ad.rolling(length, min_periods=min_periods).sum() \
        / volume.rolling(length, min_periods=min_periods).sum()

    # Offset
    if offset != 0:
        cmf = cmf.shift(offset)

    # Fill
    if "fillna" in kwargs:
        cmf.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    cmf.name = f"CMF_{length}"
    cmf.category = "volume"

    return cmf
