# -*- coding: utf-8 -*-
# from numpy import average, log, nan, power, sqrt, zeros_like
from numpy import average, log, nan, sqrt, zeros_like
from numpy import power as np_power
from pandas import Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.utils import v_float, v_offset, v_pos_default, v_series



def jma(
    close: Series, length: IntFloat = None, phase: IntFloat = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Jurik Moving Average Average (JMA)

    Mark Jurik's Moving Average (JMA) attempts to eliminate noise to see
    the "true" underlying activity. It has extremely low lag, is very
    smooth and is responsive to market gaps.

    Sources:
        https://c.mql5.com/forextsd/forum/164/jurik_1.pdf
        https://www.prorealcode.com/prorealtime-indicators/jurik-volatility-bands/

    Args:
        close (pd.Series): Series of 'close's
        length (int): Period of calculation. Default: 7
        phase (float): How heavy/light the average is [-100, 100]. Default: 0
        offset (int): How many lengths to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    _length = v_pos_default(length, 7)
    close = v_series(close, _length)

    if close is None:
        return

    phase = v_float(phase, 0.0)
    offset = v_offset(offset)

    # Calculate
    jma = zeros_like(close)
    volty = zeros_like(close)
    v_sum = zeros_like(close)

    kv = det0 = det1 = ma2 = 0.0
    jma[0] = ma1 = uBand = lBand = close.iloc[0]

    # Static variables
    sum_length = 10
    length = 0.5 * (_length - 1)
    pr = 0.5 if phase < -100 else 2.5 if phase > 100 else 1.5 + phase * 0.01
    length1 = max((log(sqrt(length)) / log(2.0)) + 2.0, 0)
    pow1 = max(length1 - 2.0, 0.5)
    length2 = length1 * sqrt(length)
    bet = length2 / (length2 + 1)
    beta = 0.45 * (_length - 1) / (0.45 * (_length - 1) + 2.0)

    m = close.shape[0]
    for i in range(1, m):
        price = close.iloc[i]

        # Price volatility
        del1 = price - uBand
        del2 = price - lBand
        volty[i] = max(abs(del1), abs(del2)) if abs(del1) != abs(del2) else 0

        # Relative price volatility factor
        v_sum[i] = v_sum[i - 1] + \
            (volty[i] - volty[max(i - sum_length, 0)]) / sum_length
        avg_volty = average(v_sum[max(i - 65, 0):i + 1])
        d_volty = 0 if avg_volty == 0 else volty[i] / avg_volty
        r_volty = max(1.0, min(np_power(length1, 1 / pow1), d_volty))
        # r_volty = max(1.0, min(length1 **(1 / pow1), d_volty))

        # Jurik volatility bands
        pow2 = np_power(r_volty, pow1)
        kv = np_power(bet, sqrt(pow2))
        uBand = price if (del1 > 0) else price - (kv * del1)
        lBand = price if (del2 < 0) else price - (kv * del2)

        # Jurik Dynamic Factor
        power = np_power(r_volty, pow1)
        alpha = np_power(beta, power)

        # 1st stage - preliminary smoothing by adaptive EMA
        ma1 = (1 - alpha) * price + alpha * ma1

        # 2nd stage - one more preliminary smoothing by Kalman filter
        det0 = (1 - beta) * (price - ma1) + beta * det0
        ma2 = ma1 + pr * det0

        # 3rd stage - final smoothing by unique Jurik adaptive filter
        det1 = ((ma2 - jma[i - 1]) * (1 - alpha) * \
                (1 - alpha)) + (alpha * alpha * det1)
        jma[i] = jma[i - 1] + det1

    jma = Series(jma, index=close.index)
    jma.iloc[0:_length - 1] = nan

    # Offset
    if offset != 0:
        jma = jma.shift(offset)

    # Fill
    if "fillna" in kwargs:
        jma.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    jma.name = f"JMA_{_length}_{phase}"
    jma.category = "overlap"

    return jma
