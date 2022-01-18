# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta.utils import get_offset, verify_series


def cube(close: Series, cubing_exponent: float = None, signal_offset: int = None, offset: int = None, **kwargs) -> DataFrame:
    """
    Indicator: Cube Transform

    John Ehlers describes this indicator to be useful in compressing signals near zero for a normalized oscillator
    like the Inverse Fisher Transform. In conjunction to that, values close to -1 and 1 are nearly unchanged,
    whereas the ones near zero are reduced regarding their amplitude.
    From the input data the effects of spectral dilation should have been removed (i.e. roofing filter).

    Sources:
        Book: Cycle Analytics for Traders, 2014, written by John Ehlers, page 200
        Implemented by rengel8 for Pandas TA based on code of Markus K. (cryptocoinserver)

    Args:
        close (pd.Series): Series of 'close's
        cubing_exponent (float):  Use this exponent 'wisely' to increase the impact of the soft limiter. Default: 3
        signal_offset (int): Offset the signal line.  Default: -1
        offset (int): How many periods to offset the result.  Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: New feature generated.
    """

    # Validate arguments
    close = verify_series(close)
    cubing_exponent = float(cubing_exponent) if cubing_exponent and cubing_exponent >= 3.0 else 3.0
    signal_offset = int(signal_offset) if signal_offset and signal_offset > 0 else 1
    offset = get_offset(offset)

    # Calculate Result
    result = close ** cubing_exponent

    cube_transform = Series(result, index=close.index)
    cube_transform_signal = Series(result, index=close.index)

    # Offset
    if offset != 0:
        cube_transform = cube_transform.shift(offset)
        cube_transform_signal = cube_transform_signal.shift(offset)
    if signal_offset != 0:
        cube_transform_signal = cube_transform_signal.shift(signal_offset)

    # Handle fills
    if "fillna" in kwargs:
        cube_transform.fillna(kwargs["fillna"], inplace=True)
        cube_transform_signal.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        cube_transform.fillna(method=kwargs["fill_method"], inplace=True)
        cube_transform_signal.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    cube_transform.name = f"CUBE"
    cube_transform_signal.name = f"CUBE_SIGNAL"
    cube_transform.category = cube_transform_signal.category = "transform"

    # Prepare DataFrame to return
    data = {cube_transform.name: cube_transform, cube_transform_signal.name: cube_transform_signal}
    df = DataFrame(data)
    df.name = f"CUBE_TRANSFORM"
    df.category = cube_transform.category

    return df
