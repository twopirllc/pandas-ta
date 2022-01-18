# -*- coding: utf-8 -*-
from numpy import exp as npExp
from pandas import DataFrame, Series
from pandas_ta.utils import get_offset, verify_series


def ifisher(close: Series, amplifying_factor: float = None, signal_offset: int = None, offset: int = None,
            **kwargs) -> DataFrame:
    """
    Indicator: Inverse Fisher Transform

    John Ehlers describes this indicator as a tool to change the "Probability Distribution Function (PDF)" for
    the results of known oscillator-indicators (time series) to receive clearer signals.
    Its input needs to be normalized into the range from -1 to 1. Input data in the range of -0.5 to 0.5
    would not have a significant impact. Ehlers note's as an important fact that larger values will be transformed
    or compressed stronger to the underlying unity of -1 to 1.

    Preparation Examples (or use 'remap'-indicator for this preparation):
        (RSI - 50) * 0.1        RSI [0 to 100] -> -5 to 5
        (RSI - 50) * 0.02       RSI [0 to 100] -> -1 to 1, use amplifying_factor of 5 to match input of example above

    Sources:
        https://www.mesasoftware.com/papers/TheInverseFisherTransform.pdf,
        Book: Cycle Analytics for Traders, 2014, written by John Ehlers, page 198
        Implemented by rengel8 for Pandas TA based on code of Markus K. (cryptocoinserver)

    Args:
        close (pd.Series): Series of 'close's
        amplifying_factor (float):  Use this factor to increase the impact of the soft limiter. Default: 1
        signal_offset (int): Offset the signal line.  Default: -1
        offset (int): How many periods to offset the result.  Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: New feature generated.
    """

    # Validate arguments
    close = verify_series(close)
    amplifying_factor = float(amplifying_factor) if amplifying_factor and amplifying_factor != 0 else 1.0
    signal_offset = int(signal_offset) if signal_offset and signal_offset > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    series = close.to_numpy()
    result = (npExp(amplifying_factor * series) - 1) / (npExp(amplifying_factor * series) + 1)

    # Series
    inv_fisher = Series(result, index=close.index)
    inv_fisher_signal = Series(result, index=close.index)

    # Offset
    if offset != 0:
        inv_fisher = inv_fisher.shift(offset)
        inv_fisher_signal = inv_fisher_signal.shift(offset)
    if signal_offset != 0:
        inv_fisher_signal = inv_fisher_signal.shift(signal_offset)        # !!!!

    # Handle fills
    if "fillna" in kwargs:
        inv_fisher.fillna(kwargs["fillna"], inplace=True)
        inv_fisher_signal.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        inv_fisher.fillna(method=kwargs["fill_method"], inplace=True)
        inv_fisher_signal.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    inv_fisher.name = f"INV_FISHER"
    inv_fisher_signal.name = f"INV_FISHER_SIGNAL"
    inv_fisher.category = inv_fisher_signal.category = "transform"

    # Prepare DataFrame to return
    data = {inv_fisher.name: inv_fisher, inv_fisher_signal.name: inv_fisher_signal}
    df = DataFrame(data)
    df.name = f"INVERSE_FISHER_TRANSFORM"
    df.category = inv_fisher.category

    return df
