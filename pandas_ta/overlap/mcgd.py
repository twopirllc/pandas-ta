# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import v_offset, v_pos_default, v_series


def mcgd(
    close: Series, length: Int = None, c: IntFloat = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """McGinley Dynamic Indicator

    The McGinley Dynamic looks like a moving average line, yet it is
    actually a smoothing mechanism for prices that minimizes price
    separation, price whipsaws, and hugs prices much more closely. Because
    of the calculation, the Dynamic Line speeds up in down markets as it
    follows prices yet moves more slowly in up markets. The indicator was
    designed by John R. McGinley, a Certified Market Technician and former
    editor of the Market Technicians Association's Journal of Technical
    Analysis.

    Sources:
        https://www.investopedia.com/articles/forex/09/mcginley-dynamic-indicator.asp

    Args:
        close (pd.Series): Series of 'close's
        length (int): Indicator's period. Default: 10
        c (float): Multiplier for the denominator, sometimes set to 0.6.
            Default: 1
        offset (int): Number of periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 10)
    close = v_series(close, length)

    if close is None:
        return

    c = float(c) if isinstance(c, float) and 0 < c <= 1 else 1
    offset = v_offset(offset)

    # Calculate
    close = close.copy()

    def mcg_(series):
        denom = (c * length * (series[1] / series[0]) ** 4)
        series[1] = (series[0] + ((series[1] - series[0]) / denom))
        return series[1]

    mcg_cell = close[0:].rolling(2, min_periods=2).apply(mcg_, raw=True)
    mcg_ds = close[:1].append(mcg_cell[1:])

    # Offset
    if offset != 0:
        mcg_ds = mcg_ds.shift(offset)

    # Fill
    if "fillna" in kwargs:
        mcg_ds.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        mcg_ds.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    mcg_ds.name = f"MCGD_{length}"
    mcg_ds.category = "overlap"

    return mcg_ds
