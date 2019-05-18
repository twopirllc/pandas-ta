# -*- coding: utf-8 -*-
from numpy import array_split
from pandas import concat, DataFrame
from ..utils import signed_series, verify_series

def vp(close, volume, width=None, **kwargs):
    """Indicator: Volume Profile (VP)"""
    # Validate arguments
    close = verify_series(close)
    volume = verify_series(volume)
    width = int(width) if width and width > 0 else 10
    sort_close = kwargs.pop('sort_close', False)

    # Setup
    signed_volume = signed_series(volume, initial=1)
    pos_volume = signed_volume[signed_volume > 0] * volume
    neg_volume = signed_volume[signed_volume < 0] * -volume
    vp = concat([close, pos_volume, neg_volume], axis=1)

    close_col = f"{vp.columns[0]}"
    high_price_col = f"high_{close_col}"
    low_price_col = f"low_{close_col}"
    mean_price_col = f"mean_{close_col}"
    mid_price_col = f"mid_{close_col}"

    volume_col = f"{vp.columns[1]}"
    pos_volume_col = f"pos_{volume_col}"
    neg_volume_col = f"neg_{volume_col}"
    total_volume_col = f"total_{volume_col}"
    vp.columns = [close_col, pos_volume_col, neg_volume_col]

    # sort_close: Sort by close before splitting into ranges. Default: False
    # If False, it sorts by date index or chronological versus by price
    if sort_close:
        vp.sort_values(by=[close_col], inplace=True)

    # Calculate Result
    vp_ranges = array_split(vp, width)
    result = ({
        low_price_col: r[close_col].min(),
        mean_price_col: r[close_col].mean(),
        high_price_col: r[close_col].max(),
        pos_volume_col: r[pos_volume_col].sum(),
        neg_volume_col: r[neg_volume_col].sum(),
    } for r in vp_ranges)
    vpdf = DataFrame(result)
    vpdf[total_volume_col] = vpdf[pos_volume_col] + vpdf[neg_volume_col]

    # Handle fills
    if 'fillna' in kwargs:
        vpdf.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        vpdf.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    vpdf.name = f"VP_{width}"
    vpdf.category = 'volume'

    return vpdf


vp.__doc__ = \
"""Volume Profile (VP)

Calculates the Volume Profile by slicing price into ranges.  Note: Value Area is not calculated.

Sources:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:volume_by_price
    https://www.tradingview.com/wiki/Volume_Profile
    http://www.ranchodinero.com/volume-tpo-essentials/
    https://www.tradingtechnologies.com/blog/2013/05/15/volume-at-price/

Calculation:
    Default Inputs:
        width=10
    
    vp = pd.concat([close, pos_volume, neg_volume], axis=1)
    vp_ranges = np.array_split(vp, width)
    result = ({high_close, low_close, mean_close, neg_volume, pos_volume} foreach range in vp_ranges)
    vpdf = pd.DataFrame(result)
    vpdf['total_volume'] = vpdf['pos_volume'] + vpdf['neg_volume']

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    width (int): How many ranges to distrubute price into.  Default: 10

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method
    sort_close (value, optional): Whether to sort by close before splitting into ranges.  Default: False

Returns:
    pd.DataFrame: New feature generated.
"""