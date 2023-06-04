# -*- coding: utf-8 -*-
from pandas import DataFrame, concat
from pandas_ta import true_range, sma, rsi, mfi
from pandas_ta.utils import get_offset, verify_series


def alphatrend(open, high, low, close, volume=None, src=None, common_period=None, multiplier=None, **kwargs):
    """Indicator: Alpha Trend"""
    open = verify_series(open)
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)

    src_mapping = {
        'open': open,
        'high': high,
        'low': low,
        'close': close
    }
    src = src if src in src_mapping.keys() else 'close'

    common_period = int(common_period) if common_period is not None else 14
    multiplier = multiplier if (multiplier is not None and multiplier > 0) else 1
    
    if volume is not None:
        volume = verify_series(volume)

    if high is None or low is None or close is None: return
    
    def alpha_trend_search(series):
        alpha_trend_ = [0]
        for idx, val in enumerate(series):
            if up50.iloc[idx]:
                if alpha_trend_[idx] < val:
                    alpha_trend_.append(val)
                else:
                    alpha_trend_.append(alpha_trend_[idx])
            else:
                if alpha_trend_[idx] > val:
                    alpha_trend_.append(val)
                else:
                    alpha_trend_.append(alpha_trend_[idx])

        return alpha_trend_[1:]
    
    def momentum_filter(momentum_series):
        df = DataFrame({'upt': upt,
                             'downt': downt})
        df['up50'] = momentum_series >= 50
        df['upt-downt'] = concat([upt[momentum_series >= 50], downt[momentum_series < 50]])
        df[['alpha-trend-val']] = df[['upt-downt']].apply(alpha_trend_search)
        
        return df['alpha-trend-val']

    tr = true_range(high, low, close)
    atr = sma(tr, common_period)
    
    src = src_mapping.get(src, src)
            
    upt = (low - atr * multiplier).fillna(0)
    
    downt = (high + atr * multiplier).fillna(0)
    
    if volume is None:
        rsi_ = rsi(src, common_period)
        up50 = rsi_ >= 50
        alpha_trend_ = momentum_filter(rsi_)
        
    else:
        mfi_ = mfi(high, low, close, volume, common_period)
        up50 = mfi_ >= 50
        alpha_trend_ = momentum_filter(mfi_)
    
    alpha_ind = DataFrame({'k1': alpha_trend_, 
                              'k2': alpha_trend_.shift(2).fillna(0)})
    alpha_ind.index = src.index
    
    return alpha_ind


alphatrend.__doc__ = \
""" Alpha Trend Inddicator

In Magic Trend we had some problems, Alpha Trend tries to solve those problems such as:

1-To minimize stop losses and overcome sideways market conditions.
2-To have more accurate BUY/SELL signals during trending market conditions.
3- To have significant support and resistance levels.
4- To bring together indicators from different categories that are compatible with each other and make a meaningful combination regarding momentum, trend, volatility, volume and trailing stop loss.

Sources:
    https://www.tradingview.com/script/o50NYLAZ-AlphaTrend/
    https://github.com/OnlyFibonacci/AlgoSeyri/blob/main/alphaTrendIndicator.py

    Default Inputs:
        volume: None, if left blank, it will be None, otherwise it's a series.
        multiplier: 1 which is the factor of trailing ATR value
	common_period: 14 which is the length of ATR MFI and RSI
	src: 'close' is default for source of ATRm MFI or RSI. However, `src` variable can also be to 'open', 'high' or 'low'
    See Source links

Args:
    open (pd.series): series of 'open's
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's. Default: None
    src (str): can be 'open', 'high', 'low' or 'close'. Default: 'close'
    multiplier (float): lfactor of trailing ATR value. Default: 1
    common_period (int): length of ATR MFI and RSI. Default: 14
    
Kwargs:

Returns:
    pd.DataFrame: index, k1, and k2 of all the input.
"""
