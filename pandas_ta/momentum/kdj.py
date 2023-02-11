# -*- coding: utf-8 -*-
"""
KDJ

Not sure if this is the same as the existing Stochastic Indicator
Please reference https://www.moomoo.com/us/learn/detail-what-is-the-kdj-67019-220809006
"""
import numpy as np
def kdj(close, low, high):
    
    rsv = (close - low) / (high - low) * 100
    K, D, J = [], [], []


    K.append( (2 / 3) * 50 + (1 / 3) * rsv[0])
    
    
    D.append((2 / 3) * 50 + (1 / 3) * K[0])
    
    for i in range(1,len(rsv)):
        K.append((2 / 3) * K[i-1] + (1 / 3) * rsv[i])
        D.append((2 / 3) * D[i-1] + (1 / 3) * K[i])
        J.append(3 * K[i] - 2 * D[i])


   

    return np.asarray(K), np.asarray(D), np.asarray(J)
