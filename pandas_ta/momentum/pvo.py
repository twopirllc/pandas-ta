# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.overlap import ema
from pandas_ta.utils import get_offset, verify_series


def pvo(
    volume: Series, fast: Int = None, slow: Int = None,
    signal: Int = None, scalar: IntFloat = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Percentage Volume Oscillator (PVO)

    Percentage Volume Oscillator is a Momentum Oscillator for Volume.

    Sources:
        https://www.fmlabs.com/reference/default.htm?url=PVO.htm

    Args:
        volume (pd.Series): Series of 'volume's
        fast (int): The short period. Default: 12
        slow (int): The long period. Default: 26
        signal (int): The signal period. Default: 9
        scalar (float): How much to magnify. Default: 100
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: pvo, histogram, signal columns.
    """
    # Validate
    fast = int(fast) if fast and fast > 0 else 12
    slow = int(slow) if slow and slow > 0 else 26
    signal = int(signal) if signal and signal > 0 else 9
    scalar = float(scalar) if scalar else 100
    if slow < fast:
        fast, slow = slow, fast
    volume = verify_series(volume, max(fast, slow, signal))
    offset = get_offset(offset)

    if volume is None:
        return

    # Calculate
    fastma = ema(volume, length=fast)
    slowma = ema(volume, length=slow)
    pvo = scalar * (fastma - slowma)
    pvo /= slowma

    signalma = ema(pvo, length=signal)
    histogram = pvo - signalma

    # Offset
    if offset != 0:
        pvo = pvo.shift(offset)
        histogram = histogram.shift(offset)
        signalma = signalma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        pvo.fillna(kwargs["fillna"], inplace=True)
        histogram.fillna(kwargs["fillna"], inplace=True)
        signalma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        pvo.fillna(method=kwargs["fill_method"], inplace=True)
        histogram.fillna(method=kwargs["fill_method"], inplace=True)
        signalma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _props = f"_{fast}_{slow}_{signal}"
    pvo.name = f"PVO{_props}"
    histogram.name = f"PVOh{_props}"
    signalma.name = f"PVOs{_props}"
    pvo.category = histogram.category = signalma.category = "momentum"

    data = {pvo.name: pvo, histogram.name: histogram, signalma.name: signalma}
    df = DataFrame(data)
    df.name = pvo.name
    df.category = pvo.category

    return df
