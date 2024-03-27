# -*- coding: utf-8 -*-
from numpy import arange, array, polyfit, std
from pandas import DataFrame, DatetimeIndex, Series
from pandas_ta._typing import DictLike, Int, List
from pandas_ta.utils import v_list, v_lowerbound, v_offset, v_series



def tos_stdevall(
    close: Series, length: Int = None,
    stds: List = None, ddof: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """TD Ameritrade's Think or Swim Standard Deviation All (TOS_STDEV)

    A port of TD Ameritrade's Think or Swim Standard Deviation All indicator
    which returns the standard deviation of data for the entire plot or for
    the interval of the last bars defined by the length parameter.

    WARNING: This function may leak future data when used for machine learning.
        Setting lookahead=False does not currently prevent leakage.
        See https://github.com/twopirllc/pandas-ta/issues/667.

    Sources:
        https://tlc.thinkorswim.com/center/reference/thinkScript/Functions/Statistical/StDevAll

    Args:
        close (pd.Series): Series of 'close's
        length (int): Bars from current bar. Default: None
        stds (list): List of Standard Deviations in increasing order from the
                    central Linear Regression line. Default: [1,2,3]
        ddof (int): Delta Degrees of Freedom.
                    The divisor used in calculations is N - ddof,
                    where N represents the number of elements. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: Central LR, Pairs of Lower and Upper LR Lines based on
            multiples of the standard deviation. Default: returns 7 columns.
    """
    # Validate
    _props = f"TOS_STDEVALL"
    if length is None:
        length = close.size
    else:
        length = v_lowerbound(length, 2, 30)
        close = close.iloc[-length:]
        _props = f"{_props}_{length}"

    close = v_series(close, 2)

    if close is None:
        return

    stds = v_list(stds, [1, 2, 3])
    if min(stds) <= 0:
        return

    if not all(i < j for i, j in zip(stds, stds[1:])):
        stds = stds[::-1]

    ddof = int(ddof) if isinstance(ddof, int) and 0 <= ddof < length else 1
    offset = v_offset(offset)

    # Calculate
    X = src_index = close.index
    if isinstance(close.index, DatetimeIndex):
        X = arange(length)
        close = array(close)

    m, b = polyfit(X, close, 1)
    lr = Series(m * X + b, index=src_index)
    stdev = std(close, ddof=ddof)

    # Name and Category
    df = DataFrame({f"{_props}_LR": lr}, index=src_index)
    for i in stds:
        df[f"{_props}_L_{i}"] = lr - i * stdev
        df[f"{_props}_U_{i}"] = lr + i * stdev
        df[f"{_props}_L_{i}"].name = df[f"{_props}_U_{i}"].name = f"{_props}"
        df[f"{_props}_L_{i}"].category = df[f"{_props}_U_{i}"].category = "statistics"

    # Offset
    if offset != 0:
        df = df.shift(offset)

    # Fill
    if "fillna" in kwargs:
        df.fillna(kwargs["fillna"], inplace=True)

    df.name = f"{_props}"
    df.category = "statistics"

    return df
