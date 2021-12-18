# -*- coding: utf-8 -*-
from pandas import DataFrame
from pandas_ta.overlap import ma
from pandas_ta.volatility import atr
from pandas_ta.utils import get_drift, get_offset, verify_series, zero


def adx(high, low, close, length=None, lensig=None, scalar=None, mamode=None, drift=None, offset=None, **kwargs):
    """Average Directional Movement (ADX)

    Average Directional Movement is meant to quantify trend strength by measuring
    the amount of movement in a single direction.

    Sources:
        TA Lib Correlation: >99%
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/average-directional-movement-adx/

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 14
        lensig (int): Signal Length. Like TradingView's default ADX. Default: length
        scalar (float): How much to magnify. Default: 100
        mamode (str): See ```help(ta.ma)```. Default: 'rma'
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: adx, dmp, dmn columns.
    """
    # Validate Arguments
    length = length if length and length > 0 else 14
    lensig = lensig if lensig and lensig > 0 else length
    mamode = mamode if isinstance(mamode, str) else "rma"
    scalar = float(scalar) if scalar else 100
    high = verify_series(high, length)
    low = verify_series(low, length)
    close = verify_series(close, length)
    drift = get_drift(drift)
    offset = get_offset(offset)

    if high is None or low is None or close is None: return

    # Calculate Result
    atr_ = atr(high=high, low=low, close=close, length=length)

    up = high - high.shift(drift)  # high.diff(drift)
    dn = low.shift(drift) - low    # low.diff(-drift).shift(drift)

    pos = ((up > dn) & (up > 0)) * up
    neg = ((dn > up) & (dn > 0)) * dn

    pos = pos.apply(zero)
    neg = neg.apply(zero)

    k = scalar / atr_
    dmp = k * ma(mamode, pos, length=length)
    dmn = k * ma(mamode, neg, length=length)

    dx = scalar * (dmp - dmn).abs() / (dmp + dmn)
    adx = ma(mamode, dx, length=lensig)

    # Offset
    if offset != 0:
        dmp = dmp.shift(offset)
        dmn = dmn.shift(offset)
        adx = adx.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        adx.fillna(kwargs["fillna"], inplace=True)
        dmp.fillna(kwargs["fillna"], inplace=True)
        dmn.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        adx.fillna(method=kwargs["fill_method"], inplace=True)
        dmp.fillna(method=kwargs["fill_method"], inplace=True)
        dmn.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    adx.name = f"ADX_{lensig}"
    dmp.name = f"DMP_{length}"
    dmn.name = f"DMN_{length}"

    adx.category = dmp.category = dmn.category = "trend"

    # Prepare DataFrame to return
    data = {adx.name: adx, dmp.name: dmp, dmn.name: dmn}
    adxdf = DataFrame(data)
    adxdf.name = f"ADX_{lensig}"
    adxdf.category = "trend"

    return adxdf
