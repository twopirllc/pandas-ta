# -*- coding: utf-8 -*-
# from . import (
    # dema, ema, hma, linreg, rma, sma, swma, t3, tema, trima, vidya, wma
# )
from pandas_ta.overlap import ma
from pandas_ta.utils import get_offset, verify_series


def zlma(close, length=None, mamode=None, offset=None, **kwargs):
    """Zero Lag Moving Average (ZLMA)

    The Zero Lag Moving Average attempts to eliminate the lag associated
    with moving averages.  This is an adaption created by John Ehler and Ric Way.

    Sources:
        https://en.wikipedia.org/wiki/Zero_lag_exponential_moving_average

    Calculation:
        Default Inputs:
            length=10, mamode=EMA
        EMA = Exponential Moving Average
        lag = int(0.5 * (length - 1))

        SOURCE = 2 * close - close.shift(lag)
        ZLMA = MA(kind=mamode, SOURCE, length)

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 10
        mamode (str): Options: 'ema', 'hma', 'sma', 'wma'. Default: 'ema'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate Arguments
    length = int(length) if length and length > 0 else 10
    mamode = mamode.lower() if isinstance(mamode, str) else "ema"
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None: return

    # Calculate Result
    lag = int(0.5 * (length - 1))
    close_ = 2 * close - close.shift(lag)
    zlma = ma(mamode, close_, length=length, **kwargs)

    # Offset
    if offset != 0:
        zlma = zlma.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        zlma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        zlma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
    zlma.name = f"ZL_{zlma.name}"
    zlma.category = "overlap"

    return zlma
