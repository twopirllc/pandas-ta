# -*- coding: utf-8 -*-
import numpy as np
from pandas import DataFrame, Series
from pandas_ta.utils import get_offset, verify_series

def true_sequence_count(s):
    index = s.where(s == False).last_valid_index()
    
    if index is None:
        return s.count()
    else:
        s = s[s.index > index]
        return s.count()

def calc_td(close, direction='up'):
    td_bool = close.diff(4) > 0 if direction=='up' else close.diff(4) < 0
    td_num = np.where(td_bool, td_bool.rolling(13, min_periods=0).apply(true_sequence_count), 0)
    td_num = Series(td_num)
    td_num = td_num.mask(~td_num.between(6,9))

    return td_num       

def td(close, offset=None, **kwargs):
    up = calc_td(close, 'up')
    down = calc_td(close, 'down')
    df = DataFrame({'TD_up': up, 'TD_down': down})
    
     # Offset
    if offset and offset != 0:
        df = df.shift(offset)

    if "fillna" in kwargs:
        df.fillna(kwargs["fillna"], inplace=True)

    # Name & Category
    df.name = "TD"
    df.category = "momentum"

    return df

td.__doc__ = \
"""TD Sequential (TD)

TD Sequential indicator.

Sources:
    https://tradetrekker.wordpress.com/tdsequential/

Calculation:
    compare current close price with 4 days ago price, up to 13 days.
    for the consecutive ascending or descending price sequence, display 6th to 9th day value.

Args:
    close (pd.Series): Series of 'close's
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)

Returns:
    pd.DataFrame: New feature generated.
"""