# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.overlap import linreg
from pandas_ta.utils import v_offset, v_pos_default, v_series



def cti(
    close: Series, length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Correlation Trend Indicator (CTI)

    The Correlation Trend Indicator is an oscillator created
    by John Ehler in 2020. It assigns a value depending on how close prices
    in that range are to following a positively- or negatively-sloping
    straight line. Values range from -1 to 1. This is a wrapper
    for ta.linreg(close, r=True).

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 12
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: Series of the CTI values for the given period.
    """
    # Validate
    length = v_pos_default(length, 12)
    close = v_series(close, length)

    if close is None:
        return

    offset = v_offset(offset)

    # Calculate
    cti = linreg(close, length=length, r=True)

    # Offset
    if offset != 0:
        cti = cti.shift(offset)

    # Fill
    if "fillna" in kwargs:
        cti.fillna(method=kwargs["fillna"], inplace=True)

    # Name and Category
    cti.name = f"CTI_{length}"
    cti.category = "momentum"

    return cti
