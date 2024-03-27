# -*- coding: utf-8 -*-
from numpy import isnan
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import v_int, v_lowerbound, v_offset, v_series



def cube(
    close: Series, pwr: IntFloat = None, signal_offset: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """
    Indicator: Cube Transform

    John Ehlers describes this indicator to be useful in compressing signals
    near zero for a normalized oscillator like the Inverse Fisher Transform.
    In conjunction to that, values close to -1 and 1 are nearly unchanged,
    whereas the ones near zero are reduced regarding their amplitude.

    From the input data the effects of spectral dilation should have been
    removed (i.e. roofing filter).

    Sources:
        Book: Cycle Analytics for Traders, 2014, written by John Ehlers
            page 200
        Coded by rengel8 based on Markus K. (cryptocoinserver)'s source.

    Args:
        close (pd.Series): Series of 'close's
        pwr (float): Use this exponent 'wisely' to increase the impact of the
            soft limiter. Default: 3
        signal_offset (int): Offset the signal line. Default: -1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: New feature generated.
    """
    # Validate
    close = v_series(close)
    pwr = v_lowerbound(pwr, 3.0, 3.0, strict=False)
    signal_offset = v_int(signal_offset, -1, 0)
    offset = v_offset(offset)

    # Calculate
    result = close ** pwr
    ct = Series(result, index=close.index)
    ct_signal = Series(result, index=close.index)

    # Offset
    if offset != 0:
        ct = ct.shift(offset)
        ct_signal = ct_signal.shift(offset)
    if signal_offset != 0:
        ct = ct.shift(signal_offset)
        ct_signal = ct_signal.shift(signal_offset)

    if all(isnan(ct)) and all(isnan(ct_signal)):
        return  # Emergency Break

    # Fill
    if "fillna" in kwargs:
        ct.fillna(kwargs["fillna"], inplace=True)
        ct_signal.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"_{pwr}_{signal_offset}"
    ct.name = f"CUBE{_props}"
    ct_signal.name = f"CUBEs{_props}"
    ct.category = ct_signal.category = "transform"

    data = {ct.name: ct, ct_signal.name: ct_signal}
    df = DataFrame(data, index=close.index)
    df.name = f"CUBE{_props}"
    df.category = ct.category

    return df
