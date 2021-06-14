# -*- coding: utf-8 -*-
from numpy import NaN as npNaN
from pandas import DataFrame, Series
from pandas_ta.utils import get_offset, verify_series
from pandas_ta.momentum import dm


def psar(high, low, close=None, af0=None, af=None, max_af=None, offset=None, **kwargs):
    """Indicator: Parabolic Stop and Reverse (PSAR)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    af = float(af) if af and af > 0 else 0.02
    af0 = float(af0) if af0 and af0 > 0 else af
    max_af = float(max_af) if max_af and max_af > 0 else 0.2
    offset = get_offset(offset)

    _dm = dm(high, low, close)

    falling = _dm["-DM_1"].iloc[1] > 0
    if falling:
        sar = high.iloc[0]
        ep = low.iloc[0]
    else:
        sar = low.iloc[0]
        ep = high.iloc[0]

    if close is not None:
        close = verify_series(close)
        sar = close.iloc[0]

    long = Series(npNaN, index=high.index)
    short = long.copy()
    reversal = Series(False, index=high.index)
    _af = long.copy()
    _af.iloc[0:1] = af0

    m = high.shape[0]

    # Calculate Result
    for row in range(1, m):
        HIGH = high.iloc[row]
        LOW = low.iloc[row]

        if falling:
            new_sar = sar + af * (ep - sar)
            reverse = HIGH > new_sar

            if LOW < ep:
                ep = LOW
                af = min(af + af0, max_af)

            new_sar = max(high.iloc[row - 1], high.iloc[row - 2], new_sar)
        else:
            new_sar = sar + af * (ep - sar)
            reverse = LOW < new_sar

            if HIGH > ep:
                ep = HIGH
                af = min(af + af0, max_af)

            new_sar = min(low.iloc[row - 1], low.iloc[row - 2], new_sar)

        if reverse:
            new_sar = ep
            af = af0
            falling = not falling

            if falling:
                ep = LOW
            else:
                ep = HIGH

        sar = new_sar

        if not falling:
            long.iloc[row] = sar
        else:
            short.iloc[row] = sar

        _af.iloc[row] = af
        reversal.iloc[row] = reverse

    # Offset
    if offset != 0:
        _af = _af.shift(offset)
        long = long.shift(offset)
        short = short.shift(offset)
        reversal = reversal.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        _af.fillna(kwargs["fillna"], inplace=True)
        long.fillna(kwargs["fillna"], inplace=True)
        short.fillna(kwargs["fillna"], inplace=True)
        reversal.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        _af.fillna(method=kwargs["fill_method"], inplace=True)
        long.fillna(method=kwargs["fill_method"], inplace=True)
        short.fillna(method=kwargs["fill_method"], inplace=True)
        reversal.fillna(method=kwargs["fill_method"], inplace=True)

    # Prepare DataFrame to return
    _params = f"_{af0}_{max_af}"
    data = {
        f"PSARl{_params}": long,
        f"PSARs{_params}": short,
        f"PSARaf{_params}": _af,
        f"PSARr{_params}": reversal,
    }
    psardf = DataFrame(data)
    psardf.name = f"PSAR{_params}"
    psardf.category = long.category = short.category = "trend"

    return psardf


psar.__doc__ = \
"""Parabolic Stop and Reverse (psar)

Parabolic Stop and Reverse

Calculation:
    Default Inputs:
        af0=0.02, af=0.02, max_af=0.2

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series, optional): Series of 'close's. Optional
    af0 (float): Initial Acceleration Factor. Default: 0.02
    af (float): Acceleration Factor. Default: 0.02
    max_af (float): Maximum Acceleration Factor. Default: 0.2
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: long, short, af, and reversal columns.
"""
