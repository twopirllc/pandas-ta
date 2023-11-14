# -*- coding: utf-8 -*-
from numpy import isnan, zeros
from pandas import DataFrame, Series
from pandas_ta._typing import DictLike, Int
from pandas_ta.ma import ma
from pandas_ta.utils import v_bool, v_mamode, v_pos_default, v_offset, v_series


def tmo(
    open_: Series, close: Series,
    tmo_length: Int = None, calc_length: Int  =None, smooth_length: Int = None,
    mamode: str = None, compute_momentum: bool = False,
    normalize_signal: bool = False,
    offset: Int = None, **kwargs: DictLike
) -> DataFrame:
    """True Momentum Oscillator (TMO)

    The True Momentum Oscillator (TMO) aims to capture the true momentum
    underlying the price movement of an asset over a specified time frame. It
    quantifies the net buying and selling pressure by summing and then
    smoothing the signum of the closing and opening price difference over the
    given period, and then computing a main and smooth signal with a series
    of moving averages. Crossovers between the main and smooth signal generate
    potential signals for buying and selling opportunities.

    Some platforms present versions of this indicator with an optional
    momentum calculation for the main TMO signal and its smooth version, as
    well as the possibility to normalize the signals to the [-100, 100] range,
    which has the added benefit of allowing the definition of overbought and
    oversold regions typically between -70 and 70.

    Sources:
        https://www.tradingview.com/script/VRwDppqd-True-Momentum-Oscillator/
        https://www.tradingview.com/script/65vpO7T5-True-Momentum-Oscillator-Universal-Edition/
        https://www.tradingview.com/script/o9BQyaA4-True-Momentum-Oscillator/

    Args:
        open_ (pd.Series): Series of 'open' prices.
        close (pd.Series): Series of 'close' prices.
        tmo_length (int): The period for TMO calculation. Default: 14
        calc_length (int): Initial moving average window. Default: 5
        smooth_length (int): Main and smooth signal MA window. Default: 3
        mamode (str): See ``help(ta.ma)``. Default: 'ema'
        compute_momentum (bool): Compute main and smooth momentum.
            Default: False
        normalize_signal (bool): Normalize TMO values to [-100,100].
            Default: False
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: main, smooth, main momentum, smooth momentum
    """
    # Validate
    tmo_length = v_pos_default(tmo_length, 14)
    calc_length = v_pos_default(calc_length, 5)
    smooth_length = v_pos_default(smooth_length, 3)
    mamode = v_mamode(mamode, "ema")
    compute_momentum = v_bool(compute_momentum, False)
    normalize_signal = v_bool(normalize_signal, False)

    _length = max(tmo_length, calc_length, smooth_length)
    open_ = v_series(open_, _length)
    close = v_series(close, _length)
    offset = v_offset(offset)

    if "length" in kwargs:
        kwargs.pop("length")

    if open_ is None or close is None:
        return None

    # Calculate
    signed_diff = Series(close - open_) \
        .apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    signed_diff_sum = signed_diff.rolling(window=tmo_length).sum()

    if normalize_signal:
        signed_diff_sum = signed_diff_sum * 100 / tmo_length

    initial_ma = ma(mamode, signed_diff_sum, length=calc_length)
    if all(isnan(initial_ma)):
        return None # Emergency Break

    main = ma(mamode, initial_ma, length=smooth_length)
    if all(isnan(main)):
        return None # Emergency Break

    smooth = ma(mamode, main, length=smooth_length)
    if all(isnan(smooth)):
        return None # Emergency Break

    if compute_momentum:
        mom_main = main - main.shift(tmo_length)
        mom_smooth = smooth - smooth.shift(tmo_length)
    else:
        zero_array = zeros(main.size)
        mom_main = Series(zero_array, index=main.index)
        mom_smooth = Series(zero_array, index=smooth.index)

    # Offset
    if offset != 0:
        main = main.shift(offset)
        smooth = smooth.shift(offset)
        mom_main = mom_main.shift(offset)
        mom_smooth = mom_smooth.shift(offset)

    # Fill
    if "fillna" in kwargs:
        main.fillna(kwargs["fillna"], inplace=True)
        smooth.fillna(kwargs["fillna"], inplace=True)
        mom_main.fillna(kwargs["fillna"], inplace=True)
        mom_smooth.fillna(kwargs["fillna"], inplace=True)

    if "fill_method" in kwargs:
        main.fillna(method=kwargs["fill_method"], inplace=True)
        smooth.fillna(method=kwargs["fill_method"], inplace=True)
        mom_main.fillna(method=kwargs["fill_method"], inplace=True)
        mom_smooth.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _props = f"_{tmo_length}_{calc_length}_{smooth_length}"

    main.name = f"TMO{_props}"
    smooth.name = f"TMOs{_props}"
    mom_main.name = f"TMOM{_props}"
    mom_smooth.name = f"TMOMs{_props}"
    main.category = smooth.category = "momentum"
    mom_main.category = mom_smooth.category = main.category

    data = {
        main.name: main,
        smooth.name: smooth,
        mom_main.name: mom_main,
        mom_smooth.name: mom_smooth
    }
    df = DataFrame(data, index=close.index)
    df.name = f"TMO{_props}"
    df.category = main.category

    return df
