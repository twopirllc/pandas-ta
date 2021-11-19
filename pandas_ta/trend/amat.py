# -*- coding: utf-8 -*-
from pandas import DataFrame
from .long_run import long_run
from .short_run import short_run
from pandas_ta.overlap import ma
from pandas_ta.utils import get_offset, verify_series


def amat(close=None, fast=None, slow=None, lookback=None, mamode=None, offset=None, **kwargs):
    """Archer Moving Averages Trends (AMAT)

    Archer Moving Averages Trends (AMAT) developed by Kevin Johnson provides
    creates both long run ```help(ta.long_run)``` and short run
    ```help(ta.short_run)``` trend signals given two moving average speeds,
    fast and slow. The long runs and short runs are binary Series where '1' is
    a trend and '0' is not a trend.

    Sources:
        https://www.tradingview.com/script/Z2mq63fE-Trade-Archer-Moving-Averages-v1-4F/

    Calculation:
        Default Inputs:
            fast=8, slow=21, mamode="ema", lookback=2
        OBV = On Balance Volume
        LR = Long Run Trend
        SR = Short Run Trend

        FMA = ma(close, mamode, fast)
        SMA = ma(close, mamode, slow)

        AMAT_LR = LR(FMA, SMA, lookback)
        AMAT_SR = SR(FMA, SMA, lookback)

    Args:
        close (pd.Series): Series of 'close's
        fast (int): The period of the fast moving average. Default: 8
        slow (int): The period of the slow moving average. Default: 21
        lookback (int): Lookback period for long_run and short_run. Default: 2
        mamode (str): See ```help(ta.ma)```. Default: 'ema'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        run_length (int): Trend length for OBV long and short runs. Default: 2
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: AMAT_LR, AMAT_SR columns.
    """
    # Validate Arguments
    fast = int(fast) if fast and fast > 0 else 8
    slow = int(slow) if slow and slow > 0 else 21
    lookback = int(lookback) if lookback and lookback > 0 else 2
    mamode = mamode.lower() if isinstance(mamode, str) else "ema"
    close = verify_series(close, max(fast, slow, lookback))
    offset = get_offset(offset)
    if "length" in kwargs: kwargs.pop("length")

    if close is None: return

    # # Calculate Result
    fast_ma = ma(mamode, close, length=fast, **kwargs)
    slow_ma = ma(mamode, close, length=slow, **kwargs)

    mas_long = long_run(fast_ma, slow_ma, length=lookback)
    mas_short = short_run(fast_ma, slow_ma, length=lookback)

    # Offset
    if offset != 0:
        mas_long = mas_long.shift(offset)
        mas_short = mas_short.shift(offset)

    # # Handle fills
    if "fillna" in kwargs:
        mas_long.fillna(kwargs["fillna"], inplace=True)
        mas_short.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        mas_long.fillna(method=kwargs["fill_method"], inplace=True)
        mas_short.fillna(method=kwargs["fill_method"], inplace=True)

    # Prepare DataFrame to return
    amatdf = DataFrame({
        f"AMAT{mamode[0]}_LR_{fast}_{slow}_{lookback}": mas_long,
        f"AMAT{mamode[0]}_SR_{fast}_{slow}_{lookback}": mas_short
    })

    # Name and Categorize it
    amatdf.name = f"AMAT{mamode[0]}_{fast}_{slow}_{lookback}"
    amatdf.category = "trend"

    return amatdf
