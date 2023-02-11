"""
Indicator: ASI Accumulation Swing Index
Inspired by tushare

"""
import numpy as np
from pandas_ta.overlap import ma
import pandas as pd
from pandas_ta.utils import verify_series

def asi(close, low, high, open, n=None):
    
    # Validate arguments
    
    close = verify_series(close)
    low = verify_series(low)
    high = verify_series(high)
    open = verify_series(open)
    
    if close is None: return
    if low is None: return
    if high is None: return    
    if open is None: return  
    
    n = n if n and n > 0 else 5
    #calculate
    SI = []
    SI.append(0.)

    for i in range(1,len(close)):
        a = abs(close[i] - close[i-1])
        b = abs(low[i] - close[i-1])
        c = abs(high[i] - close[i-1])
        d = abs(close[i-1] - open[i-1])

        if b > a and b > c:
            r = b + (1 / 2) * a + (1 / 4) * d
        elif c > a and c > b:
            r = c + (1 / 4) * d
        else:
            r = 0

        e = close[i] - close[i-1]
        f = close[i] - open[i-1]
        g = close[i-1] - open[i-1]

        x = e + (1 / 2) * f + g
        k = max(a, b)
        l = 3

        if np.isclose(r, 0) or np.isclose(l, 0):
            si = 0
        else:
            si = 50 * (x / r) * (k / l)

        SI.append(si)

    # Prepare DataFrame to return
    SI = pd.DataFrame(SI)

    ASI = SI.rolling(n).mean()
    ASI.name = 'ASI'
    ASI.category = 'volatility'
    return ASI

