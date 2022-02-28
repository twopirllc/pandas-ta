# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.overlap import sma
from pandas_ta.utils import v_bool, v_offset, v_pos_default, v_series


def dpo(
    close: Series, length: Int = None, centered: bool = True,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Detrend Price Oscillator (DPO)

    Is an indicator designed to remove trend from price and make it easier to
    identify cycles.

    Sources:
        https://www.tradingview.com/scripts/detrendedpriceoscillator/
        https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dpo
        http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:detrended_price_osci

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 1
        centered (bool): Shift the dpo back by int(0.5 * length) + 1.
            Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 20)
    close = v_series(close, length)

    if close is None:
        return

    centered = v_bool(centered, True)
    offset = v_offset(offset)
    if not kwargs.get("lookahead", True):
        centered = False

    # Calculate
    t = int(0.5 * length) + 1
    ma = sma(close, length)

    dpo = close - ma.shift(t)
    if centered:
        dpo = (close.shift(t) - ma).shift(-t)

    # Offset
    if offset != 0:
        dpo = dpo.shift(offset)

    # Fill
    if "fillna" in kwargs:
        dpo.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        dpo.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    dpo.name = f"DPO_{length}"
    dpo.category = "trend"

    return dpo
