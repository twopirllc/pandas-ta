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


@njit
def np_rolling_hl(highs, lows, window_size):

    num_extremum = 0
    candles_len = len(highs)
    rollings_idx = zeros(candles_len)
    rollings_types = zeros(candles_len)
    rollings_values = zeros(candles_len)

    left_side, right_side = int(floor(window_size / 2)), int(floor(window_size / 2)) + 1
    for i in range(left_side, candles_len - right_side):  # sample_array = [*[left-window], *[center], *[right-window]]
        lows_center = lows[i]
        highs_center = highs[i]
        lows_window = lows[i - left_side: i + right_side]
        highs_window = highs[i - left_side: i + right_side]

        if (lows_center <= lows_window).all():
            rollings_idx[num_extremum] = i
            rollings_types[num_extremum] = -1  # This -1 means it's a low swing
            rollings_values[num_extremum] = lows_center
            num_extremum += 1
        if (highs_center >= highs_window).all():
            rollings_idx[num_extremum] = i
            rollings_types[num_extremum] = 1  # This 1 means it's a high swing
            rollings_values[num_extremum] = highs_center
            num_extremum += 1
    return rollings_idx[:num_extremum], rollings_types[:num_extremum], rollings_values[:num_extremum]


@njit
def np_find_zigzags(rolling_idx, rolling_types, rolling_values, deviation):
    rolling_len, num_zigzag = len(rolling_idx), 0

    zigzag_idx = zeros_like(rolling_idx)
    zigzag_types = zeros_like(rolling_types)
    zigzag_values = zeros_like(rolling_values)
    zigzag_dev = zeros(rolling_len)

    zigzag_idx[num_zigzag] = rolling_idx[-1]
    zigzag_types[num_zigzag] = rolling_types[-1]
    zigzag_values[num_zigzag] = rolling_values[-1]
    zigzag_dev[num_zigzag] = 0

    for i in range(rolling_len - 2, -1, -1):
        # last point in zigzag is bottom
        if zigzag_types[num_zigzag] == -1:
            if rolling_types[i] == -1:
                if zigzag_values[num_zigzag] > rolling_values[i] and num_zigzag > 1:
                    current_deviation = (zigzag_values[num_zigzag - 1] - rolling_values[i]) / rolling_values[i]
                    zigzag_idx[num_zigzag] = rolling_idx[i]
                    zigzag_types[num_zigzag] = rolling_types[i]
                    zigzag_values[num_zigzag] = rolling_values[i]
                    zigzag_dev[num_zigzag - 1] = 100 * current_deviation
            else:
                current_deviation = (rolling_values[i] - zigzag_values[num_zigzag]) / rolling_values[i]
                if current_deviation > deviation / 100:
                    num_zigzag += 1
                    zigzag_idx[num_zigzag] = rolling_idx[i]
                    zigzag_types[num_zigzag] = rolling_types[i]
                    zigzag_values[num_zigzag] = rolling_values[i]
                    zigzag_dev[num_zigzag - 1] = 100 * current_deviation

        # last point in zigzag is peak
        else:
            if rolling_types[i] == 1:
                if zigzag_values[num_zigzag] < rolling_values[i] and num_zigzag > 1:
                    current_deviation = (rolling_values[i] - zigzag_values[num_zigzag - 1]) / rolling_values[i]
                    zigzag_idx[num_zigzag] = rolling_idx[i]
                    zigzag_types[num_zigzag] = rolling_types[i]
                    zigzag_values[num_zigzag] = rolling_values[i]
                    zigzag_dev[num_zigzag - 1] = 100 * current_deviation
            else:
                current_deviation = (zigzag_values[num_zigzag] - rolling_values[i]) / rolling_values[i]
                if current_deviation > deviation / 100:
                    num_zigzag += 1
                    zigzag_idx[num_zigzag] = rolling_idx[i]
                    zigzag_types[num_zigzag] = rolling_types[i]
                    zigzag_values[num_zigzag] = rolling_values[i]
                    zigzag_dev[num_zigzag - 1] = 100 * current_deviation

    return zigzag_idx[:num_zigzag + 1], zigzag_types[:num_zigzag + 1], \
        zigzag_values[:num_zigzag + 1], zigzag_dev[:num_zigzag + 1]


@njit
def map_zigzag(zigzag_idx, zigzag_types, zigzag_values, zigzag_dev, candles_num):
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
    pivot_leg: int = None, price_deviation: IntFloat = None,
    retrace: bool = None, last_extreme: bool = None,
    offset: Int = None, **kwargs: DictLike
):
    """ Zigzag (ZIGZAG)

    Zigzag attempts to filter out smaller price movments while highlighting
    trend direction. It does not predict future trends, but it does identify
    swing highs and lows. When 'price_deviation' is set to 10, it will ignore
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
        pivot_leg (int): Number of legs > 2. Default: 10
        price_deviation (float): Price Deviation Percentage for a reversal.
            Default: 5
        retrace (bool): Default: False
        last_extreme (bool): Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: swing, and swing_type (high or low).
    """
    # Validate
    _length = 0
    pivot_leg = _length = v_pos_default(pivot_leg, 10)
    high = v_series(high, _length + 1)
    low = v_series(low, _length + 1)

    if high is None or low is None:
        return

    if close is not None:
        close = v_series(close, _length + 1)
        np_close = close.values
        if close is None:
            return

    price_deviation = v_pos_default(price_deviation, 5.0)
    retrace = v_bool(retrace, False)
    last_extreme = v_bool(last_extreme, True)
    offset = v_offset(offset)

    # Calculation
    np_high, np_low = high.values, low.values
    _rollings_idx, _rollings_types, _rollings_values = np_rolling_hl(highs=np_high, lows=np_low, window_size=pivot_leg)
    _zigzags_idx, _zigzags_types, _zigzags_values, _zigzags_dev = np_find_zigzags(_rollings_idx, _rollings_types,
                                                                                  _rollings_values,
                                                                                  deviation=price_deviation)
    _types, _values, _dev = map_zigzag(_zigzags_idx, _zigzags_types, _zigzags_values, _zigzags_dev, len(high))

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

    _params = f"_{price_deviation}%_{pivot_leg}"
    data = {
        f"ZIGZAGt{_params}": _types,
        f"ZIGZAGv{_params}": _values,
        f"ZIGZAGd{_params}": _dev,
    }
    df = DataFrame(data, index=high.index)
    df.name = f"ZIGZAG{_params}"
    df.category = "trend"

    return df
