# -*- coding: utf-8 -*-
from numpy import full, nan, zeros
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
    sar = zeros(m)
    long = full(m, nan)
    short = full(m, nan)
    reversal = zeros(m, dtype=int)
    _af = zeros(m)
    _af[:2] = af0
    falling = _falling(orig_high.iloc[:2], orig_low.iloc[:2])
    ep = low[0] if falling else high[0]
    if close is not None:
        close = v_series(close)
        sar[0] = close.iloc[0]
    else:
        sar[0] = high[0] if falling else low[0]

    # Calculate
    for i in range(1, m):
        sar[i] = sar[i - 1] + af * (ep - sar[i - 1])

        if falling:
            reverse = high[i] > sar[i]
            if low[i] < ep:
                ep = low[i]
                af = min(af + af0, max_af)
            sar[i] = max(high[i - 1], sar[i])
        else:
            reverse = low[i] < sar[i]
            if high[i] > ep:
                ep = high[i]
                af = min(af + af0, max_af)
            sar[i] = min(low[i - 1], sar[i])

        if reverse:
            sar[i] = ep
            af = af0
            falling = not falling
            ep = low[i] if falling else high[i]

        # Separate long/short SAR based on falling
        if falling:
            short[i] = sar[i]
        else:
            long[i] = sar[i]

        _af[i] = af
        reversal[i] = int(reverse)

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

    _props = f"_{af0}_{max_af}"
    data = {
        f"PSARl{_props}": long,
        f"PSARs{_props}": short,
        f"PSARaf{_props}": _af,
        f"PSARr{_props}": reversal
    }
    df = DataFrame(data, index=orig_high.index)
    df.name = f"PSAR{_props}"
    df.category = long.category = short.category = "trend"

    return df


def _falling(high, low, drift: int = 1):
    """Returns the last -DM value"""
    # Not to be confused with ta.falling()
    up = high - high.shift(drift)
    dn = low.shift(drift) - low
    _dmn = (((dn > up) & (dn > 0)) * dn).apply(zero).iloc[-1]
    return _dmn > 0
