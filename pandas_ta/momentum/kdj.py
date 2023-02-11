# -*- coding: utf-8 -*-
"""
KDJ

Not sure if this is the same as the existing Stochastic Indicator
Please reference https://www.moomoo.com/us/learn/detail-what-is-the-kdj-67019-220809006
"""
import numpy as np
def kdj(close, low, high):
    


    K, D, J = [], [], []
    last_k, last_d = None, None
    for c in close:
        for l in low:
            for h in high:
                if last_k is None or last_d is None:
                    last_k = 50
                    last_d = 50


                rsv = (c - l) / (h - l) * 100

                k = (2 / 3) * last_k + (1 / 3) * rsv
                d = (2 / 3) * last_d + (1 / 3) * k
                j = 3 * k - 2 * d

                K.append(k)
                D.append(d)
                J.append(j)

                last_k, last_d = k, d

    return np.asarray(K), np.asarray(D), np.asarray(J)
