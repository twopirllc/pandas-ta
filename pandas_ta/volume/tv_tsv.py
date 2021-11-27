# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame, Series
from pandas_ta.utils import verify_series, signed_series
import statistics
import time
from datetime import date, datetime, timedelta, timezone

def tv_tsv(close=None, volume=None, length=None, signal=None, mamode=None, **kwargs):
    """Indicator: Time Segmented Value (TSV)"""
    # Validate Arguments
    drift = kwargs.pop("drift", 1)
    length = int(length) if length and length > 0 else 18
    signal = int(signal) if signal and signal > 0 else 10
    mamode = mamode if isinstance(mamode, str) else "sma"

    # Trading View
    # https://www.tradingview.com/script/6GR4ht9X-Time-Segmented-Volume/
    # t = sum( close > close[1] ? volume*(close-close[1]) : close < close[1] ? volume*(close-close[1]) : 0,l)
    # m = sma(t ,l_ma )

    # Calculate Result
    signed_volume = volume * ta.signed_series(close, 1)  # > 0
    signed_volume[signed_volume < 0 ] = -signed_volume   # < 0
    signed_volume.apply(ta.zero)                         # ~ 0
    
    cvd = (close.diff(drift) * signed_volume).fillna(0)
        
    tsv = (cvd.rolling(length).sum()).fillna(0)
    signal = (ta.ma(mamode, tsv, length=signal)).fillna(0)
    tsv_ratio = (tsv / signal).fillna(0)
    
    # Handle fills
    if "fillna" in kwargs:
        tsv.fillna(kwargs["fillna"], inplace=True)
        signal.fillna(kwargs["fillna"], inplace=True)
        tsv_ratio.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        tsv.fillna(method=kwargs["fill_method"], inplace=True)
        signal.fillna(method=kwargs["fill_method"], inplace=True)
        tsv_ratio.fillna(method=kwargs["fill_method"], inplace=True)
        

    
    # Name & Category
    _props = f"_{length}_{signal}"
    tv_tsv.name = f"TV_TSV{_props}"
    tv_tsv.category = "volume"

    #tsv.name = "tsv"
    

    df = pd.DataFrame({
        "close": close, "volume": volume,
        "signed_volume": signed_volume, "cvd": cvd,
        "tsv": tsv, "signal": signal, "tsv_ratio": tsv_ratio
    })

    return df



tv_tsv.__doc__ = \
"""Time Segmented Value (TSV)

TSV is a proprietary technical indicator developed by Worden Brothers Inc., classified as an oscillator. 
It is calculated by comparing various time segments of both price and volume. 
TSV essentially measures the amount of money flowing in or out of a particular stock. 
The baseline represents the zero line.

TSV is a leading indicator because its movement is based on both the stock's price fluctuation and volume. 
Ideal entry and exit points are commonly found as the stock moves across the baseline level. 
This indicator is similar to on-balance volume (OBV) because it measures the amount of money flowing in or out of a particular stock.

Sources:
    https://www.investopedia.com/terms/t/tsv.asp

Calculation:
    Default Inputs:
        length=18, signal=10


Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    length (int): It's period. Default: 18
    signal (int): It's avg period. Default: 10
    mamode (str): See ```help(ta.ma)```. Default: 'sma'

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: tsv, signal, tsv_ratio
"""
