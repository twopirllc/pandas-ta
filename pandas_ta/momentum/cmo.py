# -*- coding: utf-8 -*-
from ..utils import get_drift, get_offset, verify_series

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
    negative = close.diff(drift)
    positive = negative.copy()

    positive[positive < 0] = 0  # Make negatives 0 for the postive series
    negative[negative > 0] = 0  # Make postives 0 for the negative series

    if talib:
        pos_ = positive.ewm(com=length, adjust=False).mean()
        neg_ = negative.ewm(com=length, adjust=False).mean().abs()
    else:
        pos_ = positive.rolling(length).sum()
        neg_ = negative.abs().rolling(length).sum()

    cmo = scalar * (pos_ - neg_)
    cmo /= pos_ + neg_

    # Offset
    if offset != 0:
        cmo = cmo.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        cmo.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        cmo.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    cmo.name = f"CMO_{length}"
    cmo.category = 'momentum'

    return cmo



cmo.__doc__ = \
"""Chande Momentum Oscillator (CMO)

Attempts to capture the momentum of an asset with overbought at 50 and
oversold at -50.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/chande-momentum-oscillator-cmo/

Calculation:
    Default Inputs:
        drift=1, scalar=100

    # Same Calculation as RSI except for this step
    CMO = scalar * (PSUM - NSUM) / (PSUM + NSUM)

Args:
    close (pd.Series): Series of 'close's
    scalar (float): How much to magnify.  Default: 100
    talib (bool): If True, uses TA-Libs implementation. Otherwise uses EMA version.  Default: True
    drift (int): The short period.  Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""