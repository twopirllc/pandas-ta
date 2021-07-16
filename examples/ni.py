# -*- coding: utf-8 -*-
from pandas_ta.overlap import sma
from pandas_ta.utils import get_offset, verify_series

# - Standard definition of your custom indicator function (including docs)-

def ni(close, length=None, centered=False, offset=None, **kwargs):
    """
    Example indicator ni
    """
    # Validate Arguments
    length = int(length) if length and length > 0 else 20
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None: return

    # Calculate Result
    t = int(0.5 * length) + 1
    ma = sma(close, length)

    ni = close - ma.shift(t)
    if centered:
        ni = (close.shift(t) - ma).shift(-t)

    # Offset
    if offset != 0:
        ni = ni.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        ni.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        ni.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    ni.name = f"ni_{length}"
    ni.category = "trend"

    return ni

ni.__doc__ = \
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
    centered (bool): Shift the ni back by int(0.5 * length) + 1. Default: False
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""

# - Define a matching class method --------------------------------------------

# NOTE: we need to temporarily use another name for the method than for the 
# function to avoid a name conflict in this module. But by using the bind 
# function below we can name it right so that doesn't really matter. 
# Just remember to rename the method if you at a later stage decide to move it 
# into the core.py module inside pandas_ta
def ni_method(self, length=None, offset=None, **kwargs):
    close = self._get_column(kwargs.pop("close", "close"))
    result = ni(close=close, length=length, offset=offset, **kwargs)
    return self._post_process(result, **kwargs)

# - Bind the function to pandas_ta and the method to AnalysisIndicators -------

from pandas_ta.custom import bind
bind('ni', ni, ni_method)