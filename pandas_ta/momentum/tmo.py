# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
from pandas_ta.overlap import ma
from pandas_ta.utils import get_offset, verify_series


def tmo(open_, close, tmo_length=None, calc_length=None, smooth_length=None, mamode=None,
        compute_momentum=False, normalize_signal=False, offset=None, **kwargs):
    """True Momentum Oscillator (TMO)

    The True Momentum Oscillator (TMO) is an indicator that aims to capture the
    true momentum underlying the price movement of an asset over a specified time
    frame. It quantifies the net buying and selling pressure by summing and then
    smoothing the signum of the closing and opening price difference over the
    given period, and then computing a main and smooth signal with a series of
    moving averages.
    Crossovers between the main and smoth signal generate potential signals for
    buying and selling opportunities.
    Some platforms present versions of this indicator with an optional momentum
    calculation for the main TMO signal and its smooth version, as well as the
    possibility to normalize the signals to the [-100,100] range, which has the
    added benefit of allowing the definition of overbought and oversold regions,
    typically -70 and 70.

    Calculation:
        Default Inputs: `tmo_length=14, calc_length=5, smooth_length=3`

        EMA = Exponential Moving Average
        Delta = close - open
        Signum = 1 if Delta > 0, 0 if Delta = 0, -1 if Delta < 0
        SUM = Summation of N given values
        MA = EMA(SUM(Delta, tmo_length), calc_length)
        TMO = EMA(MA, smooth_length)
        TMOs = EMA(TMO, smooth_length)
        TMO mom = TMO - TMO[-tmo_length]
        TMOs mom = TMOs - TMOs[-tmo_length]

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
        compute_momentum (bool): Compute main and smooth  momentum. Default: False
        normalize_signal (bool): Normalize TMO values to [-100,100]. Default: False
        offset (int): How many periods to offset the result. Default: 0
    
    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: main signal, smooth signal, main momentum, smooth momentum
    """

    # Validate
    tmo_length = int(tmo_length) if tmo_length and tmo_length > 0 else 14
    calc_length = int(calc_length) if calc_length and calc_length > 0 else 5
    smooth_length = int(smooth_length) if smooth_length and smooth_length > 0 else 3
    mamode = mamode if isinstance(mamode, str) else "ema"
    compute_momentum = compute_momentum if isinstance(compute_momentum, bool) else False
    normalize_signal = normalize_signal if isinstance(normalize_signal, bool) else False

    open_ = verify_series(open_, max(tmo_length, calc_length, smooth_length))
    close = verify_series(close, max(tmo_length, calc_length, smooth_length))
    offset = get_offset(offset)

    if open_ is None or close is None:
        return None

    # Calculate (see documentation)
    signum_values = Series(close - open_).apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    sum_signum = signum_values.rolling(window=tmo_length).sum()
    if normalize_signal:
        sum_signum = sum_signum * 100 / tmo_length

    initial_ema = ma(mamode, sum_signum, length=calc_length)
    main_signal = ma(mamode, initial_ema, length=smooth_length)
    smooth_signal = ma(mamode, main_signal, length=smooth_length)

    if compute_momentum:
        mom_main = main_signal - main_signal.shift(tmo_length)
        mom_smooth = smooth_signal - smooth_signal.shift(tmo_length)
    else:
        mom_main = Series([0] * len(main_signal), index=main_signal.index)
        mom_smooth = Series([0] * len(smooth_signal), index=smooth_signal.index)

    # Offset
    if offset != 0:
        main_signal = main_signal.shift(offset)
        smooth_signal = smooth_signal.shift(offset)
        mom_main = mom_main.shift(offset)
        mom_smooth = mom_smooth.shift(offset)

    # Fill
    fill_value = kwargs.get("fillna", None)
    fill_method = kwargs.get("fill_method", None)

    if fill_value is not None:
        main_signal.fillna(fill_value, inplace=True)
        smooth_signal.fillna(fill_value, inplace=True)
        mom_main.fillna(fill_value, inplace=True)
        mom_smooth.fillna(fill_value, inplace=True)

    if fill_method is not None:
        main_signal.fillna(method=fill_method, inplace=True)
        smooth_signal.fillna(method=fill_method, inplace=True)
        mom_main.fillna(fill_value, inplace=True)
        mom_smooth.fillna(fill_value, inplace=True)

    # Name and Category
    tmo_category = "momentum"
    params = f"{tmo_length}_{calc_length}_{smooth_length}"

    df = DataFrame({
        f"TMO_{params}": main_signal,
        f"TMO_Smooth_{params}": smooth_signal,
        f"TMO_Main_Mom_{params}": mom_main,
        f"TMO_Smooth_Mom_{params}": mom_smooth
    })

    df.name = f"TMO_{params}"
    df.category = tmo_category

    return df