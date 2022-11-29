# -*- coding: utf-8 -*-
from pandas import Series, DataFrame
from pandas_ta.volatility import atr as ATR
from pandas_ta._typing import Int, Float, DictLike
from pandas_ta.utils import (
    v_offset,
    v_pos_default,
    v_bool
)
import numpy as np


def chandelier_exit(high: Series, low: Series, close: Series,
                    atr_length: Int = None, roll_length: Int = None,
                    multiplier: Float = None, use_close: bool = None,
                    offset: Int = None, **kwargs: DictLike):
    """Chandelier Exit

    Chandelier Exit is an overlap indicator. It is used to set a trailing stop-loss
    based on the Average True Range. It can also inform about the trend and prevent 
    exits.

    Sources:
        https://school.stockcharts.com/doku.php?id=technical_indicators:chandelier_exit
        https://in.tradingview.com/scripts/chandelier/

    Calculation:
        Default Inputs:
            atr_length=14, roll_length=22, multiplier=2.0,
        Default Direction:
            Set to +1 or bullish trend at start

        DISTANCE = multiplier * ATR

        LONG_BAND = MAX(HIGH OR CLOSE(if use_close is True)) IN LAST roll_length CANDLES
        SHORT_BAND = MIN(LOW OR CLOSE(if use_close is True)) IN LAST roll_length CANDLES

        LONG_CHANDELIER = LONG_BAND - DISTANCE
        SHORT_CHANDELIER = SHORT_BAND + DISTANCE

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        atr_length (int) : length for ATR calculation. Default: 14
        roll_length (int): length of rolling candles for highest high and lowest 
            low calculation: 22
        multiplier (float): Coefficient for upper and lower band distance to
            midrange. Default: 2.0
        use_close (bool): If true, uses close value for highest-high and lowest-low
            calculation instead of high and low respectively.
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: CHANDELIER_LONG (long), CHANDELIER_SHORT (short), DIRECTION (direction)
    """
    atr = ATR(high, low, close, length=atr_length)

    roll_length = v_pos_default(roll_length, 22)
    multiplier = v_pos_default(multiplier, 2.0)
    use_close = v_bool(use_close, False)
    offset = v_offset(offset)

    if use_close:
        long = close.rolling(roll_length, min_periods=1).max()\
               - atr * multiplier
        short = close.rolling(roll_length, min_periods=1).min()\
                + atr * multiplier
    else:
        long = high.rolling(roll_length, min_periods=1).max()\
               - atr * multiplier
        short = low.rolling(roll_length, min_periods=1).min()\
                + atr * multiplier

    uptrend = (close > long.shift(1)).astype(int)
    downtrend = (close < short.shift(1)).astype(int) * -1
    direction = uptrend + downtrend
    if direction[0] == 0:
        direction[0] = 1
    direction = direction.replace(0, np.nan).fillna(method='ffill')

    # Offset
    if offset != 0:
        long = long.shift(offset)
        short = short.shift(offset)
        direction = short.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        long.fillna(kwargs["fillna"], inplace=True)
        short.fillna(kwargs["fillna"], inplace=True)
        direction.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        long.fillna(method=kwargs["fill_method"], inplace=True)
        short.fillna(method=kwargs["fill_method"], inplace=True)
        direction.fillna(method=kwargs["fill_method"], inplace=True)
    
    df = DataFrame({
        "CHANDELIER_LONG": long,
        "CHANDELIER_SHORT": short,
        "DIRECTION": direction
        }, index=close.index)
    _props = f"_{atr_length}_{roll_length}_{multiplier}"
    if use_close:
        _props = f"{_props}_CLOSE"
    df.name = f"CHANDELIEREXIT{_props}"
    df.category = "overlap"

    return df
