"""
WR Williams Overbought/Oversold Index


"""
import pandas as pd
from pandas_ta.utils import verify_series

def wnr(close, low, high, n=None):
    
    # Validate arguments
    
    close = verify_series(close)
    low = verify_series(low)
    high = verify_series(high)

    if close is None: return
    if low is None: return
    if open is None: return    
    n = n if n and n > 0 else 14

    #calculate
    
    high_prices = []
    low_prices = []
    WNR = []

    for i in range(0,len(close)):
        high_prices.append(high[i])
        if len(high_prices) == n:
            del high_prices[0]
        low_prices.append(low[i])
        if len(low_prices) == n:
            del low_prices[0]

        highest = max(high_prices)
        lowest = min(low_prices)

        wnr = (highest - close[i]) / (highest - lowest) * 100
        WNR.append(wnr)
    # Prepare DataFrame to return
    WNR = pd.DataFrame(WNR)    
    WNR.category = "trend"
    WNR.name = "Williams_Index"

    return WNR

