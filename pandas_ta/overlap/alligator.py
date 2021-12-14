# -*- coding: utf-8 -*-
# from numpy import nan as npNaN
from pandas import DataFrame
from .smma import smma
from pandas_ta.utils import get_offset, verify_series


def alligator(close, jaw=None, teeth=None, lips=None, talib=None, offset=None, **kwargs):
    """Bill Williams Alligator (ALLIGATOR)

    The Alligator Indicator was developed by Bill Williams and combines moving
    averages with fractal geometry and the lines are meant to resemeble an alligator
    opening and closing his mouth.. It attempts to identify if an asset is trending.
    It consists of 3 lines: the Alligator's Jaw, Teeth, and Lips. Each have
    different lookback periods and but require the user to offset the results; this
    is avoid data leaks by Pandas TA. See help(ta.ichimoku) or help(ta.dpo) to
    offset the resultant lines.

    Sources:
        https://www.tradingview.com/scripts/alligator/
        https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=175&Name=Bill_Williams_Alligator

    Args:
        close (pd.Series): Series of 'close's
        jaw (int): The Jaw period. Default: 13
        teeth (int): The Teeth period. Default: 8
        lips (int): The Lips period. Default: 5
        talib (bool): If TA Lib is installed and talib is True, Returns the TA Lib
            version. Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: JAW, TEETH, LIPS columns.
    """
    # Validate Arguments
    jaw = int(jaw) if jaw and jaw > 0 else 13
    teeth = int(teeth) if teeth and teeth > 0 else 8
    lips = int(lips) if lips and lips > 0 else 5
    close = verify_series(close, max(jaw, teeth, lips))
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if close is None: return

    # Calculate Result
    gator_jaw = smma(close, length=jaw, talib=mode_tal)
    gator_teeth = smma(close, length=teeth, talib=mode_tal)
    gator_lips = smma(close, length=lips, talib=mode_tal)

    # Offset
    if offset != 0:
        gator_jaw = gator_jaw.shift(offset)
        gator_teeth = gator_teeth.shift(offset)
        gator_lips = gator_lips.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        gator_jaw.fillna(kwargs["fillna"], inplace=True)
        gator_teeth.fillna(kwargs["fillna"], inplace=True)
        gator_lips.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        gator_jaw.fillna(method=kwargs["fill_method"], inplace=True)
        gator_teeth.fillna(method=kwargs["fill_method"], inplace=True)
        gator_lips.fillna(method=kwargs["fill_method"], inplace=True)

    # Name & Category
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
