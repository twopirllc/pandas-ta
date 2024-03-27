# -*- coding: utf-8 -*-
from numpy import isnan
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.overlap import linreg
from pandas_ta.utils import (
    v_bool,
    v_drift,
    v_mamode,
    v_offset,
    v_pos_default,
    v_scalar,
    v_series
)
from pandas_ta.volatility import rvi



def inertia(
    close: Series, high: Series = None, low: Series = None,
    length: Int = None, rvi_length: Int = None, scalar: IntFloat = None,
    refined: bool = None, thirds: bool = None,
    drift: Int = None, mamode: str = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Inertia (INERTIA)

    Inertia was developed by Donald Dorsey and was introduced his article
    in September, 1995. It is the Relative Vigor Index smoothed by the Least
    Squares Moving Average. Positive Inertia when values are greater than 50,
    Negative Inertia otherwise.

    Sources:
        https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=285&Name=Inertia
        https://www.tradingview.com/script/mLZJqxKn-Relative-Volatility-Index/

    Args:
        open_ (pd.Series): Series of 'open's
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 20
        rvi_length (int): RVI period. Default: 14
        refined (bool): Use 'refined' calculation. Default: False
        thirds (bool): Use 'thirds' calculation. Default: False
        mamode (str): See ``help(ta.ma)``. Default: 'ema'
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 20)
    rvi_length = v_pos_default(rvi_length, 14)
    _length = 2 * max(length, rvi_length) - min(length, rvi_length) // 2 - 1
    close = v_series(close, _length)

    if close is None:
        return

    refined = v_bool(refined, False)
    thirds = v_bool(thirds, False)

    if refined or thirds:
        high = v_series(high, _length)
        low = v_series(low, _length)
        if high is None or low is None:
            return

    scalar = v_scalar(scalar, 100)
    mamode = v_mamode(mamode, "ema")
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    if refined:
        _mode = "r"
        rvi_ = rvi(
                    close, high=high, low=low, length=rvi_length,
                    scalar=scalar, refined=refined, mamode=mamode
                )
    elif thirds:
        _mode = "t"
        rvi_ = rvi(
                    close, high=high, low=low, length=rvi_length,
                    scalar=scalar, thirds=thirds, mamode=mamode
                )
    else:
        _mode = ""
        rvi_ = rvi(close, length=rvi_length, scalar=scalar, mamode=mamode)

    if all(isnan(rvi_)):
        return  # Emergency Break

    inertia = linreg(rvi_, length=length)
    if all(isnan(inertia)):
        return  # Emergency Break

    # Offset
    if offset != 0:
        inertia = inertia.shift(offset)

    # Fill
    if "fillna" in kwargs:
        inertia.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"_{length}_{rvi_length}"
    inertia.name = f"INERTIA{_mode}{_props}"
    inertia.category = "momentum"

    return inertia
