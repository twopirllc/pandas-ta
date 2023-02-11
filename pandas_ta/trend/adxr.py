"""
ADXR
"""

import numpy as np
import pandas as pd
from pandas_ta.utils import verify_series
from pandas_ta.trend import adx
def adxr(high, low, close, n=None):
    
    # Validate arguments
    close = verify_series(close)
    low = verify_series(low)
    high = verify_series(high)

    
    if close is None: return
    if low is None: return
    if high is None: return

    n = n if n and n > 0 else 6
    
    ADX = adx(high, low, close, length=n).iloc[:, 0] 
    print(ADX)
    ADXR = []
    
    for i in range(0,len(close)):
        
        if i>= n:
            adxr = (ADX[i] + ADX[i - n]) / 2
            ADXR.append(adxr)
        else:
            ADXR.append(0)
            
    # Prepare DataFrame to return
    
    ADXR = pd.DataFrame(ADXR)
    ADXR.name = 'ADXR'
    ADXR.category = 'trend'
    return ADXR
