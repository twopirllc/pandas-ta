# -*- coding: utf-8 -*-
from warnings import simplefilter

from numpy import array_split, mean, sum
from pandas import cut, concat, DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.utils import signed_series, v_bool, v_pos_default, v_series



def vp(
    close: Series, volume: Series,
    width: Int = None, sort: bool = None,
    **kwargs: DictLike
) -> DataFrame:
    """Volume Profile (VP)

    Calculates the Volume Profile by slicing price into ranges.
    Note: Value Area is not calculated.

    Sources:
        https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:volume_by_price
        https://www.tradingview.com/wiki/Volume_Profile
        http://www.ranchodinero.com/volume-tpo-essentials/
        https://www.tradingtechnologies.com/blog/2013/05/15/volume-at-price/

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        width (int): How many ranges to distrubute price into. Default: 10
        sort (value, optional): Whether to sort by close before
            splitting into ranges. Default: False

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: New feature generated.
    """
    # Validate
    width = v_pos_default(width, 10)
    close = v_series(close, width)
    volume = v_series(volume, width)

    if close is None or volume is None:
        return

    sort = v_bool(sort, False)

    # Calculate
    signed_price = signed_series(close, 1)
    pos_volume = volume * signed_price[signed_price > 0]
    pos_volume.name = volume.name
    neg_volume = -volume * signed_price[signed_price < 0]
    neg_volume.name = volume.name
    neut_volume = volume + signed_price[signed_price == 0]
    neut_volume.name = volume.name
    vp = concat([close, pos_volume, neg_volume, neut_volume], axis=1)

    close_col = f"{vp.columns[0]}"
    high_price_col = f"high_{close_col}"
    low_price_col = f"low_{close_col}"
    mean_price_col = f"mean_{close_col}"

    volume_col = f"{vp.columns[1]}"
    pos_volume_col = f"pos_{volume_col}"
    neg_volume_col = f"neg_{volume_col}"
    neut_volume_col = f"neut_{volume_col}"
    total_volume_col = f"total_{volume_col}"
    vp.columns = [close_col, pos_volume_col, neg_volume_col, neut_volume_col]

    simplefilter(action="ignore", category=FutureWarning)
    # sort: Sort by close before splitting into ranges. Default: False
    # If False, it sorts by date index or chronological versus by price
    if sort:
        vp[mean_price_col] = vp[close_col]

        vpdf = vp.groupby(
            cut(vp[close_col], width, include_lowest=True, precision=2),
            observed=False
        ).agg({
            mean_price_col: mean,
            pos_volume_col: sum,
            neg_volume_col: sum,
            neut_volume_col: sum
        })

        vpdf[low_price_col] = [x.left for x in vpdf.index]
        vpdf[high_price_col] = [x.right for x in vpdf.index]
        vpdf = vpdf.reset_index(drop=True)

        vpdf = vpdf[[
            low_price_col, mean_price_col, high_price_col,
            pos_volume_col, neg_volume_col, neut_volume_col
        ]]
    else:
        vp_ranges = array_split(vp, width)
        result = list({
            low_price_col: r[close_col].min(),
            mean_price_col: r[close_col].mean(),
            high_price_col: r[close_col].max(),
            pos_volume_col: r[pos_volume_col].sum(),
            neg_volume_col: r[neg_volume_col].sum(),
            neut_volume_col: r[neut_volume_col].sum(),
        } for r in vp_ranges)

        vpdf = DataFrame(result)

    vpdf[total_volume_col] = vpdf[pos_volume_col] + vpdf[neg_volume_col]

    # Fill
    if "fillna" in kwargs:
        vpdf.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    vpdf.name = f"VP_{width}"
    vpdf.category = "volume"

    return vpdf
