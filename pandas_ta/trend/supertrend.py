# -*- coding: utf-8 -*-
import numpy as np
from pandas import DataFrame
from ..utils import get_offset, verify_series
from ..volatility import atr


def supertrend(high, low, close, length=None, multiplier=None, mamode=None, drift=None, offset=None, **kwargs):
    # indicator : supertrend
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)
    length = int(length) if length and length > 0 else 10
    multiplier = float(multiplier) if multiplier and multiplier > 0 else 3
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs[
        'min_periods'] is not None else length

    supertrend_dir = np.zeros(shape=(len(close)))
    strend = np.zeros(shape=(len(close)))

    # Bands initial calculation
    midrange = 0.5 * (high + low)
    distance = multiplier * atr(high, low, close, length, mamode, drift, offset, min_periods=min_periods)
    lowerband = midrange - distance
    upperband = midrange + distance

    # final calculation loop
    for i in range(1, len(close)):
        if close[i] > upperband[i - 1]:
            supertrend_dir[i] = 1
        elif close[i] < lowerband[i - 1]:
            supertrend_dir[i] = -1
        else:
            supertrend_dir[i] = supertrend_dir[i - 1]
            if supertrend_dir[i] > 0 and lowerband[i] < lowerband[i - 1]:
                lowerband[i] = lowerband[i - 1]
            if supertrend_dir[i] < 0 and upperband[i] > upperband[i - 1]:
                upperband[i] = upperband[i - 1]
        if supertrend_dir[i] < 0:
            strend[i] = upperband[i]
        else:
            strend[i] = lowerband[i]

    # Prepare DataFrame to return
    data = {f"supertrend_{length}_{multiplier}": strend, f"supertrend_dir_{length}_{multiplier}": supertrend_dir}
    supertrend_df = DataFrame(data)
    supertrend_df.name = f"supertrend_{length}_{multiplier}"
    supertrend_df.category = 'trend'

    # Apply offset if needed
    if offset != 0:
        supertrend_df = supertrend_df.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        supertrend_df.fillna(kwargs['fillna'], inplace=True)

    if 'fill_method' in kwargs:
        supertrend_df.fillna(method=kwargs['fill_method'], inplace=True)

    return supertrend_df


supertrend.__doc__ = \
    """Supertrend (supertrend)

Supertrend is a trend indicator. It is usually used to help identify trend direction, setting stop loss, 
identify support and resistance, and / or generate buy & sell signals.
Calculation is in 2 steps : first a multiple of ATR is added and substracted to the middle of the high - low range.
This gives the upperband and lowerband. 
The direction of the trend is then calculated : if close > previous upperband or < previous lowerband, 
then trend direction is changed, else it is the same as previous value.
If trend direction is unchanged and down, upperband is set to minimum between current and previous value
If trend direction is unchanged and up, lowerband is set to maximum between current and previous value.

The final band is then choosen according to the direction of the trend : upperband if trend is downward, 
lowerband if trend is upward.
Returned values are : float for final band level, int (1 : upward trend, -1 : downward trend) for trend direction

Calculation:
    Default Inputs:
        length = 10
        multiplier = 3

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int) : length for ATR calculation. Default : 10
    multiplier : coefficient for upper and lower band distance to midrange. Default : 3
    mamode: parameter used for ATR calculation. See ATR documentation. Default : None (= ema)
    drift : parameter used for ATR calculation. See ATR documentation. Default : None (= 1)
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method
    min_periods (int, optional) : parameter used for ATR calculation. See ATR documentation. Default : length

Returns:
    pd.DataFrame: supertrend (float), supertrend_dir (int) columns.
"""
