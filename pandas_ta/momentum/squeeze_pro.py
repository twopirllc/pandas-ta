# -*- coding: utf-8 -*-
from numpy import nan
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int, IntFloat
from pandas_ta.ma import ma
from pandas_ta.momentum import mom
from pandas_ta.trend import decreasing, increasing
from pandas_ta.utils import (
    simplify_columns,
    unsigned_differences,
    v_bool,
    v_mamode,
    v_offset,
    v_pos_default,
    v_scalar,
    v_series
)
from pandas_ta.volatility import bbands, kc



def squeeze_pro(
    high: Series, low: Series, close: Series,
    bb_length: Int = None, bb_std: IntFloat = None,
    kc_length: Int = None, kc_scalar_wide: IntFloat = None,
    kc_scalar_normal: IntFloat = None, kc_scalar_narrow: IntFloat = None,
    mom_length: Int = None, mom_smooth: Int = None,
    use_tr: bool = None, mamode: str = None,
    prenan: bool = None,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """Squeeze PRO(SQZPRO)

    This indicator is an extended version of "TTM Squeeze" from John Carter.
    The default is based on John Carter's "TTM Squeeze" indicator, as
    discussed in his book "Mastering the Trade" (chapter 11). The Squeeze
    indicator attempts to capture the relationship between two studies:
    Bollinger Bands® and Keltner's Channels. When the volatility increases,
    so does the distance between the bands, conversely, when the volatility
    declines, the distance also decreases. It finds sections of the
    Bollinger Bands® study which fall inside the Keltner's Channels.

    Sources:
        https://usethinkscript.com/threads/john-carters-squeeze-pro-indicator-for-thinkorswim-free.4021/
        https://www.tradingview.com/script/TAAt6eRX-Squeeze-PRO-Indicator-Makit0/

    Args:
        high (pd.Series): Series of 'high's
        low (pd.Series): Series of 'low's
        close (pd.Series): Series of 'close's
        bb_length (int): Bollinger Bands period. Default: 20
        bb_std (float): Bollinger Bands Std. Dev. Default: 2
        kc_length (int): Keltner Channel period. Default: 20
        kc_scalar_wide (float): Keltner Channel scalar for wider channel.
            Default: 2
        kc_scalar_normal (float): Keltner Channel scalar for normal channel.
            Default: 1.5
        kc_scalar_narrow (float): Keltner Channel scalar for narrow channel.
            Default: 1
        mom_length (int): Momentum Period. Default: 12
        mom_smooth (int): Smoothing Period of Momentum. Default: 6
        mamode (str): Only "ema" or "sma". Default: "sma"
        prenan (bool): If True, sets nan for all columns up the first
            valid squeeze value. Default: False
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        tr (value, optional): Use True Range for Keltner Channels.
            Default: True
        asint (value, optional): Use integers instead of bool. Default: True
        mamode (value, optional): Which MA to use. Default: "sma"
        detailed (value, optional): Return additional variations of SQZ for
            visualization. Default: False
        fillna (value, optional): pd.DataFrame.fillna(value)

    Returns:
        pd.DataFrame: SQZPRO, SQZPRO_ON_WIDE, SQZPRO_ON_NORMAL,
            SQZPRO_ON_NARROW, SQZPRO_OFF_WIDE, SQZPRO_NO columns by default.
            More detailed columns if 'detailed' kwarg is True.
    """
    # Validate
    bb_length = v_pos_default(bb_length, 20)
    kc_length = v_pos_default(kc_length, 20)
    mom_length = v_pos_default(mom_length, 12)
    mom_smooth = v_pos_default(mom_smooth, 6)
    _length = max(bb_length, kc_length, mom_length, mom_smooth) + 1
    high = v_series(high, _length)
    low = v_series(low, _length)
    close = v_series(close, _length)

    if high is None or low is None or close is None:
        return

    kc_scalar_narrow = v_scalar(kc_scalar_narrow, 1)
    kc_scalar_normal = v_scalar(kc_scalar_normal, 1.5)
    kc_scalar_wide = v_scalar(kc_scalar_wide, 2)
    prenan = v_bool(prenan, False)
    valid_kc_scaler = kc_scalar_wide > kc_scalar_normal \
        and kc_scalar_normal > kc_scalar_narrow

    if not valid_kc_scaler:
        return

    bb_std = v_pos_default(bb_std, 2.0)
    mamode = v_mamode(mamode, "sma")
    offset = v_offset(offset)
    use_tr = kwargs.pop("tr", True)
    asint = kwargs.pop("asint", True)
    detailed = kwargs.pop("detailed", False)

    # Calculate
    bbd = bbands(close, length=bb_length, std=bb_std, mamode=mamode)
    kch_wide = kc(
        high, low, close, length=kc_length, scalar=kc_scalar_wide,
        mamode=mamode, tr=use_tr
    )
    kch_normal = kc(
        high, low, close, length=kc_length, scalar=kc_scalar_normal,
        mamode=mamode, tr=use_tr
    )
    kch_narrow = kc(
        high, low, close, length=kc_length, scalar=kc_scalar_narrow,
        mamode=mamode, tr=use_tr
    )

    # Simplify KC and BBAND column names for dynamic access
    bbd.columns = simplify_columns(bbd)
    kch_wide.columns = simplify_columns(kch_wide)
    kch_normal.columns = simplify_columns(kch_normal)
    kch_narrow.columns = simplify_columns(kch_narrow)

    momo = mom(close, length=mom_length)
    squeeze = ma(mamode, momo, length=mom_smooth)

    # Classify Squeezes
    squeeze_on_wide = (bbd.l > kch_wide.l) & (bbd.u < kch_wide.u)
    squeeze_on_normal = (bbd.l > kch_normal.l) & (bbd.u < kch_normal.u)
    squeeze_on_narrow = (bbd.l > kch_narrow.l) & (bbd.u < kch_narrow.u)
    squeeze_off_wide = (bbd.l < kch_wide.l) & (bbd.u > kch_wide.u)
    no_squeeze = ~squeeze_on_wide & ~squeeze_off_wide

    # Offset
    if offset != 0:
        squeeze = squeeze.shift(offset)
        squeeze_on_wide = squeeze_on_wide.shift(offset)
        squeeze_on_normal = squeeze_on_normal.shift(offset)
        squeeze_on_narrow = squeeze_on_narrow.shift(offset)
        squeeze_off_wide = squeeze_off_wide.shift(offset)
        no_squeeze = no_squeeze.shift(offset)

    # Fill
    if "fillna" in kwargs:
        squeeze.fillna(kwargs["fillna"], inplace=True)
        squeeze_on_wide.fillna(kwargs["fillna"], inplace=True)
        squeeze_on_normal.fillna(kwargs["fillna"], inplace=True)
        squeeze_on_narrow.fillna(kwargs["fillna"], inplace=True)
        squeeze_off_wide.fillna(kwargs["fillna"], inplace=True)
        no_squeeze.fillna(kwargs["fillna"], inplace=True)

    # Name and Category
    _props = "" if use_tr else "hlr"
    _props += f"_{bb_length}_{bb_std}_{kc_length}_{kc_scalar_wide}_{kc_scalar_normal}_{kc_scalar_narrow}"
    squeeze.name = f"SQZPRO{_props}"

    if asint:
        squeeze_on_wide = squeeze_on_wide.astype(int)
        squeeze_on_narrow = squeeze_on_narrow.astype(int)
        squeeze_on_normal = squeeze_on_normal.astype(int)
        squeeze_off_wide = squeeze_off_wide.astype(int)
        no_squeeze = no_squeeze.astype(int)

    if prenan:
        nanlength = max(bb_length, kc_length) - 2
        squeeze_on_wide[:nanlength] = nan
        squeeze_on_narrow[:nanlength] = nan
        squeeze_on_normal[:nanlength] = nan
        squeeze_off_wide[:nanlength] = nan
        no_squeeze[:nanlength] = nan

    data = {
        squeeze.name: squeeze,
        f"SQZPRO_ON_WIDE": squeeze_on_wide,
        f"SQZPRO_ON_NORMAL": squeeze_on_normal,
        f"SQZPRO_ON_NARROW": squeeze_on_narrow,
        f"SQZPRO_OFF": squeeze_off_wide,
        f"SQZPRO_NO": no_squeeze
    }
    df = DataFrame(data, index=close.index)
    df.name = squeeze.name
    df.category = squeeze.category = "momentum"

    # More Detail
    if detailed:
        pos_squeeze = squeeze[squeeze >= 0]
        neg_squeeze = squeeze[squeeze < 0]

        pos_inc, pos_dec = unsigned_differences(pos_squeeze, asint=True)
        neg_inc, neg_dec = unsigned_differences(neg_squeeze, asint=True)

        pos_inc *= squeeze
        pos_dec *= squeeze
        neg_dec *= squeeze
        neg_inc *= squeeze

        pos_inc.replace(0, nan, inplace=True)
        pos_dec.replace(0, nan, inplace=True)
        neg_dec.replace(0, nan, inplace=True)
        neg_inc.replace(0, nan, inplace=True)

        sqz_inc = squeeze * increasing(squeeze)
        sqz_dec = squeeze * decreasing(squeeze)
        sqz_inc.replace(0, nan, inplace=True)
        sqz_dec.replace(0, nan, inplace=True)

        # Fill
        if "fillna" in kwargs:
            sqz_inc.fillna(kwargs["fillna"], inplace=True)
            sqz_dec.fillna(kwargs["fillna"], inplace=True)
            pos_inc.fillna(kwargs["fillna"], inplace=True)
            pos_dec.fillna(kwargs["fillna"], inplace=True)
            neg_dec.fillna(kwargs["fillna"], inplace=True)
            neg_inc.fillna(kwargs["fillna"], inplace=True)

        df[f"SQZPRO_INC"] = sqz_inc
        df[f"SQZPRO_DEC"] = sqz_dec
        df[f"SQZPRO_PINC"] = pos_inc
        df[f"SQZPRO_PDEC"] = pos_dec
        df[f"SQZPRO_NDEC"] = neg_dec
        df[f"SQZPRO_NINC"] = neg_inc

    return df
