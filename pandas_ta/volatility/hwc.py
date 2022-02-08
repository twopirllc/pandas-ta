# -*- coding: utf-8 -*-
from numpy import sqrt
from pandas import DataFrame, Series
from pandas_ta.utils import get_offset, verify_series


def hwc(
    close: Series, scalar: float = None, channel_eval: bool = None,
    na: float = None, nb: float = None, nc: float = None, nd: float = None,
    offset: int = None, **kwargs
) -> DataFrame:
    """HWC (Holt-Winter Channel)

    Channel indicator HWC (Holt-Winters Channel) based on HWMA - a three-parameter
    moving average calculated by the method of Holt-Winters.

    This version has been implemented for Pandas TA by rengel8 based on a
    publication for MetaTrader 5 extended by width and percentage price position
    against width of channel.

    Sources:
        https://www.mql5.com/en/code/20857

    Args:
        close (pd.Series): Series of 'close's
        scaler (float): Width multiplier of the channel. Default: 1
        channel_eval (bool): Return width and percentage price position against
            price. Default: False
        na (float): Smoothed series (from 0 to 1). Default: 0.2
        nb (float): Trend value (from 0 to 1). Default: 0.1
        nc (float): Seasonality value (from 0 to 1). Default: 0.1
        nd (float): Channel value (from 0 to 1). Default: 0.1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: HWM (Mid), HWU (Upper), HWL (Lower) columns.
    """
    # Validate
    na = float(na) if na and na > 0 else 0.2
    nb = float(nb) if nb and nb > 0 else 0.1
    nc = float(nc) if nc and nc > 0 else 0.1
    nd = float(nd) if nd and nd > 0 else 0.1
    scalar = float(scalar) if scalar and scalar > 0 else 1
    if isinstance(channel_eval, bool) and channel_eval:
        channel_eval = bool(channel_eval)
    else:
        channel_eval = False
    close = verify_series(close)
    offset = get_offset(offset)

    # Calculate Result
    last_a = last_v = last_var = 0
    last_f = last_price = last_result = close[0]
    lower, result, upper = [], [], []
    chan_pct_width, chan_width = [], []

    m = close.size
    for i in range(m):
        F = (1.0 - na) * (last_f + last_v + 0.5 * last_a) + na * close[i]
        V = (1.0 - nb) * (last_v + last_a) + nb * (F - last_f)
        A = (1.0 - nc) * last_a + nc * (V - last_v)
        result.append((F + V + 0.5 * A))

        var = (1.0 - nd) * last_var + \
            nd * (last_price - last_result) * (last_price - last_result)
        stddev = sqrt(last_var)
        upper.append(result[i] + scalar * stddev)
        lower.append(result[i] - scalar * stddev)

        if channel_eval:
            # channel width
            chan_width.append(upper[i] - lower[i])
            # channel percentage price position
            chan_pct_width.append((close[i] - lower[i]) / (upper[i] - lower[i]))

        # update values
        last_price = close[i]
        last_a = A
        last_f = F
        last_v = V
        last_var = var
        last_result = result[i]

    # Aggregate
    hwc = Series(result, index=close.index)
    hwc_upper = Series(upper, index=close.index)
    hwc_lower = Series(lower, index=close.index)
    if channel_eval:
        hwc_width = Series(chan_width, index=close.index)
        hwc_pctwidth = Series(chan_pct_width, index=close.index)

    # Offset
    if offset != 0:
        hwc = hwc.shift(offset)
        hwc_upper = hwc_upper.shift(offset)
        hwc_lower = hwc_lower.shift(offset)
        if channel_eval:
            hwc_width = hwc_width.shift(offset)
            hwc_pctwidth = hwc_pctwidth.shift(offset)

    # Fill
    if "fillna" in kwargs:
        hwc.fillna(kwargs["fillna"], inplace=True)
        hwc_upper.fillna(kwargs["fillna"], inplace=True)
        hwc_lower.fillna(kwargs["fillna"], inplace=True)
        if channel_eval:
            hwc_width.fillna(kwargs["fillna"], inplace=True)
            hwc_pctwidth.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        hwc.fillna(method=kwargs["fill_method"], inplace=True)
        hwc_upper.fillna(method=kwargs["fill_method"], inplace=True)
        hwc_lower.fillna(method=kwargs["fill_method"], inplace=True)
        if channel_eval:
            hwc_width.fillna(method=kwargs["fill_method"], inplace=True)
            hwc_pctwidth.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _props = f"_{scalar}"
    hwc.name = f"HWM{_props}"
    hwc_upper.name = f"HWU{_props}"
    hwc_lower.name = f"HWL{_props}"
    hwc.category = hwc_upper.category = hwc_lower.category = "volatility"

    if channel_eval:
        data = {
            hwc.name: hwc,
            hwc_upper.name: hwc_upper,
            hwc_lower.name: hwc_lower,
            f"HWW{_props}": hwc_width,
            f"HWPCT{_props}": hwc_pctwidth
        }
    else:
        data = {
            hwc.name: hwc,
            hwc_upper.name: hwc_upper,
            hwc_lower.name: hwc_lower
        }
    df = DataFrame(data)
    df.name = f"HWC_{scalar}"
    df.category = hwc.category

    return df
