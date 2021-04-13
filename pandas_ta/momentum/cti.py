import pandas as pd
from pandas_ta.utils import get_offset, verify_series
from pandas_ta.overlap import linreg


def cti(close: pd.Series, length: int, offset=None, **kwargs) -> pd.Series:
    """Indicator: Correlation Trend Indicator"""
    close = verify_series(close)
    length = int(length) if length and length > 0 else 12
    offset = get_offset(offset)

    cti_ds = linreg(close, length, r=True)

    # Offset
    if offset != 0:
        cti_ds = cti_ds.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        cti_ds.fillna(method=kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        cti_ds.fillna(method=kwargs["fill_method"], inplace=True)

    cti_ds.name = f"CTI_{length}"
    cti_ds.category = "momentum"
    return cti_ds


cti.__doc__ = """
The Correlation Trend Indicator is an oscillating technical indicator created 
by John Ehler in 2020. Assigns a value depending on how close prices in that 
range are to following a positively- or negatively-sloping straight line. 
Values range from -1 to 1.

Args:
    close (pd.Series): The dataseries of close prices for the selected instrument.
    length (int): The window to be taking values from for the indicator. Default is 12.
    offset ([type], optional): If there is an offset of the series to be applied.
        Default is None.

Returns:
    pd.Series: Series of the CTI values for the given period.
"""
