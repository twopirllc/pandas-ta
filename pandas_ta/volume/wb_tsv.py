# -*- coding: utf-8 -*-
from numpy import isnan
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.utils import (
    signed_series,
    v_drift,
    v_mamode,
    v_pos_default,
    v_offset,
    v_series,
    zero
)



def wb_tsv(
    close: Series, volume: Series,
    length: Int = None, signal: Int = None,
    mamode: str = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Time Segmented Value (TSV)

    TSV is a proprietary technical indicator developed by Worden Brothers
    Inc., classified as an oscillator. It compares various time segments of
    both price and volume. It measures the amount money flowing at various
    time segments for price and time; similar to On Balance Volume. The zero
    line is called the baseline. Entry and exit points are commonly
    determined when crossing the baseline.

    Sources:
        https://www.tradingview.com/script/6GR4ht9X-Time-Segmented-Volume/
        https://help.tc2000.com/m/69404/l/747088-time-segmented-volume
        https://usethinkscript.com/threads/time-segmented-volume-for-thinkorswim.519/

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        length (int): It's period. Default: 18
        signal (int): It's avg period. Default: 10
        mamode (str): See ``help(ta.ma)``. Default: 'sma'
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: tsv, signal, ratio
    """
    # Validate
    length = v_pos_default(length, 18)
    signal = v_pos_default(signal, 10)
    _length = max(length, signal) + 1
    close = v_series(close, _length)

    if close is None:
        return

    mamode = v_mamode(mamode, "sma")
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    signed_volume = volume * signed_series(close, 1)     # > 0
    signed_volume[signed_volume < 0] = -signed_volume    # < 0
    signed_volume.apply(zero)                            # ~ 0
    cvd = signed_volume * close.diff(drift)

    tsv = cvd.rolling(length).sum()
    if all(isnan(tsv)):
        return  # Emergency Break
    signal_ = ma(mamode, tsv, length=signal)
    ratio = tsv / signal_

    # Offset
    if offset != 0:
        tsv = tsv.shift(offset)
        signal_ = signal.shift(offset)
        ratio = ratio.shift(offset)

    # Fill
    if "fillna" in kwargs:
        tsv.fillna(kwargs["fillna"], inplace=True)
        signal_.fillna(kwargs["fillna"], inplace=True)
        ratio.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"_{length}_{signal}"
    tsv.name = f"TSV{_props}"
    signal_.name = f"TSVs{_props}"
    ratio.name = f"TSVr{_props}"
    tsv.category = signal_.category = ratio.category = "volume"

    data = {tsv.name: tsv, signal_.name: signal_, ratio.name: ratio}
    df = DataFrame(data, index=close.index)
    df.name = f"TSV{_props}"
    df.category = tsv.category

    return df
