# -*- coding: utf-8 -*-
from numpy import NaN as npNaN
from pandas import DataFrame
from pandas_ta.utils import get_offset, verify_series, get_drift, zero


def dm(high, low, drift=None, offset=None, **kwargs):
    """Indicator: DM"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    drift = get_drift(drift)
    offset = get_offset(offset)

    if high is None or low is None:
        return

    up = high - high.shift(drift)
    dn = low.shift(drift) - low

    pos = ((up > dn) & (up > 0)) * up
    neg = ((dn > up) & (dn > 0)) * dn

    pos = pos.apply(zero)
    neg = neg.apply(zero)

    # Offset
    if offset != 0:
        pos = pos.shift(offset)
        neg = neg.shift(offset)

    _params = f"_{drift}"
    data = {
        f"+DM{_params}": pos,
        f"-DM{_params}": neg,
    }

    dmdf = DataFrame(data)
    dmdf.name = f"DM{_params}"
    dmdf.category = "trend"

    return dmdf


dm.__doc__ = \
    """Directional Movement (DM)

Directional Movement

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    drift (int): The difference period. Default: 1
    offset (int): How many periods to offset the result. Default: 0

Returns:
    pd.DataFrame: +DM and -DM columns.
"""
