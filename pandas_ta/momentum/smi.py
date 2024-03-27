# -*- coding: utf-8 -*-
from numpy import isnan
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import v_offset, v_pos_default, v_scalar, v_series
from .tsi import tsi



def smi(
    close: Series, fast: Int = None, slow: Int = None,
    signal: Int = None, scalar: IntFloat = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """SMI Ergodic Indicator (SMI)

    The SMI Ergodic Indicator is the same as the True Strength Index (TSI)
    developed by William Blau, except the SMI includes a signal line.
    The SMI uses double moving averages of price minus previous price
    over 2 time frames. The signal line, which is an EMA of the SMI, is
    plotted to help trigger trading signals. The trend is bullish when
    crossing above zero and bearish when crossing below zero. This
    implementation includes both the SMI Ergodic Indicator and
    SMI Ergodic Oscillator.

    Sources:
        https://www.motivewave.com/studies/smi_ergodic_indicator.htm
        https://www.tradingview.com/script/Xh5Q0une-SMI-Ergodic-Oscillator/
        https://www.tradingview.com/script/cwrgy4fw-SMIIO/

    Args:
        close (pd.Series): Series of 'close's
        fast (int): The short period. Default: 5
        slow (int): The long period. Default: 20
        signal (int): The signal period. Default: 5
        scalar (float): How much to magnify. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: smi, signal, oscillator columns.
    """
    # Validate
    fast = v_pos_default(fast, 5)
    slow = v_pos_default(slow, 20)
    signal = v_pos_default(signal, 5)
    if slow < fast:
        fast, slow = slow, fast
    _length = slow + signal + 1
    close = v_series(close, _length)

    if close is None:
        return

    scalar = v_scalar(scalar, 1)
    offset = v_offset(offset)

    # Calculate
    tsi_df = tsi(close, fast=fast, slow=slow, signal=signal, scalar=scalar)
    if tsi_df is None:
        return  # Emergency Break

    smi = tsi_df.iloc[:, 0]
    signalma = tsi_df.iloc[:, 1]
    if all(isnan(signalma)):
        return  # Emergency Break
    osc = smi - signalma

    # Offset
    if offset != 0:
        smi = smi.shift(offset)
        signalma = signalma.shift(offset)
        osc = osc.shift(offset)

    # Fill
    if "fillna" in kwargs:
        smi.fillna(kwargs["fillna"], inplace=True)
        signalma.fillna(kwargs["fillna"], inplace=True)
        osc.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    # _scalar = f"_{scalar}" if scalar != 1 else ""
    _props = f"_{fast}_{slow}_{signal}_{scalar}"
    smi.name = f"SMI{_props}"
    signalma.name = f"SMIs{_props}"
    osc.name = f"SMIo{_props}"
    smi.category = signalma.category = osc.category = "momentum"

    data = {smi.name: smi, signalma.name: signalma, osc.name: osc}
    df = DataFrame(data, index=close.index)
    df.name = f"SMI{_props}"
    df.category = smi.category

    return df
