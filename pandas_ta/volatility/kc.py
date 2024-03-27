# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.ma import ma
from pandas_ta.utils import (
    high_low_range,
    v_bool,
    v_mamode,
    v_offset,
    v_pos_default,
    v_series
)
from .true_range import true_range



def kc(
    high: Series, low: Series, close: Series,
    length: Int = None, scalar: IntFloat = None,
    tr: bool = None, mamode: str = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Keltner Channels (KC)

    A popular volatility indicator similar to Bollinger Bands and
    Donchian Channels.

    Sources:
        https://www.tradingview.com/wiki/Keltner_Channels_(KC)

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): The short period.  Default: 20
        scalar (float): A positive float to scale the bands. Default: 2
        mamode (str): See ``help(ta.ma)``. Default: 'ema'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        tr (bool): When True, it uses True Range for calculation.
            When False, use a high - low as it's range calculation.
            Default: True
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: lower, basis, upper columns.
    """
    # Validate
    length = v_pos_default(length, 20)
    _length = length + 1
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return

    scalar = v_pos_default(scalar, 2)
    tr = v_bool(tr, True)
    mamode = v_mamode(mamode, "ema")
    offset = v_offset(offset)

    # Calculate
    range_ = true_range(high, low, close) if tr else high_low_range(high, low)
    basis = ma(mamode, close, length=length)
    band = ma(mamode, range_, length=length)

    lower = basis - scalar * band
    upper = basis + scalar * band

    # Offset
    if offset != 0:
        lower = lower.shift(offset)
        basis = basis.shift(offset)
        upper = upper.shift(offset)

    # Fill
    if "fillna" in kwargs:
        lower.fillna(kwargs["fillna"], inplace=True)
        basis.fillna(kwargs["fillna"], inplace=True)
        upper.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"{mamode.lower()[0] if len(mamode) else ''}_{length}_{scalar}"
    lower.name = f"KCL{_props}"
    basis.name = f"KCB{_props}"
    upper.name = f"KCU{_props}"
    basis.category = upper.category = lower.category = "volatility"

    data = {lower.name: lower, basis.name: basis, upper.name: upper}
    df = DataFrame(data, index=close.index)
    df.name = f"KC{_props}"
    df.category = basis.category

    return df
