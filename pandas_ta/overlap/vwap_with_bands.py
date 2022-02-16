# -*- coding: utf-8 -*-
import math
import pandas
from pandas import Series, DataFrame
from pandas_ta.overlap import hlc3
from pandas_ta.utils import get_offset, is_datetime_ordered, verify_series


def vwap_with_bands(
    high: Series, low: Series, close: Series, volume: Series, bands: list = [-1,1],
    anchor: str = None,
    offset: int = None, **kwargs
) -> DataFrame:
    """Volume Weighted Average Price (VWAP)

    The Volume Weighted Average Price that measures the average typical price
    by volume.  It is typically used with intraday charts to identify general
    direction.

    Sources:
        https://www.tradingview.com/wiki/Volume_Weighted_Average_Price_(VWAP)
        https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/volume-weighted-average-price-vwap/
        https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:vwap_intraday
        https://www.sierrachart.com/index.php?page=doc/StudiesReference.php&ID=108&Name=Volume_Weighted_Average_Price_-_VWAP_-_with_Standard_Deviation_Lines

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        bands (list): List of volume weighted standard deviation bands to be processed
        anchor (str): How to anchor VWAP. Depending on the index values,
            it will implement various Timeseries Offset Aliases
            as listed here:
            https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
            Default: "D".
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: New feature generated.
    """
    # Validate
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    volume = verify_series(volume)
    anchor = anchor.upper() if anchor and isinstance(
        anchor, str) and len(anchor) >= 1 else "D"
    offset = get_offset(offset)

    typical_price = hlc3(high=high, low=low, close=close)
    if not is_datetime_ordered(volume):
        _s = "[!] VWAP volume series is not datetime ordered."
        print(f"{_s} Results may not be as expected.")
    if not is_datetime_ordered(typical_price):
        _s = "[!] VWAP price series is not datetime ordered."
        print(f"{_s} Results may not be as expected.")

    # Calculate vwap
    wp = typical_price * volume
    vwap = wp.groupby(wp.index.to_period(anchor)).cumsum()
    vwap /= volume.groupby(volume.index.to_period(anchor)).cumsum()

    # Calculate vwap stdev bands
    var = volume * (typical_price - vwap) ** 2
    var_sum = var.groupby(var.index.to_period(anchor)).cumsum()
    volume_sum = volume.groupby(volume.index.to_period(anchor)).cumsum()
    std_volume_weighted = (var_sum/volume_sum) ** 0.5

    # Build Dataframe
    df = pandas.DataFrame()
    df[f"VWAP_{anchor}"] = vwap
    for i in bands:
        df[f"{i}_VWAP_band"] = vwap + i*std_volume_weighted

    # Offset
    if offset != 0:
        vwap = vwap.shift(offset)

    # Fill
    if "fillna" in kwargs:
        vwap.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        vwap.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    vwap.name = f"VWAP_{anchor}_bands"
    vwap.category = "overlap"

    return df
