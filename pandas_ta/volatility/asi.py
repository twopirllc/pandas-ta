# -*- coding: utf-8 -*-
"""
Indicator: ASI Accumulation Swing Index
Inspired by tushare
"""
import numpy as np
from pandas_ta.overlap import ma

def asi(data, n=None):

    n = n if n and n > 0 else 5

    SI = []
    for index, row in data.iterrows():
        if index == 0:
            last_row = row
            SI.append(0.)
        else:

            a = abs(row["close"] - last_row["close"])
            b = abs(row["low"] - last_row["close"])
            c = abs(row["high"] - last_row["close"])
            d = abs(last_row["close"] - last_row["open"])

            if b > a and b > c:
                r = b + (1 / 2) * a + (1 / 4) * d
            elif c > a and c > b:
                r = c + (1 / 4) * d
            else:
                r = 0

            e = row["close"] - last_row["close"]
            f = row["close"] - last_row["open"]
            g = last_row["close"] - last_row["open"]

            x = e + (1 / 2) * f + g
            k = max(a, b)
            l = 3

            if np.isclose(r, 0) or np.isclose(l, 0):
                si = 0
            else:
                si = 50 * (x / r) * (k / l)

            SI.append(si)

    ASI = ma("sma",SI, n)
    return ASI
