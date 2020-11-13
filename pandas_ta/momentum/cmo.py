# -*- coding: utf-8 -*-
from pandas_ta.overlap import rma
from pandas_ta.utils import get_drift, get_offset, verify_series


def cmo(close, length=None, scalar=None, drift=None, offset=None, **kwargs):
    """Indicator: Chande Momentum Oscillator (CMO)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    scalar = float(scalar) if scalar else 100
    talib = kwargs.pop("talib", True)
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    mom = close.diff(drift)
    positive = mom.copy().clip(lower=0)
    negative = mom.copy().clip(upper=0).abs()

    if talib:
        pos_ = rma(positive, length)
        neg_ = rma(negative, length)
    else:
        pos_ = positive.rolling(length).sum()
        neg_ = negative.rolling(length).sum()

    cmo = scalar * (pos_ - neg_) / (pos_ + neg_)

    # Offset
    if offset != 0:
        cmo = cmo.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        cmo.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        cmo.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    cmo.name = f"CMO_{length}"
    cmo.category = "momentum"

    return cmo


cmo.__doc__ = \
"""Chande Momentum Oscillator (CMO)

Attempts to capture the momentum of an asset with overbought at 50 and
oversold at -50.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/chande-momentum-oscillator-cmo/
    https://www.tradingview.com/script/hdrf0fXV-Variable-Index-Dynamic-Average-VIDYA/

Calculation:
    Default Inputs:
        drift=1, scalar=100

    # Same Calculation as RSI except for this step
    CMO = scalar * (PSUM - NSUM) / (PSUM + NSUM)

Args:
    close (pd.Series): Series of 'close's
    scalar (float): How much to magnify. Default: 100
    drift (int): The short period. Default: 1
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    talib (bool): If True, uses TA-Libs implementation. Otherwise uses EMA version. Default: True
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
