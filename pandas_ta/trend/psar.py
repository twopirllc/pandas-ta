# -*- coding: utf-8 -*-
from numpy import NaN as npNaN
from pandas import DataFrame, Series
from pandas_ta.utils import get_offset, verify_series


def psar(high, low, close=None, af0=None, af=None, max_af=None, offset=None, **kwargs):
    """Indicator: Parabolic Stop and Reverse (PSAR)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    start_af = float(af) if af and af > 0 else 0.02
    max_af = float(max_af) if max_af and max_af > 0 else 0.2
    offset = get_offset(offset)

    # Initialize
    m = high.shape[0]
    af0 = start_af if not af0 else float(af0)
    af = af0
    bullish = True
    high_point = high.iloc[0]
    low_point = low.iloc[0]

    if close is not None:
        close = verify_series(close)
        sar = close.copy()
    else:
        sar = low.copy()

    long = Series(npNaN, index=sar.index)
    short = long.copy()
    reversal = Series(False, index=sar.index)

    _af = long.copy()
    _af.iloc[0:2] = af0

    # Calculate Result
    for i in range(2, m):
        reverse = False
        _af.iloc[i] = af

        if bullish:
            sar.iloc[i] = sar.iloc[i - 1] + af * (high_point - sar.iloc[i - 1])

            if low.iloc[i] < sar.iloc[i]:
                bullish, reverse, af = False, True, af0
                sar.iloc[i] = high_point
                low_point = low.iloc[i]
        else:
            sar.iloc[i] = sar.iloc[i - 1] + af * (low_point - sar.iloc[i - 1])

            if high.iloc[i] > sar.iloc[i]:
                bullish, reverse, af = True, True, af0
                sar.iloc[i] = low_point
                high_point = high.iloc[i]

        reversal.iloc[i] = reverse

        if not reverse:
            if bullish:
                if high.iloc[i] > high_point:
                    high_point = high.iloc[i]
                    af = min(af + start_af, max_af)
                if low.iloc[i - 1] < sar.iloc[i]:
                    sar.iloc[i] = low.iloc[i - 1]
                if low.iloc[i - 2] < sar.iloc[i]:
                    sar.iloc[i] = low.iloc[i - 2]
            else:
                if low.iloc[i] < low_point:
                    low_point = low.iloc[i]
                    af = min(af + start_af, max_af)
                if high.iloc[i - 1] > sar.iloc[i]:
                    sar.iloc[i] = high.iloc[i - 1]
                if high.iloc[i - 2] > sar.iloc[i]:
                    sar.iloc[i] = high.iloc[i - 2]

        if bullish:
            long.iloc[i] = sar.iloc[i]
        else:
            short.iloc[i] = sar.iloc[i]

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

Source:
    https://github.com/virtualizedfrog/blog_code/blob/master/PSAR/psar.py

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
