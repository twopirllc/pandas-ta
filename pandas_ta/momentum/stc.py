# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.overlap import ema
from pandas_ta.utils import non_zero_range, v_offset
from pandas_ta.utils import v_pos_default, v_series


def stc(
    close: Series, tclength: Int = None,
    fast: Int = None, slow: Int = None, factor: IntFloat = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Schaff Trend Cycle (STC)

    The Schaff Trend Cycle is an evolution of the popular MACD
    incorportating two cascaded stochastic calculations with additional
    smoothing.

    The STC returns also the beginning MACD result as well as the result
    after the first stochastic including its smoothing. This implementation
    has been extended for Pandas TA to also allow for separatly feeding any
    other two moving Averages (as ma1 and ma2) or to skip this to feed an
    oscillator, based on which the Schaff Trend Cycle should be calculated.

    Feed external moving averages:
    Internally calculation..
        stc = ta.stc(close=df["close"], tclen=stc_tclen, fast=ma1_interval, slow=ma2_interval, factor=stc_factor)
    becomes..
        extMa1 = df.ta.zlma(close=df["close"], length=ma1_interval, append=True)
        extMa2 = df.ta.ema(close=df["close"], length=ma2_interval, append=True)
        stc = ta.stc(close=df["close"], tclen=stc_tclen, ma1=extMa1, ma2=extMa2, factor=stc_factor)

    The same goes for osc=, which allows the input of an externally
    calculated oscillator, overriding ma1 & ma2.

    Coded by rengel8

    Sources:
        https://www.prorealcode.com/prorealtime-indicators/schaff-trend-cycle2/

    Args:
        close (pd.Series): Series of 'close's
        tclen (int): SchaffTC Signal-Line length.
            Default: 10 (adjust to the half of cycle)
        fast (int): The short period. Default: 12
        slow (int): The long period. Default: 26
        factor (float): smoothing factor for last stoch. calculation.
            Default: 0.5
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        ma1: External MA (mandatory in conjuction with ma2)
        ma2: External MA (mandatory in conjuction with ma1)
        osc: External osillator
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: stc, macd, stoch
    """
    # Validate
    fast = v_pos_default(fast, 12)
    slow = v_pos_default(slow, 26)
    tclength = v_pos_default(tclength, 10)
    if slow < fast:                # mandatory condition, but might be confusing
        fast, slow = slow, fast
    _length = max(tclength, fast, slow)
    close = v_series(close, _length)

    if close is None:
        return

    factor = v_pos_default(factor, 0.5)
    offset = v_offset(offset)

    # Calculate
    # kwargs allows for three more series (ma1, ma2 and osc) which can be passed
    # here ma1 and ma2 input negate internal ema calculations, osc substitutes
    # both ma's.
    ma1 = kwargs.pop("ma1", False)
    ma2 = kwargs.pop("ma2", False)
    osc = kwargs.pop("osc", False)

    # 3 different modes of calculation..
    if isinstance(ma1, Series) and isinstance(ma2, Series) and not osc:
        ma1 = v_series(ma1, _length)
        ma2 = v_series(ma2, _length)

        if ma1 is None or ma2 is None:
            return
        # According to external feeded series
        xmacd = ma1 - ma2
        pff, pf = schaff_tc(close, xmacd, tclength, factor)
    elif isinstance(osc, Series):
        osc = v_series(osc, _length)
        if osc is None:
            return
        # According to feeded oscillator (should be ranging around 0 x-axis)
        xmacd = osc
        pff, pf = schaff_tc(close, xmacd, tclength, factor)
    else:
        # MACD (traditional/full)
        fastma = ema(close, length=fast)
        slowma = ema(close, length=slow)
        xmacd = fastma - slowma
        pff, pf = schaff_tc(close, xmacd, tclength, factor)

    stc = Series(pff, index=close.index)
    macd = Series(xmacd, index=close.index)
    stoch = Series(pf, index=close.index)

    # Offset
    if offset != 0:
        stc = stc.shift(offset)
        macd = macd.shift(offset)
        stoch = stoch.shift(offset)

    # Fill
    if "fillna" in kwargs:
        stc.fillna(kwargs["fillna"], inplace=True)
        macd.fillna(kwargs["fillna"], inplace=True)
        stoch.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        stc.fillna(method=kwargs["fill_method"], inplace=True)
        macd.fillna(method=kwargs["fill_method"], inplace=True)
        stoch.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _props = f"_{tclength}_{fast}_{slow}_{factor}"
    stc.name = f"STC{_props}"
    macd.name = f"STCmacd{_props}"
    stoch.name = f"STCstoch{_props}"
    stc.category = macd.category = stoch.category = "momentum"

    data = {stc.name: stc, macd.name: macd, stoch.name: stoch}
    df = DataFrame(data)
    df.name = f"STC{_props}"
    df.category = stc.category

    return df


def schaff_tc(close, xmacd, tclength, factor):
    # ACTUAL Calculation part, which is shared between operation modes
    # 1St : Stochastic of MACD
    lowest_xmacd = xmacd.rolling(tclength).min()  # min value in interval tclen
    xmacd_range = non_zero_range(xmacd.rolling(tclength).max(), lowest_xmacd)
    m = len(xmacd)

    # %Fast K of MACD
    stoch1, pf = list(xmacd), list(xmacd)
    stoch1[0], pf[0] = 0, 0
    for i in range(1, m):
        if lowest_xmacd[i] > 0:
            stoch1[i] = 100 * ((xmacd[i] - lowest_xmacd[i]) / xmacd_range[i])
        else:
            stoch1[i] = stoch1[i - 1]
        # Smoothed Calculation for % Fast D of MACD
        pf[i] = round(pf[i - 1] + (factor * (stoch1[i] - pf[i - 1])), 8)

    pf = Series(pf, index=close.index)

    # 2nd : Stochastic of smoothed Percent Fast D, 'PF', above
    lowest_pf = pf.rolling(tclength).min()
    pf_range = non_zero_range(pf.rolling(tclength).max(), lowest_pf)

    # % of Fast K of PF
    stoch2, pff = list(xmacd), list(xmacd)
    stoch2[0], pff[0] = 0, 0
    for i in range(1, m):
        if pf_range[i] > 0:
            stoch2[i] = 100 * ((pf[i] - lowest_pf[i]) / pf_range[i])
        else:
            stoch2[i] = stoch2[i - 1]
        # Smoothed Calculation for % Fast D of PF
        pff[i] = round(pff[i - 1] + (factor * (stoch2[i] - pff[i - 1])), 8)

    return pff, pf
