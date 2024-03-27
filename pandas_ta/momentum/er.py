# -*- coding: utf-8 -*-
from pandas import DataFrame, concat, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import (
    signals,
    v_drift,
    v_offset,
    v_pos_default,
    v_series
)



def er(
    close: Series, length: Int = None, drift: Int = None,
    offset: Int = None, **kwargs: DictLike
) -> Series:
    """Efficiency Ratio (ER)

    The Efficiency Ratio was invented by Perry J. Kaufman and presented in
    his book "New Trading Systems and Methods". It is designed to account
    for market noise or volatility.

    It is calculated by dividing the net change in price movement over
    N periods by the sum of the absolute net changes over the same N periods.

    Sources:
        https://help.tc2000.com/m/69404/l/749623-kaufman-efficiency-ratio

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = v_pos_default(length, 10)
    close = v_series(close, length + 1)

    if close is None:
        return

    drift = v_drift(drift)
    offset = v_offset(offset)

    # Calculate
    abs_diff = close.diff(length).abs()
    abs_volatility = close.diff(drift).abs()
    abs_volatility_rsum = abs_volatility.rolling(window=length).sum()

    er = abs_diff / abs_volatility_rsum

    # Offset
    if offset != 0:
        er = er.shift(offset)

    # Fill
    if "fillna" in kwargs:
        er.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    er.name = f"ER_{length}"
    er.category = "momentum"

    signal_indicators = kwargs.pop("signal_indicators", False)
    if signal_indicators:
        signalsdf = concat(
            [
                DataFrame({er.name: er}),
                signals(
                    indicator=er,
                    xa=kwargs.pop("xa", 80),
                    xb=kwargs.pop("xb", 20),
                    xserie=kwargs.pop("xserie", None),
                    xserie_a=kwargs.pop("xserie_a", None),
                    xserie_b=kwargs.pop("xserie_b", None),
                    cross_values=kwargs.pop("cross_values", False),
                    cross_series=kwargs.pop("cross_series", True),
                    offset=offset,
                ),
            ],
            axis=1,
        )

        return signalsdf
    else:
        return er
