# -*- coding: utf-8 -*-
"""
WR Williams Overbought/Oversold Index
TODO: change input to rows and not entire dataframe

"""

def wnr(data, n=None):
    n = n if n and n > 0 else 14


    high_prices = []
    low_prices = []
    WNR = []

    for index, row in data.iterrows():
        high_prices.append(row["high"])
        if len(high_prices) == n:
            del high_prices[0]
        low_prices.append(row["low"])
        if len(low_prices) == n:
            del low_prices[0]

        highest = max(high_prices)
        lowest = min(low_prices)

        wnr = (highest - row["close"]) / (highest - lowest) * 100
        WNR.append(wnr)

    return WNR