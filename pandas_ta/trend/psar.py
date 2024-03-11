# -*- coding: utf-8 -*-
import numpy as np
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import v_offset, v_pos_default, v_series, zero

def psar(
    high: Series, low: Series, close: Series = None,
    af0: IntFloat = None, af: IntFloat = None, max_af: IntFloat = None, tv=False,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Parabolic Stop and Reverse (psar)

    Parabolic Stop and Reverse (PSAR) was developed by J. Wells Wilder, that
    is used to determine trend direction and it's potential reversals in
    price. PSAR uses a trailing stop and reverse method called "SAR," or stop
    and reverse, to identify possible entries and exits. It is also known
    as SAR.

    PSAR indicator typically appears on a chart as a series of dots, either
    above or below an asset's price, depending on the direction the price is
    moving. A dot is placed below the price when it is trending upward, and
    above the price when it is trending downward.

    Sources:
        https://www.tradingview.com/pine-script-reference/#fun_sar
        https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=66&Name=Parabolic

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
    # Validate
    _length = 1
    high = v_series(high, _length)
    low = v_series(low, _length)

    if high is None or low is None:
        return

    orig_high = high.copy()
    orig_low = low.copy()
    # Numpy arrays offer some performance improvements
    high, low = high.values, low.values

    paf = v_pos_default(af, 0.02) # paf is used to keep af from parameters
    af0 = v_pos_default(af0, paf)
    af = af0

    max_af = v_pos_default(max_af, 0.2)
    offset = v_offset(offset)

    # Set up
    m = high.size
    sar = np.zeros(m)
    long = np.full(m, np.nan)
    short = np.full(m, np.nan)
    reversal = np.zeros(m, dtype=int)
    _af = np.zeros(m)
    _af[:2] = af0
    falling = _falling(orig_high.iloc[:2], orig_low.iloc[:2])
    ep = low[0] if falling else high[0]
    if close is not None:
        close = v_series(close)
        sar[0] = close.iloc[0]
    else:
        sar[0] = high[0] if falling else low[0]

    # Calculate
    for row in range(1, m):
        sar[row] = sar[row-1] + af * (ep - sar[row-1])

        if falling:
            reverse = high[row] > sar[row]
            if low[row] < ep:
                ep = low[row]
                af = min(af + af0, max_af)
            sar[row] = max(high[row-1], sar[row])
        else:
            reverse = low[row] < sar[row]
            if high[row] > ep:
                ep = high[row]
                af = min(af + af0, max_af)
            sar[row] = min(low[row-1], sar[row])

        if reverse:
            sar[row] = ep
            af = af0
            falling = not falling
            ep = low[row] if falling else high[row]

        # Separate long/short SAR based on falling
        if falling:
            short[row] = sar[row]
        else:
            long[row] = sar[row]

        _af[row] = af
        reversal[row] = int(reverse)

    _af = Series(_af, index=orig_high.index)
    long = Series(long, index=orig_high.index)
    short = Series(short, index=orig_high.index)
    reversal = Series(reversal, index=orig_high.index)

    # Offset
    if offset != 0:
        _af = _af.shift(offset)
        long = long.shift(offset)
        short = short.shift(offset)
        reversal = reversal.shift(offset)

    # Fill
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

    _params = f"_{af0}_{max_af}"
    data = {
        f"PSARl{_params}": long,
        f"PSARs{_params}": short,
        f"PSARaf{_params}": _af,
        f"PSARr{_params}": reversal
    }
    df = DataFrame(data, index=orig_high.index)
    df.name = f"PSAR{_params}"
    df.category = long.category = short.category = "trend"

    return df

def _falling(high, low, drift: int = 1):
    """Returns the last -DM value"""
    # Not to be confused with ta.falling()
    up = high - high.shift(drift)
    dn = low.shift(drift) - low
    _dmn = (((dn > up) & (dn > 0)) * dn).apply(zero).iloc[-1]
    return _dmn > 0
