# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.overlap import hl2, sma
from pandas_ta.utils import (
    non_zero_range,
    v_drift,
    v_pos_default,
    v_offset,
    v_series
)



def eom(
    high: Series, low: Series, close: Series, volume: Series,
    length: Int = None, divisor: IntFloat= None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Ease of Movement (EOM)

    Ease of Movement is a volume based oscillator that is designed to
    measure the relationship between price and volume fluctuating across
    a zero line.

    Sources:
        https://www.tradingview.com/wiki/Ease_of_Movement_(EOM)
        https://www.motivewave.com/studies/ease_of_movement.htm
        https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ease_of_movement_emv

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        length (int): The short period. Default: 14
        divisor (float): Divisor. Default: 100000000
        drift (int): The diff period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 14)
    _length = length + 1
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)
    volume = v_series(volume, _length)

    if high is None or low is None or close is None or volume is None:
        return

    divisor = v_pos_default(divisor, 100_000_000)
    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    high_low_range = non_zero_range(high, low)
    distance = hl2(high=high, low=low)
    distance -= hl2(high=high.shift(drift), low=low.shift(drift))
    box_ratio = volume / divisor
    box_ratio /= high_low_range
    eom = distance / box_ratio
    eom = sma(eom, length=length)

    # Offset
    if offset != 0:
        eom = eom.shift(offset)

    # Fill
    if "fillna" in kwargs:
        eom.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    eom.name = f"EOM_{length}_{divisor}"
    eom.category = "volume"

    return eom
