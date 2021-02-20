# -*- coding: utf-8 -*-
from pandas import DataFrame
from pandas_ta.overlap import hlc3
from pandas_ta.utils import get_drift, get_offset, verify_series


def mfi(high, low, close, volume, length=None, drift=None, offset=None, **kwargs):
    """Indicator: Money Flow Index (MFI)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    volume = verify_series(volume)
    length = int(length) if length and length > 0 else 14
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    typical_price = hlc3(high=high, low=low, close=close)
    raw_money_flow = typical_price * volume

    tdf = DataFrame({"diff": 0, "rmf": raw_money_flow, "+mf": 0, "-mf": 0})

    tdf.loc[(typical_price.diff(drift) > 0), "diff"] = 1
    tdf.loc[tdf["diff"] == 1, "+mf"] = raw_money_flow

    tdf.loc[(typical_price.diff(drift) < 0), "diff"] = -1
    tdf.loc[tdf["diff"] == -1, "-mf"] = raw_money_flow

    psum = tdf["+mf"].rolling(length).sum()
    nsum = tdf["-mf"].rolling(length).sum()
    tdf["mr"] = psum / nsum
    mfi = 100 * psum / (psum + nsum)
    tdf["mfi"] = mfi

    # Offset
    if offset != 0:
        mfi = mfi.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        mfi.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        mfi.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    mfi.name = f"MFI_{length}"
    mfi.category = "volume"

    return mfi


mfi.__doc__ = \
"""Money Flow Index (MFI)

Money Flow Index is an oscillator indicator that is used to measure buying and
selling pressure by utilizing both price and volume.

Sources:
    https://www.tradingview.com/wiki/Money_Flow_(MFI)

Calculation:
    Default Inputs:
        length=14, drift=1
    tp = typical_price = hlc3 = (high + low + close) / 3
    rmf = raw_money_flow = tp * volume

    pmf = pos_money_flow = SUM(rmf, length) if tp.diff(drift) > 0 else 0
    nmf = neg_money_flow = SUM(rmf, length) if tp.diff(drift) < 0 else 0

    MFR = money_flow_ratio = pmf / nmf
    MFI = money_flow_index = 100 * pmf / (pmf + nmf)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    length (int): The sum period. Default: 14
    drift (int): The difference period. Default: 1
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
