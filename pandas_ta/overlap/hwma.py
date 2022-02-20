# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import get_offset, verify_series


def hwma(
    close: Series,
    na: IntFloat = None, nb: IntFloat = None, nc: IntFloat = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """HWMA (Holt-Winter Moving Average)

    Indicator HWMA (Holt-Winter Moving Average) is a three-parameter
    moving average by the Holt-Winter method; the three parameters should
    be selected to obtain a forecast.

    This version has been implemented for Pandas TA by rengel8 based
    on a publication for MetaTrader 5.

    Sources:
        https://www.mql5.com/en/code/20856

    Args:
        close (pd.Series): Series of 'close's
        na (float): Smoothed series parameter (from 0 to 1). Default: 0.2
        nb (float): Trend parameter (from 0 to 1). Default: 0.1
        nc (float): Seasonality parameter (from 0 to 1). Default: 0.1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: hwma
    """
    # Validate
    na = float(na) if na and na > 0 and na < 1 else 0.2
    nb = float(nb) if nb and nb > 0 and nb < 1 else 0.1
    nc = float(nc) if nc and nc > 0 and nc < 1 else 0.1
    close = verify_series(close)
    offset = get_offset(offset)

    # Calculate
    last_a = last_v = 0
    last_f = close.iloc[0]

    result = []
    m = close.size
    for i in range(m):
        F = (1.0 - na) * (last_f + last_v + 0.5 * last_a) + na * close.iloc[i]
        V = (1.0 - nb) * (last_v + last_a) + nb * (F - last_f)
        A = (1.0 - nc) * last_a + nc * (V - last_v)
        result.append((F + V + 0.5 * A))
        last_a, last_f, last_v = A, F, V  # update values

    hwma = Series(result, index=close.index)

    # Offset
    if offset != 0:
        hwma = hwma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        hwma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        hwma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    hwma.name = f"HWMA_{na}_{nb}_{nc}"
    hwma.category = "overlap"

    return hwma
