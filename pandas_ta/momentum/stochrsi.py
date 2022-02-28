# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.momentum import rsi
from pandas_ta.utils import non_zero_range, v_mamode
from pandas_ta.utils import v_offset, v_pos_default, v_series


def stochrsi(
    close: Series, length: Int = None, rsi_length: Int = None,
    k: Int = None, d: Int = None, mamode: str = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Stochastic (STOCHRSI)

    "Stochastic RSI and Dynamic Momentum Index" was created by Tushar Chande
    and Stanley Kroll and published in Stock & Commodities V.11:5 (189-199)

    It is a range-bound oscillator with two lines moving between 0 and 100.
    The first line (%K) displays the current RSI in relation to the period's
    high/low range. The second line (%D) is a Simple Moving Average of the
    %K line. The most common choices are a 14 period %K and a 3 period
    SMA for %D.

    Sources:
        https://www.tradingview.com/wiki/Stochastic_(STOCH)

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): The STOCHRSI period. Default: 14
        rsi_length (int): RSI period. Default: 14
        k (int): The Fast %K period. Default: 3
        d (int): The Slow %K period. Default: 3
        mamode (str): See ``help(ta.ma)``. Default: 'sma'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: RSI %K, RSI %D columns.
    """
    # Validate
    length = v_pos_default(length, 14)
    rsi_length = v_pos_default(rsi_length, 14)
    k = v_pos_default(k, 3)
    d = v_pos_default(d, 3)
    close = v_series(close, length + rsi_length + k + d)

    if close is None:
        return

    mamode = v_mamode(mamode, "sma")
    offset = v_offset(offset)

    # Calculate
    rsi_ = rsi(close, length=rsi_length)
    lowest_rsi = rsi_.rolling(length).min()
    highest_rsi = rsi_.rolling(length).max()

    stoch = 100 * (rsi_ - lowest_rsi)
    stoch /= non_zero_range(highest_rsi, lowest_rsi)

    stochrsi_k = ma(mamode, stoch, length=k)
    stochrsi_d = ma(mamode, stochrsi_k, length=d)

    # Offset
    if offset != 0:
        stochrsi_k = stochrsi_k.shift(offset)
        stochrsi_d = stochrsi_d.shift(offset)

    # Fill
    if "fillna" in kwargs:
        stochrsi_k.fillna(kwargs["fillna"], inplace=True)
        stochrsi_d.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        stochrsi_k.fillna(method=kwargs["fill_method"], inplace=True)
        stochrsi_d.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _name = "STOCHRSI"
    _props = f"_{length}_{rsi_length}_{k}_{d}"
    stochrsi_k.name = f"{_name}k{_props}"
    stochrsi_d.name = f"{_name}d{_props}"
    stochrsi_k.category = stochrsi_d.category = "momentum"

    data = {stochrsi_k.name: stochrsi_k, stochrsi_d.name: stochrsi_d}
    df = DataFrame(data)
    df.name = f"{_name}{_props}"
    df.category = stochrsi_k.category

    return df
