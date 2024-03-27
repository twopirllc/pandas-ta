# -*- coding: utf-8 -*-
from numpy import isnan
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.ma import ma
from pandas_ta.statistics import stdev
from pandas_ta.utils import (
    unsigned_differences,
    v_bool,
    v_drift,
    v_mamode,
    v_offset,
    v_pos_default,
    v_series
)



def _rvi(source, length, scalar, mode, drift):
    """RVI"""
    std = stdev(source, length)
    pos, neg = unsigned_differences(source, amount=drift)

    pos_std = pos * std
    neg_std = neg * std

    pos_avg = ma(mode, pos_std, length=length)
    neg_avg = ma(mode, neg_std, length=length)

    result = scalar * pos_avg / (pos_avg + neg_avg)
    return result


def rvi(
    close: Series, high: Series = None, low: Series = None,
    length: Int = None, scalar: IntFloat = None,
    refined: bool = None, thirds: bool = None,
    mamode: str = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Relative Volatility Index (RVI)

    The Relative Volatility Index (RVI) was created in 1993 and revised
    in 1995. Instead of adding up price changes like RSI based on price
    direction, the RVI adds up standard deviations based on price direction.

    Sources:
        https://www.motivewave.com/studies/relative_volatility_index.htm
        https://www.tradingview.com/script/mLZJqxKn-Relative-Volatility-Index/
        https://www.tradingview.com/support/solutions/43000594684-relative-volatility-index/

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): The short period. Default: 14
        scalar (float): A positive float to scale the bands. Default: 100
        refined (bool): Use 'refined' calculation which is the average of
            RVI(high) and RVI(low) instead of RVI(close). Default: False
        thirds (bool): Average of high, low and close. Default: False
        mamode (str): See ``help(ta.ma)``. Default: 'ema'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: lower, basis, upper columns.
    """
    # Validate
    length = v_pos_default(length, 14)
    close = v_series(close, length + 2)

    if close is None:
        return

    scalar = v_pos_default(scalar, 100)
    refined = v_bool(refined, False)
    thirds = v_bool(thirds, False)
    mamode = v_mamode(mamode, "ema")
    drift = v_drift(drift)
    offset = v_offset(offset)

    if refined or thirds:
        high = v_series(high)
        low = v_series(low)

    # Calculate
    _mode = ""
    if refined:
        high_rvi = _rvi(high, length, scalar, mamode, drift)
        low_rvi = _rvi(low, length, scalar, mamode, drift)
        rvi = 0.5 * (high_rvi + low_rvi)
        _mode = "r"
    elif thirds:
        high_rvi = _rvi(high, length, scalar, mamode, drift)
        low_rvi = _rvi(low, length, scalar, mamode, drift)
        close_rvi = _rvi(close, length, scalar, mamode, drift)
        rvi = (high_rvi + low_rvi + close_rvi) / 3.0
        _mode = "t"
    else:
        rvi = _rvi(close, length, scalar, mamode, drift)

    if all(isnan(rvi)):
        return  # Emergency Break

    # Offset
    if offset != 0:
        rvi = rvi.shift(offset)

    # Fill
    if "fillna" in kwargs:
        rvi.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    rvi.name = f"RVI{_mode}_{length}"
    rvi.category = "volatility"

    return rvi
