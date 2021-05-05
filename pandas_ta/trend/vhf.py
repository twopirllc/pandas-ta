# -*- coding: utf-8 -*-
from numpy import fabs as npFabs
from pandas_ta.utils import get_offset, verify_series


def vhf(source, length=None, offset=None, **kwargs):
    """Indicator: Vertical Horizontal Filter (VHF)"""
    # Validate arguments
    length = int(length ) if length and length > 0 else 28
    source = verify_series(source, length)  # usually close price
    offset = get_offset(offset)

    if source is None: return

    # Calculate Result
    hcp = source.rolling(length).max()
    lcp = source.rolling(length).min()
    diff = npFabs(source - source.shift(1))
    vhf_ = npFabs(hcp - lcp) / diff.rolling(length).sum()

    # Offset
    if offset != 0:
        vhf_ = vhf_.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        vhf_.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        vhf_.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    vhf_.name = f"VHF_{length}"
    vhf_.category = "trend"

    return vhf_


vhf.__doc__ = """Vertical Horizontal Filter (VHF)
    
    VHF was created by Adam White to identify trending and ranging markets.   
    
    Sources:
        https://www.incrediblecharts.com/indicators/vertical_horizontal_filter.php
    
    Calculation:
        Default Inputs:
            source = Close, length = 28
        HCP = Highest Close Price in Period
        LCP = Lowest Close Price in Period
        Change = abs(Ct - Ct-1)
        VHF = (HCP - LCP) / RollingSum[length] of Change     
                
    Args:
        source (pd.Series): Series of prices (usually close). 
        length (int): The period length. Default: 28
        offset (int): How many periods to offset the result. Default: 0
    
    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method
    
    Returns:
        pd.Series: New feature generated.
    """
