# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas import Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.utils import v_offset, v_mamode, v_pos_default, v_series

def pvi(
    close: Series, volume: Series, length: Int = None, initial: Int = None,
    mamode: str = None, offset: Int = None, **kwargs: DictLike
) -> pd.DataFrame:
    """Positive Volume Index (PVI)

    The Positive Volume Index is a cumulative indicator that uses volume
    change in an attempt to identify where smart money is active. Used in
    conjunction with NVI.

    Sources:
        https://www.investopedia.com/terms/p/pvi.asp

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        length (int): The short period. Default: 255
        initial (int): The short period. Default: 100
        mamode (str): See ``help(ta.ma)``. Default: 'ema'
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: New DataFrame with ['PVI_1', 'PVIs_<length>']
    """

    # Validate
    mamode = v_mamode(mamode, "ema")
    length = v_pos_default(length, 255)
    close = v_series(close, length + 1)
    volume = v_series(volume, length + 1)
    initial = v_pos_default(initial, 100)
    offset = v_offset(offset)

    if close is None or volume is None:
        return

    # Get numpy arrays of the data
    close_prices = close.to_numpy()
    volumes = volume.to_numpy()
    pvis = np.empty(len(close_prices))

    # Set the first value from from initial
    pvis[0] = initial

    # Calculate
    for i in range(1, len(close_prices)):
        if volumes[i] > volumes[i-1]:
            # PVI = Yesterday’s PVI + [[(Close – Yesterday’s Close) / Yesterday’s Close] * Yesterday’s PVI
            pvis[i] = pvis[i-1] + (((close_prices[i] - close_prices[i-1]) / close_prices[i-1]) * pvis[i-1])
        else:
            # PVI = Yesterday’s PVI
            pvis[i] = pvis[i-1]

    data = {
        'PVI_1': pvis,
    }
    df = pd.DataFrame(data, index=close.index)

    if offset != 0:
        df['PVI_1'] = df['PVI_1'].shift(offset)

    sig_series = ma(mamode, df['PVI_1'], length=length)
    df[f'PVIs_{length}'] = sig_series

    # Fill
    if "fillna" in kwargs:
        df.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        df.fillna(method=kwargs["fill_method"], inplace=True)

    return df
