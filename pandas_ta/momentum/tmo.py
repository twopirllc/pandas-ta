# -*- coding: utf-8 -*-
from numpy import broadcast_to, isnan, nan, nansum, newaxis, pad, sign, zeros
from numpy.lib.stride_tricks import sliding_window_view
from pandas import DataFrame, Series

from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.utils import (
    v_bool,
    v_mamode,
    v_offset,
    v_pos_default,
    v_series
)



def sum_signed_rolling_deltas(
    open_: Series, close: Series, length: Int, exclusive: bool = True
) -> Series:
    """Sum of signed rolling price deltas

    Calculate the sum of signed differences between the current day's closing
    price and a rolling window of preceding opening prices. This sum is then
    padded to match the original series length.

    The function can operate in two modes: exclusive and inclusive.
    In exclusive mode, the rolling window considers the current day is not part
    of the lookback period, while in inclusive mode it is.

    Parameters:
        close (Series): Series of closing prices.
        open_ (Series): Series of opening prices.
        length (Int): The window length for the rolling calculation.
        exclusive (bool): If True, the rolling window is exclusive of the
            current day's opening price, otherwise it's inclusive.

    Returns:
        Series: A series with the sum of signed rolling deltas between current
            day closing price and preceding days opening prices.

    Example:
    >>> close = Series([100, 110, 140,  80,  90,  60,  50,  40, 90, 110])
    >>> open_ = Series([95,   83,  71, 132, 129, 145, 133, 101, 68,  96])
    >>> result = sum_signed_rolling_deltas(close, open_, 4, exclusive=True)
    >>> expected_result = Series([np.nan, np.nan, np.nan, np.nan, \
        0.0, -4.0, -4.0, -4.0, -4.0, 0.0])
    >>> np.allclose(result, expected_result, rtol=1e-6, equal_nan=True)
    True
    >>> result = sum_signed_rolling_deltas(close, open_, 4, exclusive=False)
    >>> expected_result = Series([np.nan, np.nan, np.nan, \
        -1.0, 1.0, -3.0, -3.0, -3.0, -3.0, 1.0])
    >>> np.allclose(result, expected_result, rtol=1e-6, equal_nan=True)
    True
    """
    if not exclusive:
        length -= 1

    rolling_open = sliding_window_view(open_, window_shape=length)[:-1]

    close_broadcasted = broadcast_to(
        close[length:].to_numpy()[:, newaxis], rolling_open.shape
    )

    signed_deltas = sign(close_broadcasted - rolling_open)
    sum_signed_deltas = nansum(signed_deltas, axis=1).astype(float)

    return Series(
        pad(sum_signed_deltas, (length, 0), mode="constant", constant_values=nan),
        index=close.index,
    )


def tmo(
    open_: Series, close: Series,
    tmo_length: Int = None, calc_length: Int = None, smooth_length: Int = None,
    momentum: bool = False, normalize: bool = False, exclusive: bool = True,
    mamode: str = None, offset: Int = None, **kwargs: DictLike,
) -> DataFrame:
    """True Momentum Oscillator (TMO)

    This function computes the True Momentum Oscillator (TMO), a technical
    indicator that measures the momentum of an asset's price movement over
    a specified time frame. It does this by comparing the most recent closing
    price within a rolling window to each opening price in that window, summing
    the sign of these differences, and then applying a series of moving
    averages to smooth the results.

    Some platforms present versions of this indicator with an optional
    momentum calculation for the main TMO signal and its smooth version, as
    well as the possibility to normalize the signals to the [-100, 100] range,
    which has the added benefit of allowing the definition of overbought and
    oversold regions typically between -70 and 70.
    Common implementations in TV include indicators where the rolling windows
    are exclusive or not, and control over this behaviour is also provided.

    Sources:
        https://www.tradingview.com/script/VRwDppqd-True-Momentum-Oscillator/
        https://www.tradingview.com/script/65vpO7T5-True-Momentum-Oscillator-Universal-Edition/

    Args:
        open_ (Series): Series of 'open' prices.
        close (Series): Series of 'close' prices.
        tmo_length (Int): The period for TMO calculation. Default: 14
        calc_length (Int): Initial moving average window. Default: 5
        smooth_length (Int): Main and smooth signal MA window. Default: 3
        mamode (str): See ``help(ta.ma)``. Default: 'ema'
        momentum (bool): Compute main and smooth momentum.
            Default: False
        normalize (bool): Normalize TMO values to [-100,100].
            Default: False
        exclusive (bool): Exclusive or inclusive rolling window, where
            the lookback is made over n days, or n-1, if we consider the rolling
            window period should include the current date.
        offset (Int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): DataFrame.fillna(value)

    Returns:
        DataFrame: main, smooth, main momentum, smooth momentum

    """
    # Validate
    tmo_length = v_pos_default(tmo_length, 14)
    calc_length = v_pos_default(calc_length, 5)
    smooth_length = v_pos_default(smooth_length, 3)
    mamode = v_mamode(mamode, "ema")
    compute_momentum = v_bool(momentum, False)
    normalize_signal = v_bool(normalize, False)

    _length = max(tmo_length, calc_length, smooth_length)
    open_ = v_series(open_, _length)
    close = v_series(close, _length)
    offset = v_offset(offset)

    if "length" in kwargs:
        kwargs.pop("length")

    if open_ is None or close is None:
        return None

    signed_diff_sum = sum_signed_rolling_deltas(
        open_, close, tmo_length, exclusive=exclusive
    )
    if all(isnan(signed_diff_sum)):
        return None  # Emergency Break

    initial_ma = ma(mamode, signed_diff_sum, length=calc_length)
    if all(isnan(initial_ma)):
        return None  # Emergency Break

    main = ma(mamode, initial_ma, length=smooth_length)
    if all(isnan(main)):
        return None  # Emergency Break

    smooth = ma(mamode, main, length=smooth_length)
    if all(isnan(smooth)):
        return None  # Emergency Break

    if compute_momentum:
        mom_main = main - main.shift(tmo_length)
        mom_smooth = smooth - smooth.shift(tmo_length)
    else:
        zero_array = zeros(main.size)
        mom_main = Series(zero_array, index=main.index)
        mom_smooth = Series(zero_array, index=smooth.index)

    # Offset
    if offset != 0:
        main = main.shift(offset)
        smooth = smooth.shift(offset)
        mom_main = mom_main.shift(offset)
        mom_smooth = mom_smooth.shift(offset)

    # Fill
    if "fillna" in kwargs:
        main.fillna(kwargs["fillna"], inplace=True)
        smooth.fillna(kwargs["fillna"], inplace=True)
        mom_main.fillna(kwargs["fillna"], inplace=True)
        mom_smooth.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"_{tmo_length}_{calc_length}_{smooth_length}"
    main.name = f"TMO{_props}"
    smooth.name = f"TMOs{_props}"
    mom_main.name = f"TMOM{_props}"
    mom_smooth.name = f"TMOMs{_props}"
    main.category = smooth.category = "momentum"
    mom_main.category = mom_smooth.category = main.category

    data = {
        main.name: main,
        smooth.name: smooth,
        mom_main.name: mom_main,
        mom_smooth.name: mom_smooth,
    }
    df = DataFrame(data, index=close.index)
    df.name = f"TMO{_props}"
    df.category = main.category

    return df
