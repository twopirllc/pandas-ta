# -*- coding: utf-8 -*-
from pandas import Series
from numpy import log, nan, roll
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_bool, v_offset, v_pos_default, v_series


def log_return(
    close: Series, length: Int = None, cumulative: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Log Return

    Calculates the logarithmic return of a Series.
    See also: help(df.ta.log_return) for additional **kwargs a valid 'df'.

    Sources:
        https://stackoverflow.com/questions/31287552/logarithmic-returns-in-pandas-dataframe

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 20
        cumulative (bool): If True, returns the cumulative returns.
            Default: False
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 1)
    close = v_series(close, length)

    if close is None:
        return

    cumulative = v_bool(cumulative, False)
    offset = v_offset(offset)

    # Calculate
    np_close = close.values
    if cumulative:
        r = np_close / np_close[0]
    else:
        r = np_close / roll(np_close, length)
        r[:length] = nan
    log_return = Series(log(r), index=close.index)

    # Offset
    if offset != 0:
        log_return = log_return.shift(offset)

    # Fill
    if "fillna" in kwargs:
        log_return.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        log_return.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    log_return.name = f"{'CUM' if cumulative else ''}LOGRET_{length}"
    log_return.category = "performance"

    return log_return
