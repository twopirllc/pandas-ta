from numpy import NaN, select
from pandas import DataFrame, to_datetime, infer_freq,Series
from pandas_ta.utils import v_datetime_ordered, v_series
import pandas as pd
from pandas_ta._typing import DictLike, Int, IntFloat



def pivots(open_, high, low, close, anchor=None, method=None,**kwargs: DictLike
) -> Series:
    open_ = v_series(open_)
    high = v_series(high)
    low = v_series(low)
    close = v_series(close)
    anchor = (
        anchor.upper()
        if anchor and isinstance(anchor, str) and len(anchor) >= 1
        else "D"
    )
    method_list = [
        "traditional",
        "fibonacci",
        "woodie",
        "classic",
        "demark",
        "camarilla",
    ]
    method = method if method in method_list else "traditional"
    date = (
        to_datetime(close.index, unit="ms")
        if not v_datetime_ordered(close) and v_series(close)
        else close.index
    )

    freq = infer_freq(date)
    # print(freq)
    # print(anchor)
    # print(date)
    df = DataFrame(
        index=date,
        data={
            "open": open_.values,
            "high": high.values,
            "low": low.values,
            "close": close.values,
        },
    )

    if freq is not anchor:
        a = DataFrame()
        a["open"] = df["open"].resample(anchor).first()
        a["high"] = df["high"].resample(anchor).max()
        a["low"] = df["low"].resample(anchor).min()
        a["close"] = df["close"].resample(anchor).last()
    else:
        a = df

    # print(a.tail())
    # return a

    # Calculate the Pivot Points
    if method == "traditional":
        a["p"] = (a.high.values + a.low.values + a.close.values) / 3

        a["bc"] = (a.high.values + a.low.values) / 2
        a["tc"] = (2 * a.p.values) - a.bc.values
        a["rng"] = abs(a.tc.values - a.bc.values) / a.p.values * 100

        a["s1"] = (2 * a.p.values) - a.high.values
        a["s2"] = a.p.values - (a.high.values - a.low.values)
        a["s3"] = a.p.values - (a.high.values - a.low.values) * 2
        a["r1"] = (2 * a.p.values) - a.low.values
        a["r2"] = a.p.values + (a.high.values - a.low.values)
        a["r3"] = a.p.values + (a.high.values - a.low.values) * 2

    elif method == "fibonacci":
        a["p"] = (a.high.values + a.low.values + a.close.values) / 3
        a["pivot_range"] = a.high.values - a.low.values
        a["s1"] = a.p.values - 0.382 * a.pivot_range.values
        a["s2"] = a.p.values - 0.618 * a.pivot_range.values
        a["s3"] = a.p.values - 1 * a.pivot_range.values
        a["r1"] = a.p.values + 0.382 * a.pivot_range.values
        a["r2"] = a.p.values + 0.618 * a.pivot_range.values
        a["r3"] = a.p.values + 1 * a.pivot_range.values
        a.drop(["pivot_range"], axis=1, inplace=True)
    elif method == "woodie":
        a["pivot_range"] = a.high.values - a.low.values
        a["p"] = (a.high.values + a.low.values + a.open.values * 2) / 4
        a["s1"] = a.p.values * 2 - a.high.values
        a["s2"] = a.p.values - 1 * a.pivot_range.values
        a["s3"] = a.high.values + 2 * (a.p.values - a.low.values)
        a["s4"] = a.s3 - a.p.values
        a["r1"] = a.p.values * 2 - a.low.values
        a["r2"] = a.p.values + 1 * a.pivot_range.values
        a["r3"] = a.low.values - 2 * (a.high.values - a.p.values)
        a["r4"] = a.r3 + a.p.values
        a.drop(["pivot_range"], axis=1, inplace=True)
    elif method == "classic":
        a["p"] = (a.high.values + a.low.values + a.close.values) / 3
        a["pivot_range"] = a.high.values - a.low.values
        a["s1"] = a.p.values * 2 - a.high.values
        a["s2"] = a.p.values - 1 * a.pivot_range.values
        a["s3"] = a.p.values - 2 * a.pivot_range.values
        a["s4"] = a.p.values - 3 * a.pivot_range.values
        a["r1"] = a.p.values * 2 - a.low.values
        a["r2"] = a.p.values + 1 * a.pivot_range.values
        a["r3"] = a.p.values + 2 * a.pivot_range.values
        a["r4"] = a.p.values + 3 * a.pivot_range.values
        a.drop(["pivot_range"], axis=1, inplace=True)
    elif method == "demark":
        conds = (
            a.close.values == a.open.values,
            a.close.values > a.open.values,
        )
        vals = (
            a.high.values + a.low.values + a.close.values * 2,
            a.high.values * 2 + a.low.values + a.close.values,
        )
        p = select(
            conds, vals, default=(a.high.values + a.low.values * 2 + a.close.values)
        )
        a["p"] = p / 4
        a["s1"] = p / 2 - a.high.values
        a["r1"] = p / 2 - a.low.values
    elif method == "camarilla":
        a["p"] = (a.high.values + a.low.values + a.close.values) / 3
        a["pivot_range"] = a.high.values - a.low.values
        a["s1"] = a.close.values - a.pivot_range.values * 1.1 / 12
        a["s2"] = a.close.values - a.pivot_range.values * 1.1 / 6
        a["s3"] = a.close.values - a.pivot_range.values * 1.1 / 4
        a["s4"] = a.close.values - a.pivot_range.values * 1.1 / 2
        a["r1"] = a.close.values + a.pivot_range.values * 1.1 / 12
        a["r2"] = a.close.values + a.pivot_range.values * 1.1 / 6
        a["r3"] = a.close.values + a.pivot_range.values * 1.1 / 4
        a["r4"] = a.close.values + a.pivot_range.values * 1.1 / 2
        a.drop(["pivot_range"], axis=1, inplace=True)
    else:
        raise ValueError("Invalid method")

    a.index = a.index + pd.Timedelta(1, anchor.lower())
    if freq is not anchor:
        pivots_df = a.reindex(df.index, method="ffill")
    else:
        pivots_df = a

    pivots_df.drop(columns=["open", "high", "low", "close"], inplace=True)

    # x = (
    #     pivots_df.loc[lambda x: (x.index.hour == 23) & (x.index.minute == 59)]
    #     .iloc[0]
    #     .name
    # )
    # pivots_df.loc[:x] = NaN

    return pivots_df
