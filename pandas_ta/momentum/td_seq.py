# -*- coding: utf-8 -*-
from numpy import where
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_bool, v_offset, v_series


def td_seq(
    close: Series, asint: bool = None, show_all: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """TD Sequential (TD_SEQ)

    Tom DeMark's Sequential indicator attempts to identify a price point
    where an uptrend or a downtrend exhausts itself and reverses.

    Sources:
        https://tradetrekker.wordpress.com/tdsequential/

    Args:
        close (pd.Series): Series of 'close's
        asint (bool): If True, fillnas with 0 and change type to int.
            Default: False
        show_all (bool): Show 1 - 13. If set to False, show 6 - 9.
            Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: New feature generated.
    """
    # Validate
    close = v_series(close)

    if close is None:
        return

    asint = v_bool(asint, False)
    show_all = v_bool(show_all, True)
    offset = v_offset(offset)

    # Calculate
    up_seq = calc_td(close, "up", show_all)
    down_seq = calc_td(close, "down", show_all)

    if asint:
        if up_seq.hasnans and down_seq.hasnans:
            up_seq.fillna(0, inplace=True)
            down_seq.fillna(0, inplace=True)
        up_seq = up_seq.astype(int)
        down_seq = down_seq.astype(int)

     # Offset
    if offset != 0:
        up_seq = up_seq.shift(offset)
        down_seq = down_seq.shift(offset)

    # Fill
    if "fillna" in kwargs:
        up_seq.fillna(kwargs["fillna"], inplace=True)
        down_seq.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        up_seq.fillna(method=kwargs["fill_method"], inplace=True)
        down_seq.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    up_seq.name = f"TD_SEQ_UPa" if show_all else f"TD_SEQ_UP"
    down_seq.name = f"TD_SEQ_DNa" if show_all else f"TD_SEQ_DN"
    up_seq.category = down_seq.category = "momentum"

    data = {up_seq.name: up_seq, down_seq.name: down_seq}
    df = DataFrame(data)
    df.index = close.index  # Only works here for some reason?
    df.name = "TD_SEQ"
    df.category = up_seq.category

    return df


def sequence_count(series: Series):
    index = series.where(series == False).last_valid_index()

    if index is None:
        return series.count()
    else:
        s = series[series.index > index]
        return s.count()


def calc_td(series: Series, direction: str, show_all: bool):
    td_bool = series.diff(4) > 0 if direction == "up" else series.diff(4) < 0
    td_num = where(td_bool, td_bool.rolling(13, min_periods=0) \
        .apply(sequence_count), 0)
    td_num = Series(td_num)

    if show_all:
        td_num = td_num.mask(td_num == 0)
    else:
        td_num = td_num.mask(~td_num.between(6, 9))

    return td_num
