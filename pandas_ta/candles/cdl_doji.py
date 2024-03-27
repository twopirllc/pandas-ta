# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.overlap import sma
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import high_low_range, is_percent
from pandas_ta.utils import real_body, v_offset, v_pos_default
from pandas_ta.utils import v_scalar, v_series



def cdl_doji(
    open_: Series, high: Series, low: Series, close: Series,
    length: Int = None, factor: IntFloat = None, scalar: IntFloat = None,
    asint: bool = True,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Candle Type: Doji

    A candle body is Doji, when it's shorter than 10% of the
    average of the 10 previous candles' high-low range.

    Sources:
        TA-Lib: 96.56% Correlation

    Args:
        open_ (pd.Series): Series of 'open's
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        length (int): The period. Default: 10
        factor (float): Doji value. Default: 100
        scalar (float): How much to magnify. Default: 100
        asint (bool): Keep results numerical instead of boolean.
            Default: True

    Kwargs:
        naive (bool, optional): If True, prefills potential Doji less than
            the length if less than a percentage of it's high-low range.
            Default: False
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: CDL_DOJI column.
    """
    # Validate
    length = v_pos_default(length, 10)
    open_ = v_series(open_, length)
    high = v_series(high, length)
    low = v_series(low, length)
    close = v_series(close, length)

    if open_ is None or high is None or low is None or close is None:
        return

    factor = v_scalar(factor, 10) if is_percent(factor) else 10
    scalar = v_scalar(scalar, 100)
    offset = v_offset(offset)
    naive = kwargs.pop("naive", False)

    # Calculate
    body = real_body(open_, close).abs()
    hl_range = high_low_range(high, low).abs()
    hl_range_avg = sma(hl_range, length)
    doji = body < 0.01 * factor * hl_range_avg

    if naive:
        doji.iat[:length] = body < 0.01 * factor * hl_range
    if asint:
        doji = scalar * doji.astype(int)

    # Offset
    if offset != 0:
        doji = doji.shift(offset)

    # Fill
    if "fillna" in kwargs:
        doji.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    doji.name = f"CDL_DOJI_{length}_{0.01 * factor}"
    doji.category = "candles"

    return doji
