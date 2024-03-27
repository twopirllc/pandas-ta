# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import v_offset, v_pos_default, v_series, v_talib
from .smma import smma



def alligator(
    close: Series, jaw: Int = None, teeth: Int = None, lips: Int = None,
    talib: bool = None, offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Bill Williams Alligator (ALLIGATOR)

    The Alligator Indicator was developed by Bill Williams and combines
    moving averages with fractal geometry and the lines are meant to
    resemble an alligator opening and closing his mouth.. It attempts to
    identify if an asset is trending. It consists of 3 lines: the
    Alligator's Jaw, Teeth, and Lips. Each have different lookback periods
    and but require the user to offset the results; this is avoid data leaks
    by Pandas TA. See help(ta.ichimoku) or help(ta.dpo) to offset the
    resultant lines.

    Sources:
        https://www.tradingview.com/scripts/alligator/
        https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=175&Name=Bill_Williams_Alligator

    Args:
        close (pd.Series): Series of 'close's
        jaw (int): The Jaw period. Default: 13
        teeth (int): The Teeth period. Default: 8
        lips (int): The Lips period. Default: 5
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: JAW, TEETH, LIPS columns.
    """
    # Validate
    jaw = v_pos_default(jaw, 13)
    teeth = v_pos_default(teeth, 8)
    lips = v_pos_default(lips, 5)
    close = v_series(close, max(jaw, teeth, lips))

    if close is None:
        return

    mode_tal = v_talib(talib)
    offset = v_offset(offset)

    # Calculate
    gator_jaw = smma(close, length=jaw, talib=mode_tal)
    gator_teeth = smma(close, length=teeth, talib=mode_tal)
    gator_lips = smma(close, length=lips, talib=mode_tal)

    # Offset
    if offset != 0:
        gator_jaw = gator_jaw.shift(offset)
        gator_teeth = gator_teeth.shift(offset)
        gator_lips = gator_lips.shift(offset)

    # Fill
    if "fillna" in kwargs:
        gator_jaw.fillna(kwargs["fillna"], inplace=True)
        gator_teeth.fillna(kwargs["fillna"], inplace=True)
        gator_lips.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = f"_{jaw}_{teeth}_{lips}"
    data = {
        f"AGj{_props}": gator_jaw,
        f"AGt{_props}": gator_teeth,
        f"AGl{_props}": gator_lips
    }
    df = DataFrame(data, index=close.index)

    df.name = f"AG{_props}"
    df.category = "overlap"

    return df
