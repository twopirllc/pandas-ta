# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import get_offset, verify_series
from pandas_ta.volatility import atr


def cksp(
    high: Series, low: Series, close: Series,
    p: Int = None, x: IntFloat = None, q: Int = None,
    tvmode: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Chande Kroll Stop (CKSP)

    The Tushar Chande and Stanley Kroll in their book
    “The New Technical Trader”. It is a trend-following indicator,
    identifying your stop by calculating the average true range of
    the recent market volatility. The indicator defaults to the implementation
    found on tradingview but it provides the original book implementation as
    well, which differs by the default periods and moving average mode. While
    the trading view implementation uses the Welles Wilder moving average, the
    book uses a simple moving average.

    Defaults:
    Book:         p=10, x=3, q=20
    Trading View: p=10, x=1, q=9

    Sources:
        https://www.multicharts.com/discussion/viewtopic.php?t=48914
        "The New Technical Trader", Wikey 1st ed. ISBN 9780471597803, page 95

    Args:
        close (pd.Series): Series of 'close's
        p (int): ATR and first stop period. Default: 10 in both modes
        x (float): ATR scalar. Default: 1 in TV mode, 3 otherwise
        q (int): Second stop period. Default: 9 in TV mode, 20 otherwise
        tvmode (bool): Trading View or book implementation mode. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: long and short columns.
    """
    # Validate
    tvmode = tvmode if isinstance(tvmode, bool) else True
    p = int(p) if p and p > 0 else 10
    x = float(x) if x and x > 0 else 1 if tvmode is True else 3
    q = int(q) if q and q > 0 else 9 if tvmode is True else 20
    _length = max(p, q, x)

    high = verify_series(high, _length)
    low = verify_series(low, _length)
    close = verify_series(close, _length)
    if high is None or low is None or close is None:
        return

    offset = get_offset(offset)
    mamode = "rma" if tvmode is True else "sma"

    # Calculate
    atr_ = atr(high=high, low=low, close=close, length=p, mamode=mamode)

    long_stop_ = high.rolling(p).max() - x * atr_
    long_stop = long_stop_.rolling(q).max()

    short_stop_ = low.rolling(p).min() + x * atr_
    short_stop = short_stop_.rolling(q).min()

    # Offset
    if offset != 0:
        long_stop = long_stop.shift(offset)
        short_stop = short_stop.shift(offset)

    # Fill
    if "fillna" in kwargs:
        long_stop.fillna(kwargs["fillna"], inplace=True)
        short_stop.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        long_stop.fillna(method=kwargs["fill_method"], inplace=True)
        short_stop.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _props = f"_{p}_{x}_{q}"
    long_stop.name = f"CKSPl{_props}"
    short_stop.name = f"CKSPs{_props}"
    long_stop.category = short_stop.category = "trend"

    ckspdf = DataFrame({
        long_stop.name: long_stop, short_stop.name: short_stop
    })
    ckspdf.name = f"CKSP{_props}"
    ckspdf.category = long_stop.category

    return ckspdf
