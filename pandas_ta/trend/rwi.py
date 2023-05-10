# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.volatility import atr
from pandas_ta.utils import (
    v_drift,
    v_mamode,
    v_offset,
    v_pos_default,
    v_series,
    v_scalar,
    v_talib
)


def rwi(
    high: Series, low: Series, close: Series,
    length: Int = None, lensig: Int = None, scalar: IntFloat = None,
    mamode: str = None, talib: bool = None,
    drift: Int = None, offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Random Walk Index (RWI)

    This indicator aims to differntiate whether the price is following a specific trend
    or is doing a random walk

    Sources:
        https://www.technicalindicators.net/indicators-technical-analysis/168-rwi-random-walk-index

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        lensig (int): Signal Length. Like TradingView's default ADX.
            Default: length
        scalar (float): How much to magnify. Default: 100
        mamode (str): See ```help(ta.ma)```. Default: 'rma'
        talib (bool): If TA Lib is installed and talib is True, Returns the
            TA Lib version. Default: True
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: high, low columns.
    """

    # Validate Arguments
    length = v_pos_default(length, 14)
    lensig = v_pos_default(lensig, length)
    _length = max(length, lensig)
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return

    scalar = v_scalar(scalar, 100)
    mamode = v_mamode(mamode, "rma")
    mode_tal = v_talib(talib)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate Result
    atr_ = atr(
        high=high, low=low, close=close,
        length=length, mamode=mamode, talib=mode_tal
    )
    denom = atr_ * (length ** 0.5)

    rwi_high = ((high - low.shift(length)) / denom)#.shift(-length)
    rwi_low = ((high.shift(length) - low) / denom)#.shift(-length)

    # Offset
    if offset != 0:
        rwi_high = rwi_high.shift(offset)
        rwi_low = rwi_low.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        rwi_high.fillna(kwargs["fillna"], inplace=True)
        rwi_low.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        rwi_high.fillna(method=kwargs["fill_method"], inplace=True)
        rwi_low.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    rwi_high.name = f"RWIh_{lensig}"
    rwi_low.name = f"RWIl_{lensig}"
    rwi_high.category = rwi_low.category = "trend"

    # Prepare DataFrame to return
    data = {rwi_high.name: rwi_high, rwi_low.name: rwi_low}
    rwidf = DataFrame(data)
    rwidf.name = f"RWI_{lensig}"
    rwidf.category = "trend"

    return rwidf
