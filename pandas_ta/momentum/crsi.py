# -*- coding: utf-8 -*-
from numpy import (
    concatenate,
    diff,
    full,
    nan,
    nanmean,
    newaxis,
    sign,
)
from numpy.lib.stride_tricks import sliding_window_view
from pandas import Series
from pandas_ta._typing import Array, DictLike, Int, IntFloat
from pandas_ta.maps import Imports
from pandas_ta.momentum.rsi import rsi
from pandas_ta.utils import (
    v_drift,
    v_offset,
    v_pos_default,
    v_scalar,
    v_series,
    v_talib,
)



def consecutive_streak(x: Array) -> Array:
    """Calculate the streak of consecutive price increases or decreases.

    This function computes the streak of consecutive daily price increases
    or decreases. A positive streak indicates consecutive days of price
    increases, while a negative streak indicates consecutive days of price
    decreases. The streak is reset to zero when the direction of the price
    change reverses.

    Parameters:
        prices (Array1d): An array of prices.

    Returns:
        Array1d: An array representing the streak of price changes.

    The function first calculates the difference between consecutive prices.
    It then assigns a +1 for each positive change, -1 for each negative change,
    and 0 for no change. The result is an array where each element represents
    the streak value for that day.

    Example:
    >>> prices = np.array([100, 101, 102, 100, 100, 101, 102, 103])
    >>> result = consecutive_streak(prices)
    >>> expected_result = np.array([0, 1, 1, -1, 0, 1, 1, 1])
    >>> np.array_equal(result, expected_result)
    True
    """
    return concatenate(([0], sign(diff(x))))


def percent_rank(x: Series, lookback: Int) -> Series:
    """Calculate the Percent Rank of daily returns over given period.

    The Percent Rank compares today's return with the one-day returns from each
    of the previous days within the lookback period. It measures the percentage
    of these past returns that are less than the current day's return.

    Args:
        close (Series): Series of 'close' prices.
        lookback (Int): The lookback period for calculating the Percent Rank.

    Returns:
        Series: A Pandas Series containing the Percent Rank values.

    The function first calculates the daily percentage returns of the 'close'
    prices.It then creates a rolling window of these returns and compares each
    value in the window to the current value (the last value in each window).
    The Percent Rank is calculated as the percentage of values in each window
    that are less than the current value. The result is a Series where the
    initial part (up to 'lookback - 1') is padded with NaNs, and the rest
    contains the Percent Rank values.

    Example:
    >>> close = Series([100, 80, 75, 123, 140, 80, 70, 40, 100, 120])
    >>> result = percent_rank(close, 3)
    >>> expected_result = Series([np.nan, np.nan, np.nan, \
        66.666667, 66.666667, 0.0, 33.333333, 0.0, 100.0, 66.666667])
    >>> np.allclose(result, expected_result, rtol=1e-6, equal_nan=True)
    True
    """
    daily_returns_np = x.pct_change().to_numpy()

    rolling_windows = sliding_window_view(daily_returns_np, window_shape=(lookback + 1,))
    comparison_matrix = rolling_windows[:, :-1] < rolling_windows[:, -1, newaxis]

    percent_ranks = nanmean(comparison_matrix, axis=1) * 100
    padded_percent_ranks = full(len(x), nan)
    padded_percent_ranks[lookback:] = percent_ranks

    return Series(padded_percent_ranks, index=x.index)


def crsi(
    close: Series, length_rsi: Int = None, length_streak: Int = None,
    length_rank: Int = None, scalar: IntFloat = None, talib: bool = None,
    drift: Int = None, offset: Int = None, **kwargs: DictLike,
) -> Series:
    """Connors Relative Strength Index (RSI)

    Connors RSI (CRSI) integrates Relative Strength Index (RSI), UpDown Length,
    and Rate of Change (ROC) of RSI components to evaluate overbought and
    oversold conditions in financial markets, providing insights into price
    momentum and potential reversals.

    Sources:
        Connors, L., Alvarez, C., & Radtke, M. (2012). An Introduction to
        ConnorsRSI. Connors Research Trading Strategy Series.
        ISBN 978-0-9853072-9-5.
        Retrieved from https://alvarezquanttrading.com/blog/connorsrsi-analysis/
        https://www.tradingview.com/support/solutions/43000502017-connors-rsi-crsi/

    Args:
        close (pd.Series): Series of 'close's
        length_rsi (int): The RSI period. Default: 3
        length_streak (int): The Streak RSI period. Default: 2
        length_rank (int): Percent Rank length. Default: 100
        scalar (float): How much to magnify. Default: 100
        talib (bool): Use TAlib for RSI if available. Default: True
        drift (int): The difference period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated
    """
    # Validate
    length_rsi = v_pos_default(length_rsi, 3)
    length_streak = v_pos_default(length_streak, 2)
    length_rank = v_pos_default(length_rank, 100)
    _length = max(length_rsi, length_streak, length_rank)
    close = v_series(close, _length)

    if "length" in kwargs:
        kwargs.pop("length")

    if close is None:
        return None

    scalar = v_scalar(scalar, 100)
    mode_tal = v_talib(talib)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    np_close = close.to_numpy()
    streak = Series(consecutive_streak(np_close), index=close.index)

    if Imports["talib"] and mode_tal:
        from talib import RSI
        close_rsi = RSI(close, length_rsi)
        streak_rsi = RSI(streak, length_streak)
    else:
        # Both TA-lib and Pandas-TA use the Wilder's RSI and its smoothing
        # function.
        close_rsi = rsi(
            close, length=length_rsi, scalar=scalar, talib=talib,
            drift=drift, offset=offset, **kwargs
        )

        streak_rsi = rsi(
            streak, length=length_streak, scalar=scalar, talib=talib,
            drift=drift, offset=offset, **kwargs
        )

    pr = percent_rank(close, length_rank)
    crsi = (close_rsi + streak_rsi + pr) / 3.0

    # Offset
    if offset != 0:
        crsi = crsi.shift(offset)

    # Fill
    if "fillna" in kwargs:
        crsi.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    crsi.name = f"CRSI_{length_rsi}_{length_streak}_{length_rank}"
    crsi.category = "momentum"

    return crsi
