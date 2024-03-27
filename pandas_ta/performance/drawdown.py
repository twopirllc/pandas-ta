# -*- coding: utf-8 -*-
from numpy import log, seterr
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_series



def drawdown(
    close: Series, offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Drawdown (DD)

    Drawdown is a peak-to-trough decline during a specific period for an
    investment, trading account, or fund. It is usually quoted as the
    percentage between the peak and the subsequent trough.

    Sources:
        https://www.investopedia.com/terms/d/drawdown.asp

    Args:
        close (pd.Series): Series of 'close's.
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: drawdown, drawdown percent, drawdown log columns
    """
    # Validate
    close = v_series(close)
    offset = v_offset(offset)

    # Calculate
    max_close = close.cummax()
    dd = max_close - close
    dd_pct = 1 - (close / max_close)

    _np_err = seterr()
    seterr(divide="ignore", invalid="ignore")
    dd_log = log(max_close) - log(close)
    seterr(divide=_np_err["divide"], invalid=_np_err["invalid"])

    # Offset
    if offset != 0:
        dd = dd.shift(offset)
        dd_pct = dd_pct.shift(offset)
        dd_log = dd_log.shift(offset)

    # Fill
    if "fillna" in kwargs:
        dd.fillna(kwargs["fillna"], inplace=True)
        dd_pct.fillna(kwargs["fillna"], inplace=True)
        dd_log.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    dd.name = "DD"
    dd_pct.name = f"{dd.name}_PCT"
    dd_log.name = f"{dd.name}_LOG"
    dd.category = dd_pct.category = dd_log.category = "performance"

    data = {dd.name: dd, dd_pct.name: dd_pct, dd_log.name: dd_log}
    df = DataFrame(data, index=close.index)
    df.name = dd.name
    df.category = dd.category

    return df
