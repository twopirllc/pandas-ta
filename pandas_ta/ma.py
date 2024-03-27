# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike
from pandas_ta.overlap.dema import dema
from pandas_ta.overlap.ema import ema
from pandas_ta.overlap.fwma import fwma
from pandas_ta.overlap.hma import hma
from pandas_ta.overlap.linreg import linreg
from pandas_ta.overlap.midpoint import midpoint
from pandas_ta.overlap.pwma import pwma
from pandas_ta.overlap.rma import rma
from pandas_ta.overlap.sinwma import sinwma
from pandas_ta.overlap.sma import sma
from pandas_ta.overlap.ssf import ssf
from pandas_ta.overlap.swma import swma
from pandas_ta.overlap.t3 import t3
from pandas_ta.overlap.tema import tema
from pandas_ta.overlap.trima import trima
from pandas_ta.overlap.vidya import vidya
from pandas_ta.overlap.wma import wma



def ma(name: str = None, source: Series = None, **kwargs: DictLike) -> Series:
    """Simple MA Utility for easier MA selection

    Available MAs:
        dema, ema, fwma, hma, linreg, midpoint, pwma, rma, sinwma, sma, ssf,
        swma, t3, tema, trima, vidya, wma

    Examples:
        ema8 = ta.ma("ema", df.close, length=8)
        sma50 = ta.ma("sma", df.close, length=50)
        pwma10 = ta.ma("pwma", df.close, length=10, asc=False)

    Args:
        name (str): One of the Available MAs. Default: "ema"
        source (pd.Series): The 'source' Series.

    Kwargs:
        Any additional kwargs the MA may require.

    Returns:
        pd.Series: New feature generated.
    """
    _mas = [
        "dema", "ema", "fwma", "hma", "linreg", "midpoint", "pwma", "rma",
        "sinwma", "sma", "ssf", "swma", "t3", "tema", "trima", "vidya", "wma"
    ]
    if name is None and source is None:
        return _mas
    elif isinstance(name, str) and name.lower() in _mas:
        name = name.lower()
    else:  # "ema"
        name = _mas[1]

    if   name == "dema": return dema(source, **kwargs)
    elif name == "fwma": return fwma(source, **kwargs)
    elif name == "hma": return hma(source, **kwargs)
    elif name == "linreg": return linreg(source, **kwargs)
    elif name == "midpoint": return midpoint(source, **kwargs)
    elif name == "pwma": return pwma(source, **kwargs)
    elif name == "rma": return rma(source, **kwargs)
    elif name == "sinwma": return sinwma(source, **kwargs)
    elif name == "sma": return sma(source, **kwargs)
    elif name == "ssf": return ssf(source, **kwargs)
    elif name == "swma": return swma(source, **kwargs)
    elif name == "t3": return t3(source, **kwargs)
    elif name == "tema": return tema(source, **kwargs)
    elif name == "trima": return trima(source, **kwargs)
    elif name == "vidya": return vidya(source, **kwargs)
    elif name == "wma": return wma(source, **kwargs)
    else: return ema(source, **kwargs)
