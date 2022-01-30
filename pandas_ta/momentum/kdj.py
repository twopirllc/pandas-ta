# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta.utils import get_offset, non_zero_range, rma_pandas, verify_series


def kdj(
    high: Series, low: Series, close: Series,
    length: int = None, signal: int = None,
    offset: int = None, **kwargs
) -> Series:
    """KDJ (KDJ)

    The KDJ indicator is actually a derived form of the Slow
    Stochastic with the only difference being an extra line
    called the J line. The J line represents the divergence
    of the %D value from the %K. The value of J can go
    beyond [0, 100] for %K and %D lines on the chart.

    Sources:
        https://www.prorealcode.com/prorealtime-indicators/kdj/
        https://docs.anychart.com/Stock_Charts/Technical_Indicators/Mathematical_Description#kdj

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): Default: 9
        signal (int): Default: 3
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 9
    signal = int(signal) if signal and signal > 0 else 3
    _length = max(length, signal)
    high = verify_series(high, _length)
    low = verify_series(low, _length)
    close = verify_series(close, _length)
    offset = get_offset(offset)

    if high is None or low is None or close is None:
        return

    # Calculate
    highest_high = high.rolling(length).max()
    lowest_low = low.rolling(length).min()

    fastk = 100 * (close - lowest_low) / \
        non_zero_range(highest_high, lowest_low)

    k = rma_pandas(fastk, length=signal)
    d = rma_pandas(k, length=signal)
    j = 3 * k - 2 * d

    # Offset
    if offset != 0:
        k = k.shift(offset)
        d = d.shift(offset)
        j = j.shift(offset)

    # Fill
    if "fillna" in kwargs:
        k.fillna(kwargs["fillna"], inplace=True)
        d.fillna(kwargs["fillna"], inplace=True)
        j.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        k.fillna(method=kwargs["fill_method"], inplace=True)
        d.fillna(method=kwargs["fill_method"], inplace=True)
        j.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _params = f"_{length}_{signal}"
    k.name = f"K{_params}"
    d.name = f"D{_params}"
    j.name = f"J{_params}"
    k.category = d.category = j.category = "momentum"

    kdjdf = DataFrame({k.name: k, d.name: d, j.name: j})
    kdjdf.name = f"KDJ{_params}"
    kdjdf.category = "momentum"

    return kdjdf
