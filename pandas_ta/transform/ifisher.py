# -*- coding: utf-8 -*-
from numpy import exp, isnan, logical_and, max, min
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import v_int, v_offset, v_scalar, v_series
from .remap import remap



def ifisher(
    close: Series,
    amp: IntFloat = None, signal_offset: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """
    Indicator: Inverse Fisher Transform

    John Ehlers describes this indicator as a tool to change the
    "Probability Distribution Function (PDF)" for the results of known
    oscillator-indicators (time series) to receive clearer signals. Its input
    needs to be normalized into the range from -1 to 1. Input data in the
    range of -0.5 to 0.5 would not have a significant impact. Ehlers note's as
    an important fact that larger values will be transformed or compressed
    stronger to the underlying unity of -1 to 1.

    Preparation Examples (or use 'remap'-indicator for this preparation):
        (RSI - 50) * 0.1        RSI [0 to 100] -> -5 to 5
        (RSI - 50) * 0.02       RSI [0 to 100] -> -1 to 1, use amp of 5 to
                                                           match input of
                                                           example above

    Sources:
        https://www.mesasoftware.com/papers/TheInverseFisherTransform.pdf,
        Book: Cycle Analytics for Traders, 2014, written by John Ehlers,
            page 198
        Coded by rengel8 based on Markus K. (cryptocoinserver)'s source.

    Args:
        close (pd.Series): Series of 'close's
        amp (float): Use the amplifying factor to increase the impact of
            the soft limiter. Default: 1
        signal_offset (int): Offset the signal line. Default: -1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: New feature generated.
    """
    # Validate
    close = v_series(close)
    amp = v_scalar(amp, 1.0)
    signal_offset = v_int(signal_offset, -1, 0)
    offset = v_offset(offset)

    # Calculate
    np_close = close.to_numpy()
    is_remapped = logical_and(np_close >= -1, np_close <= 1)
    if not all(is_remapped):
        np_max, np_min = max(np_close), min(np_close)
        close_map = remap(close, from_min=np_min, from_max=np_max, to_min=-1, to_max=1)
        if close_map is None or all(isnan(close_map.to_numpy())):
            return  # Emergency Break
        np_close = close_map.to_numpy()
    amped = exp(amp * np_close)
    result = (amped - 1) / (amped + 1)

    inv_fisher = Series(result, index=close.index)
    signal = Series(result, index=close.index)

    # Offset
    if offset != 0:
        inv_fisher = inv_fisher.shift(offset)
        signal = signal.shift(offset)
    if signal_offset != 0:
        inv_fisher = inv_fisher.shift(signal_offset)
        signal = signal.shift(signal_offset)

    # Fill
    if "fillna" in kwargs:
        inv_fisher.fillna(kwargs["fillna"], inplace=True)
        signal.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"_{amp}"
    inv_fisher.name = f"INVFISHER{_props}"
    signal.name = f"INVFISHERs{_props}"
    inv_fisher.category = signal.category = "transform"

    data = {inv_fisher.name: inv_fisher, signal.name: signal}
    df = DataFrame(data, index=close.index)
    df.name = f"INVFISHER{_props}"
    df.category = inv_fisher.category

    return df
