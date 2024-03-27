# -*- coding: utf-8 -*-
from pandas import DataFrame, RangeIndex, Timedelta, Series, concat, date_range
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_pos_default, v_series
from .midprice import midprice



def ichimoku(
    high: Series, low: Series, close: Series,
    tenkan: Int = None, kijun: Int = None, senkou: Int = None,
    include_chikou: bool = True,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Ichimoku Kinkō Hyō (ichimoku)

    Developed Pre WWII as a forecasting model for financial markets.

    WARNING: This function may leak future data when used for machine learning
        if include_chikou=True (default). Set lookahead=False to avoid data leakage.
        See https://github.com/twopirllc/pandas-ta/issues/60#.

    Sources:
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/ichimoku-ich/

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        tenkan (int): Tenkan period. Default: 9
        kijun (int): Kijun period. Default: 26
        senkou (int): Senkou period. Default: 52
        include_chikou (bool): Whether to include chikou component.
            Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        lookahead (value, optional): To prevent data leakage by
            the Chikou Span column, set to False.

    Returns:
        pd.DataFrame: Two DataFrames.
            For the visible period: spanA, spanB, tenkan_sen, kijun_sen,
                and chikou_span columns
            For the forward looking period: spanA and spanB columns
    """
    # Validate
    tenkan = v_pos_default(tenkan, 9)
    kijun = v_pos_default(kijun, 26)
    senkou = v_pos_default(senkou, 52)
    _length = max(tenkan, kijun, senkou)
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return None, None

    offset = v_offset(offset)
    if not kwargs.get("lookahead", True):
        include_chikou = False

    # Calculate
    tenkan_sen = midprice(high=high, low=low, length=tenkan)
    kijun_sen = midprice(high=high, low=low, length=kijun)
    span_a = 0.5 * (tenkan_sen + kijun_sen)
    span_b = midprice(high=high, low=low, length=senkou)

    # Copy Span A and B values before their shift
    _span_a = span_a[-kijun:].shift(-1).copy()
    _span_b = span_b[-kijun:].shift(-1).copy()

    span_a = span_a.shift(kijun - 1)
    span_b = span_b.shift(kijun - 1)
    chikou_span = close.shift(-kijun + 1)

    # Offset
    if offset != 0:
        tenkan_sen = tenkan_sen.shift(offset)
        kijun_sen = kijun_sen.shift(offset)
        span_a = span_a.shift(offset)
        span_b = span_b.shift(offset)
        chikou_span = chikou_span.shift(offset)

    # Fill
    if "fillna" in kwargs:
        span_a.fillna(kwargs["fillna"], inplace=True)
        span_b.fillna(kwargs["fillna"], inplace=True)
        chikou_span.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    span_a.name = f"ISA_{tenkan}"
    span_b.name = f"ISB_{kijun}"
    tenkan_sen.name = f"ITS_{tenkan}"
    kijun_sen.name = f"IKS_{kijun}"
    chikou_span.name = f"ICS_{kijun}"

    chikou_span.category = kijun_sen.category = tenkan_sen.category = "overlap"
    span_b.category = span_a.category = chikou_span

    # Prepare Ichimoku DataFrame
    data = {
        span_a.name: span_a,
        span_b.name: span_b,
        tenkan_sen.name: tenkan_sen,
        kijun_sen.name: kijun_sen,
    }
    if include_chikou:
        data[chikou_span.name] = chikou_span

    ichimokudf = DataFrame(data, index=close.index)
    ichimokudf.name = f"ICHIMOKU_{tenkan}_{kijun}_{senkou}"
    ichimokudf.category = "overlap"

    # Prepare Span DataFrame
    last = close.index[-1]
    if close.index.dtype == "int64":
        ext_index = RangeIndex(start=last + 1, stop=last + kijun + 1)
        spandf = DataFrame(index=ext_index, columns=[span_a.name, span_b.name])
        _span_a.index = _span_b.index = ext_index
    else:
        df_freq = close.index.value_counts().mode()[0]
        tdelta = Timedelta(df_freq, unit="d")
        new_dt = date_range(start=last + tdelta, periods=kijun, freq="B")
        spandf = DataFrame(index=new_dt, columns=[span_a.name, span_b.name])
        _span_a.index = _span_b.index = new_dt

    spandf[span_a.name] = _span_a
    spandf[span_b.name] = _span_b
    spandf.name = f"ICHISPAN_{tenkan}_{kijun}"
    spandf.category = "overlap"

    return ichimokudf, spandf
