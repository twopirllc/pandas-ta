# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.utils import get_offset, verify_series
from .dema import dema
from .ema import ema
from .fwma import fwma
from .hma import hma
from .linreg import linreg
from .midpoint import midpoint
from .pwma import pwma
from .rma import rma
from .sinwma import sinwma
from .sma import sma
from .ssf import ssf
from .swma import swma
from .t3 import t3
from .tema import tema
from .trima import trima
from .vidya import vidya
from .wma import wma


def zlma(
        close: Series, length: int = None, mamode: str = None,
        offset: int = None, **kwargs
    ) -> Series:
    """Zero Lag Moving Average (ZLMA)

    The Zero Lag Moving Average attempts to eliminate the lag associated
    with moving averages.  This is an adaption created by John Ehler and Ric Way.

    Sources:
        https://en.wikipedia.org/wiki/Zero_lag_exponential_moving_average

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
    # Validate
    length = int(length) if length and length > 0 else 10
    mamode = mamode.lower() if isinstance(mamode, str) else "ema"
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None: return

    # Calculate
    lag = int(0.5 * (length - 1))
    close_ = 2 * close - close.shift(lag)

    kwargs.update({"close": close_})
    kwargs.update({"length": length})

    # Not ideal but it works. Submit a PR for a better solution. =)
    # This design pattern is undesirable
    def _ma(**kwargs):
        if   mamode == "dema":      return dema(**kwargs)
        elif mamode == "fwma":      return fwma(**kwargs)
        elif mamode == "hma":       return hma(**kwargs)
        elif mamode == "linreg":    return linreg(**kwargs)
        elif mamode == "midpoint":  return midpoint(**kwargs)
        elif mamode == "pwma":      return pwma(**kwargs)
        elif mamode == "rma":       return rma(**kwargs)
        elif mamode == "sinwma":    return sinwma(**kwargs)
        elif mamode == "sma":       return sma(**kwargs)
        elif mamode == "ssf":       return ssf(**kwargs)
        elif mamode == "swma":      return swma(**kwargs)
        elif mamode == "t3":        return t3(**kwargs)
        elif mamode == "tema":      return tema(**kwargs)
        elif mamode == "trima":     return trima(**kwargs)
        elif mamode == "vidya":     return vidya(**kwargs)
        elif mamode == "wma":       return wma(**kwargs)
        else:                       return ema(**kwargs)

    zlma = _ma(**kwargs)

    # Offset
    if offset != 0:
        zlma = zlma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        zlma.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        zlma.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    zlma.name = f"ZL_{zlma.name}"
    zlma.category = "overlap"

    return zlma
