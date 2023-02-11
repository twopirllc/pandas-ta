# -*- coding: utf-8 -*-
"""
Indicator: BBI Bull Bear Index
While this was inspired by Tushare, I found a different way to calculate this at https://www.tradingview.com/script/KvLCcuHB-BBI-4MA-4-overlay/


"""
from pandas_ta.overlap import ma
import numpy as np

def bbi(data, shorter=None, short=None, long=None, longer=None):
   #usually a 3, 6, 12, and 24 day sma is used here I think
   #but it may be more useful to allow this to be changed
    shorter = shorter if shorter and shorter > 0 else 3
    short = short if short and short > 0 else 6
    long = long if long and long > 0 else 12
    longer = longer if longer and longer > 0 else 24



    CS = []
    BBI = []
    for index, row in data.iterrows():
        CS.append(row["close"])

        if len(CS) < 24:
            BBI.append(row["close"])
        else:
            #bbi = np.average([np.average(CS[-3:]), np.average(CS[-6:]), np.average(CS[-12:]), np.average(CS[-24:])])
            bbi = (ma("sma", CS[-shorter:], length=shorter)+ma("sma", CS[-short:], length=short)+ma("sma", CS[-long:], length=long)+ma("sma", CS[-longer:], length=longer)/4)
            BBI.append(bbi)

    return np.asarray(BBI)