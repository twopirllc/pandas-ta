
"""
KDJ

Not sure if this is the same as the existing Stochastic Indicator
Please reference https://www.moomoo.com/us/learn/detail-what-is-the-kdj-67019-220809006
"""
import numpy as np
import pandas as pd
from pandas_ta.utils import verify_series
def kdj(close, low, high):
    
    # Validate arguments
    
    close = verify_series(close)
    low = verify_series(low)
    high = verify_series(high)
    
    if close is None: return
    if low is None: return
    if high is None: return
    
    #calculate
    
    rsv = (close - low) / (high - low) * 100
    K, D, J = [], [], []


    K.append( (2 / 3) * 50 + (1 / 3) * rsv[0])
    
    
    D.append((2 / 3) * 50 + (1 / 3) * K[0])
    
    J.append(3 * K[0] - 2 * D[0])
    
    for i in range(1,len(rsv)):
        K.append((2 / 3) * K[i-1] + (1 / 3) * rsv[i])
        D.append((2 / 3) * D[i-1] + (1 / 3) * K[i])
        J.append(3 * K[i] - 2 * D[i])
        
    # Prepare DataFrame to return

    K = pd.DataFrame(K)
    D = pd.DataFrame(D)
    J = pd.DataFrame(J)

    
    K.name = 'STOCH_K_TUSHARE'
    D.name = 'STOCH_D_TUSHARE'
    J.name = 'STOCH_J_TUSHARE'

    K.category = D.category = J.category = "momentum"


    df = pd.DataFrame()
    df["K"] = K
    df["D"] = D
    df["J"] = J

    df.name = 'KDJ'
    df.category = K.category
    return df
