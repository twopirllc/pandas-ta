# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.overlap import hl2, sma
from pandas_ta.utils import get_drift, get_offset, non_zero_range, verify_series


def eom(
    high: Series, low: Series, close: Series, volume: Series,
    length: Int = None, divisor: IntFloat= None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Ease of Movement (EOM)

    Ease of Movement is a volume based oscillator that is designed to measure the
    relationship between price and volume flucuating across a zero line.

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
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 14
    divisor = float(divisor) if divisor and divisor > 0 else 100000000
    high = verify_series(high, length)
    low = verify_series(low, length)
    close = verify_series(close, length)
    volume = verify_series(volume, length)
    drift = get_drift(drift)
    offset = get_offset(offset)

    if high is None or low is None or close is None or volume is None:
        return

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
    if "fill_method" in kwargs:
        eom.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    eom.name = f"EOM_{length}_{divisor}"
    eom.category = "volume"

    return eom
