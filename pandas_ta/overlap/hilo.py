# -*- coding: utf-8 -*-
from numpy import nan
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.utils import v_mamode, v_offset, v_pos_default, v_series



def hilo(
    high: Series, low: Series, close: Series,
    high_length: Int = None, low_length: Int = None, mamode: str = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Gann HiLo Activator(HiLo)

    The Gann High Low Activator Indicator was created by Robert Krausz in
    a 1998 issue of Stocks & Commodities Magazine. It is a moving average
    based trend indicator consisting of two different simple moving averages.

    The indicator tracks both curves (of the highs and the lows). The close
    of the bar defines which of the two gets plotted.

    Increasing high_length and decreasing low_length better for short trades,
    vice versa for long positions.

    Sources:
        https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=447&Name=Gann_HiLo_Activator
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/simple-moving-average-sma/
        https://www.tradingview.com/script/XNQSLIYb-Gann-High-Low/

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        high_length (int): It's period. Default: 13
        low_length (int): It's period. Default: 21
        mamode (str): See ``help(ta.ma)``. Default: 'sma'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        adjust (bool): Default: True
        presma (bool, optional): If True, uses SMA for initial value.
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: HILO (line), HILOl (long), HILOs (short) columns.
    """
    # Validate
    high_length = v_pos_default(high_length, 13)
    low_length = v_pos_default(low_length, 21)
    _length = max(high_length, low_length) + 1
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return

    mamode = v_mamode(mamode, "sma")
    offset = v_offset(offset)

    # Calculate
    m = close.size
    hilo = Series(nan, index=close.index)
    long = Series(nan, index=close.index)
    short = Series(nan, index=close.index)

    high_ma = ma(mamode, high, length=high_length)
    low_ma = ma(mamode, low, length=low_length)

    for i in range(1, m):
        if close.iat[i] > high_ma.iat[i - 1]:
            hilo.iat[i] = long.iat[i] = low_ma.iat[i]
        elif close.iat[i] < low_ma.iat[i - 1]:
            hilo.iat[i] = short.iat[i] = high_ma.iat[i]
        else:
            hilo.iat[i] = hilo.iat[i - 1]
            long.iat[i] = short.iat[i] = hilo.iat[i - 1]

    # Offset
    if offset != 0:
        hilo = hilo.shift(offset)
        long = long.shift(offset)
        short = short.shift(offset)

    # Fill
    if "fillna" in kwargs:
        hilo.fillna(kwargs["fillna"], inplace=True)
        long.fillna(kwargs["fillna"], inplace=True)
        short.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"_{high_length}_{low_length}"
    data = {
        f"HILO{_props}": hilo,
        f"HILOl{_props}": long,
        f"HILOs{_props}": short
    }
    df = DataFrame(data, index=close.index)

    df.name = f"HILO{_props}"
    df.category = "overlap"

    return df
