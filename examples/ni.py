# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.ma import ma
from pandas_ta.utils import v_mamode, v_offset, v_pos_default, v_series

# - Standard definition of your custom indicator function (including docs)-
def ni(
    close: Series, length: Int = None,
    centered: bool = False, mamode: str = None,
    offset: Int = None, **kwargs: DictLike
):
    """Example indicator (NI)

    Is an indicator provided solely as an example

    Sources:
        https://github.com/twopirllc/pandas-ta/issues/264

    Calculation:
        Default Inputs:
            length=20, centered=False
        SMA = Simple Moving Average
        t = int(0.5 * length) + 1

        ni = close.shift(t) - SMA(close, length)
        if centered:
            ni = ni.shift(-t)

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 20
        mamode (str): Chosen Moving Average. Default: "sma"
        centered (bool): Shift the ni back by int(0.5 * length) + 1. Default: False
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """    # Validate Arguments
    length = v_pos_default(length, 20)
    close = v_series(close, length)

    if close is None:
        return

    mamode = v_mamode(mamode, "sma")
    offset = v_offset(offset)

    # Calculate Result
    ma = ma(mamode, close, length=length, **kwargs)

    t = int(0.5 * length) + 1
    ni = close - ma.shift(t)
    if centered:
        ni = (close.shift(t) - ma).shift(-t)

    # Offset
    if offset != 0:
        ni = ni.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        ni.fillna(kwargs["fillna"], inplace=True)

    # Name and Categorize it
    ni.name = f"ni_{length}"
    ni.category = "trend"

    return ni


# - Define a matching class method --------------------------------------------

def ni_method(self, length=None, offset=None, **kwargs):
    close = self._get_column(kwargs.pop("close", "close"))
    result = ni(close=close, length=length, offset=offset, **kwargs)
    return self._post_process(result, **kwargs)
