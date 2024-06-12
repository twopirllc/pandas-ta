# -*- coding: utf-8 -*-
from numpy import isnan, nan, zeros, zeros_like, floor
from numba import njit
from pandas import Series, DataFrame
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import (
    v_bool,
    v_offset,
    v_pos_default,
    v_series,
)


@njit(cache=True)
def nb_rolling_hl(np_high, np_low, window):
    extremums = 0
    m = np_high.size
    idx, value = zeros(m), zeros(m)
    kind = zeros(m)   # High Swing = 1, Low Swing = -1

    left = int(floor(window / 2))
    right = left + 1

    # sample_array = [*[left-window], *[center], *[right-window]]
    for i in range(left, m - right):
        low_center = np_low[i]
        high_center = np_high[i]
        low_window = np_low[i - left: i + right]
        high_window = np_high[i - left: i + right]

        if (low_center <= low_window).all():
            idx[extremums] = i
            kind[extremums] = -1
            value[extremums] = low_center
            extremums += 1

        if (high_center >= high_window).all():
            idx[extremums] = i
            kind[extremums] = 1
            value[extremums] = high_center
            extremums += 1

    return idx[:extremums], kind[:extremums], value[:extremums]


@njit(cache=True)
def nb_find_zigzags(idx, kind, value, deviation):
    rolling_len, zigzags = idx.size, 0

    idx = zeros_like(idx)
    zigzag_types = zeros_like(kind)
    zigzag_values = zeros_like(value)
    zigzag_dev = zeros(rolling_len)

    idx[zigzags] = idx[-1]
    zigzag_types[zigzags] = kind[-1]
    zigzag_values[zigzags] = value[-1]
    zigzag_dev[zigzags] = 0

    for i in range(rolling_len - 2, -1, -1):
        # last point in zigzag is bottom
        if zigzag_types[zigzags] == -1:
            if kind[i] == -1:
                if zigzag_values[zigzags] > value[i] and zigzags > 1:
                    current_deviation = (zigzag_values[zigzags - 1] - value[i]) / value[i]
                    idx[zigzags] = idx[i]
                    zigzag_types[zigzags] = kind[i]
                    zigzag_values[zigzags] = value[i]
                    zigzag_dev[zigzags - 1] = 100 * current_deviation
            else:
                current_deviation = (value[i] - zigzag_values[zigzags]) / value[i]
                if current_deviation > deviation / 100:
                    if idx[zigzags] == idx[i]:
                        continue
                    zigzags += 1
                    idx[zigzags] = idx[i]
                    zigzag_types[zigzags] = kind[i]
                    zigzag_values[zigzags] = value[i]
                    zigzag_dev[zigzags - 1] = 100 * current_deviation

        # last point in zigzag is peak
        else:
            if kind[i] == 1:
                if zigzag_values[zigzags] < value[i] and zigzags > 1:
                    current_deviation = (value[i] - zigzag_values[zigzags - 1]) / value[i]
                    idx[zigzags] = idx[i]
                    zigzag_types[zigzags] = kind[i]
                    zigzag_values[zigzags] = value[i]
                    zigzag_dev[zigzags - 1] = 100 * current_deviation
            else:
                current_deviation = (zigzag_values[zigzags] - value[i]) / value[i]
                if current_deviation > deviation / 100:
                    if idx[zigzags] == idx[i]:
                        continue
                    zigzags += 1
                    idx[zigzags] = idx[i]
                    zigzag_types[zigzags] = kind[i]
                    zigzag_values[zigzags] = value[i]
                    zigzag_dev[zigzags - 1] = 100 * current_deviation

    return idx[:zigzags + 1], zigzag_types[:zigzags + 1], \
        zigzag_values[:zigzags + 1], zigzag_dev[:zigzags + 1]


@njit(cache=True)
def nb_map_zigzag(zigzag_idx, zigzag_types, zigzag_values, zigzag_dev, candles_num):
    _values = zeros(candles_num)
    _types = zeros(candles_num)
    _dev = zeros(candles_num)

    for i, index in enumerate(zigzag_idx):
        _values[int(index)] = zigzag_values[i]
        _types[int(index)] = zigzag_types[i]
        _dev[int(index)] = zigzag_dev[i]

    for i in range(candles_num):
        if _types[i] == 0:
            _values[i] = nan
            _types[i] = nan
            _dev[i] = nan
    return _types, _values, _dev



def zigzag(
    high: Series, low: Series, close: Series = None,
    legs: int = None, deviation: IntFloat = None,
    retrace: bool = None, last_extreme: bool = None,
    offset: Int = None, **kwargs: DictLike
):
    """Zigzag (ZIGZAG)

    Zigzag attempts to filter out smaller price movments while highlighting
    trend direction. It does not predict future trends, but it does identify
    swing highs and lows. When 'deviation' is set to 10, it will ignore
    all price movements less than 10%; only price movements greater than 10%
    would be shown.

    Note: Zigzag lines are not permanent and a price reversal will create a
        new line.

    Sources:
        https://www.tradingview.com/support/solutions/43000591664-zig-zag/#:~:text=Definition,trader%20visual%20the%20price%20action.
        https://school.stockcharts.com/doku.php?id=technical_indicators:zigzag

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's. Default: None
        legs (int): Number of legs > 2. Default: 10
        deviation (float): Price Deviation Percentage for a reversal.
            Default: 5
        retrace (bool): Default: False
        last_extreme (bool): Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: swing, and swing_type (high or low).
    """
    # Validate
    _length = 0
    legs = _length = v_pos_default(legs, 10)
    high = v_series(high, _length + 1)
    low = v_series(low, _length + 1)

    if high is None or low is None:
        return

    if close is not None:
        close = v_series(close, _length + 1)
        np_close = close.to_numpy()
        if close is None:
            return

    deviation = v_pos_default(deviation, 5.0)
    retrace = v_bool(retrace, False)
    last_extreme = v_bool(last_extreme, True)
    offset = v_offset(offset)

    # Calculation
    np_high, np_low = high.to_numpy(), low.to_numpy()

    _rollings_idx, _rollings_types, _rollings_values = nb_rolling_hl(np_high, np_low, legs)

    _zigzags_idx, _zigzags_types, _zigzags_values, _zigzags_dev = \
        nb_find_zigzags(_rollings_idx, _rollings_types, _rollings_values, deviation=deviation)
    _types, _values, _dev = \
        nb_map_zigzag(_zigzags_idx, _zigzags_types, _zigzags_values, _zigzags_dev, len(high))

    # Offset
    if offset != 0:
        _types = _types.shift(offset)
        _values = _values.shift(offset)
        _dev = _dev.shift(offset)

    # Fill
    if "fillna" in kwargs:
        _types.fillna(kwargs["fillna"], inplace=True)
        _values.fillna(kwargs["fillna"], inplace=True)
        _dev.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        _types.fillna(method=kwargs["fill_method"], inplace=True)
        _values.fillna(method=kwargs["fill_method"], inplace=True)
        _dev.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _props = f"_{deviation}%_{legs}"
    data = {
        f"ZIGZAGt{_props}": _types,
        f"ZIGZAGv{_props}": _values,
        f"ZIGZAGd{_props}": _dev,
    }
    df = DataFrame(data, index=high.index)
    df.name = f"ZIGZAG{_props}"
    df.category = "trend"

    return df
