# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.ma import ma
from pandas_ta.utils import v_mamode, v_offset, v_pos_default, v_series
from .long_run import long_run
from .short_run import short_run


def amat(
    close: Series, fast: Int = None, slow: Int = None,
    lookback: Int = None, mamode: str = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Archer Moving Averages Trends (AMAT)

    Archer Moving Averages Trends (AMAT) developed by Kevin Johnson provides
    creates both long run ``help(ta.long_run)`` and short run
    ``help(ta.short_run)`` trend signals given two moving average speeds,
    fast and slow. The long runs and short runs are binary Series where '1'
    is a trend and '0' is not a trend.

    Sources:
        https://www.tradingview.com/script/Z2mq63fE-Trade-Archer-Moving-Averages-v1-4F/

    Args:
        close (pd.Series): Series of 'close's
        fast (int): The period of the fast moving average. Default: 8
        slow (int): The period of the slow moving average. Default: 21
        lookback (int): Lookback period for long_run and short_run. Default: 2
        mamode (str): See ``help(ta.ma)``. Default: 'ema'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        run_length (int): Trend length for OBV long and short runs. Default: 2
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: AMAT_LR, AMAT_SR columns.
    """
    # Validate
    fast = v_pos_default(fast, 8)
    slow = v_pos_default(slow, 21)
    lookback = v_pos_default(lookback, 2)
    close = v_series(close, max(fast, slow, lookback))

    if close is None:
        return

    mamode = v_mamode(mamode, "ema")
    offset = v_offset(offset)
    if "length" in kwargs:
        kwargs.pop("length")

    # Calculate
    fast_ma = ma(mamode, close, length=fast, **kwargs)
    slow_ma = ma(mamode, close, length=slow, **kwargs)

    mas_long = long_run(fast_ma, slow_ma, length=lookback)
    mas_short = short_run(fast_ma, slow_ma, length=lookback)

    # Offset
    if offset != 0:
        mas_long = mas_long.shift(offset)
        mas_short = mas_short.shift(offset)

    # Fill
    if "fillna" in kwargs:
        mas_long.fillna(kwargs["fillna"], inplace=True)
        mas_short.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        mas_long.fillna(method=kwargs["fill_method"], inplace=True)
        mas_short.fillna(method=kwargs["fill_method"], inplace=True)

    amatdf = DataFrame({
        f"AMAT{mamode[0]}_LR_{fast}_{slow}_{lookback}": mas_long,
        f"AMAT{mamode[0]}_SR_{fast}_{slow}_{lookback}": mas_short
    })

    # Name and Category
    amatdf.name = f"AMAT{mamode[0]}_{fast}_{slow}_{lookback}"
    amatdf.category = "trend"

    return amatdf
