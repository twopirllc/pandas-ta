# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.trend.long_run import long_run
from pandas_ta.trend.short_run import short_run
from pandas_ta.utils import v_mamode, v_offset, v_pos_default, v_series
from .obv import obv



def aobv(
    close: Series, volume: Series, fast: Int = None, slow: Int = None,
    max_lookback: Int = None, min_lookback: Int = None,
    mamode: str = None, run_length: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Archer On Balance Volume (AOBV)

    Archer On Balance Volume (AOBV) developed by Kevin Johnson provides
    additional indicator analysis on OBV. It calculates moving averages, default
    'ema', of OBV as well as the moving average Long and Short Run Trends, see
    ``help(ta.long_run)``. Lastly, the indicator also calculates the rolling
    Maximum and Minimum OBV.

    Sources:
        https://www.tradingview.com/script/Co1ksara-Trade-Archer-On-balance-Volume-Moving-Averages-v1/

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        fast (int): The period of the fast moving average. Default: 4
        slow (int): The period of the slow moving average. Default: 12
        max_lookback (int): Maximum OBV bars back. Default: 2
        min_lookback (int): Minimum OBV bars back. Default: 2
        run_length (int): Trend length for OBV long and short runs. Default: 2
        mamode (str): See ``help(ta.ma)``. Default: 'ema'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: OBV_MIN, OBV_MAX, OBV_FMA, OBV_SMA, OBV_LR, OBV_SR columns.
    """
    # Validate
    fast = v_pos_default(fast, 4)
    slow = v_pos_default(slow, 12)
    min_lookback = v_pos_default(min_lookback, 2)
    max_lookback = v_pos_default(max_lookback, 2)

    if slow < fast:
        fast, slow = slow, fast
    _length = max(max_lookback, min_lookback) + slow

    close = v_series(close, _length)
    volume = v_series(volume, _length)

    if close is None or volume is None:
        return

    mamode = v_mamode(mamode, "ema")
    run_length = v_pos_default(run_length, 2)
    offset = v_offset(offset)
    # remove length so it doesn't override ema length
    if "length" in kwargs:
        kwargs.pop("length")

    # Calculate
    obv_ = obv(close=close, volume=volume, **kwargs)
    maf = ma(mamode, obv_, length=fast, **kwargs)
    mas = ma(mamode, obv_, length=slow, **kwargs)

    obv_long = long_run(maf, mas, length=run_length)
    obv_short = short_run(maf, mas, length=run_length)

    # Offset
    if offset != 0:
        obv_ = obv_.shift(offset)
        maf = maf.shift(offset)
        mas = mas.shift(offset)
        obv_long = obv_long.shift(offset)
        obv_short = obv_short.shift(offset)

    # Fill
    if "fillna" in kwargs:
        obv_.fillna(kwargs["fillna"], inplace=True)
        maf.fillna(kwargs["fillna"], inplace=True)
        mas.fillna(kwargs["fillna"], inplace=True)
        obv_long.fillna(kwargs["fillna"], inplace=True)
        obv_short.fillna(kwargs["fillna"], inplace=True)

    _mode = mamode.lower()[0] if len(mamode) else ""
    data = {
        obv_.name: obv_,
        f"OBV_min_{min_lookback}": obv_.rolling(min_lookback).min(),
        f"OBV_max_{max_lookback}": obv_.rolling(max_lookback).max(),
        f"OBV{_mode}_{fast}": maf,
        f"OBV{_mode}_{slow}": mas,
        f"AOBV_LR_{run_length}": obv_long,
        f"AOBV_SR_{run_length}": obv_short
    }
    df = DataFrame(data, index=close.index)

    # Name and Category
    df.name = f"AOBV{_mode}_{fast}_{slow}_{min_lookback}_{max_lookback}_{run_length}"
    df.category = "volume"

    return df
