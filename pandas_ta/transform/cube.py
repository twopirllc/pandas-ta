# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta.utils import get_offset, verify_series


def cube(
        close: Series, cubing_exponent: float = None, signal_offset: int = None,
        offset: int = None, **kwargs
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
        Book: Cycle Analytics for Traders, 2014, written by John Ehlers, page 200
        Implemented by rengel8 for Pandas TA based on code of Markus K. (cryptocoinserver)

    Args:
        close (pd.Series): Series of 'close's
        cubing_exponent (float): Use this exponent 'wisely' to increase the
            impact of the soft limiter. Default: 3
        signal_offset (int): Offset the signal line. Default: -1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: New feature generated.
    """
    # Validate
    close = verify_series(close)
    cubing_exponent = float(cubing_exponent) if cubing_exponent and cubing_exponent >= 3.0 else 3.0
    signal_offset = int(signal_offset) if signal_offset and signal_offset > 0 else 1
    offset = get_offset(offset)

    # Calculate
    result = close ** cubing_exponent
    ct = Series(result, index=close.index)
    ct_signal = Series(result, index=close.index)

    # Offset
    if offset != 0:
        ct = ct.shift(offset)
        ct_signal = ct_signal.shift(offset)
    if signal_offset != 0:
        ct = ct.shift(signal_offset)
        ct_signal = ct_signal.shift(signal_offset)

    # Fill
    if "fillna" in kwargs:
        ct.fillna(kwargs["fillna"], inplace=True)
        ct_signal.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ct.fillna(method=kwargs["fill_method"], inplace=True)
        ct_signal.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _props = f"_{cubing_exponent}_{signal_offset}"
    ct.name = f"CUBE{_props}"
    ct_signal.name = f"CUBEs{_props}"
    ct.category = ct_signal.category = "transform"

    df = DataFrame({ct.name: ct, ct_signal.name: ct_signal})
    df.name = f"CUBE{_props}"
    df.category = ct.category

    return df
