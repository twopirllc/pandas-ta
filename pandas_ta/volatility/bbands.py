# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.ma import ma
from pandas_ta.maps import Imports
from pandas_ta.statistics import stdev
from pandas_ta.utils import get_offset, non_zero_range, tal_ma, verify_series


def bbands(
    close: Series, length: Int = None, std: IntFloat = None, ddof: Int = 0,
    mamode: str = None, talib: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Bollinger Bands (BBANDS)

    A popular volatility indicator by John Bollinger.

    Sources:
        https://www.tradingview.com/wiki/Bollinger_Bands_(BB)

    Args:
        close (pd.Series): Series of 'close's
        length (int): The short period. Default: 5
        std (int): The long period. Default: 2
        ddof (int): Degrees of Freedom to use. Default: 0
        mamode (str): See ``help(ta.ma)``. Default: 'sma'
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        ddof (int): Delta Degrees of Freedom.
                    The divisor used in calculations is N - ddof, where N
                    represents the number of elements. The 'talib' argument
                    must be false for 'ddof' to work. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: lower, mid, upper, bandwidth, and percent columns.
    """
    # Validate
    length = int(length) if length and length > 0 else 5
    std = float(std) if std and std > 0 else 2.0
    mamode = mamode if isinstance(mamode, str) else "sma"
    if isinstance(ddof, int) and ddof >= 0 and ddof < length:
        ddof = int(ddof)
    else:
        ddof = 1
    close = verify_series(close, length)
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if close is None:
        return

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import BBANDS
        upper, mid, lower = BBANDS(close, length, std, std, tal_ma(mamode))
    else:
        standard_deviation = stdev(
            close=close, length=length, ddof=ddof, talib=mode_tal
        )
        deviations = std * standard_deviation
        # deviations = std * standard_deviation.loc[standard_deviation.first_valid_index():,]

        mid = ma(mamode, close, length=length, talib=mode_tal, **kwargs)
        lower = mid - deviations
        upper = mid + deviations

    ulr = non_zero_range(upper, lower)
    bandwidth = 100 * ulr / mid
    percent = non_zero_range(close, lower) / ulr

    # Offset
    if offset != 0:
        lower = lower.shift(offset)
        mid = mid.shift(offset)
        upper = upper.shift(offset)
        bandwidth = bandwidth.shift(offset)
        percent = percent.shift(offset)

    # Fill
    if "fillna" in kwargs:
        lower.fillna(kwargs["fillna"], inplace=True)
        mid.fillna(kwargs["fillna"], inplace=True)
        upper.fillna(kwargs["fillna"], inplace=True)
        bandwidth.fillna(kwargs["fillna"], inplace=True)
        percent.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        lower.fillna(method=kwargs["fill_method"], inplace=True)
        mid.fillna(method=kwargs["fill_method"], inplace=True)
        upper.fillna(method=kwargs["fill_method"], inplace=True)
        bandwidth.fillna(method=kwargs["fill_method"], inplace=True)
        percent.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    lower.name = f"BBL_{length}_{std}"
    mid.name = f"BBM_{length}_{std}"
    upper.name = f"BBU_{length}_{std}"
    bandwidth.name = f"BBB_{length}_{std}"
    percent.name = f"BBP_{length}_{std}"
    upper.category = lower.category = "volatility"
    mid.category = bandwidth.category = upper.category

    data = {
        lower.name: lower, mid.name: mid, upper.name: upper,
        bandwidth.name: bandwidth, percent.name: percent
    }
    bbandsdf = DataFrame(data)
    bbandsdf.name = f"BBANDS_{length}_{std}"
    bbandsdf.category = mid.category

    return bbandsdf
