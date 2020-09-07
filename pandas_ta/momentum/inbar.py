import pandas as pd
from pandas_ta.utils import get_offset , verify_series , zero

def inbar(self , open , high ,low , close , offset = None , **kwargs ):
        """Indicator: Inside Bar"""
        # Validate arguments
        close = verify_series(close).apply(zero)
        open = verify_series(open).apply(zero)
        high = verify_series(high).apply(zero)
        low = verify_series(low).apply(zero)
        offset = get_offset(offset)
        prevBar = 1

        # Calculate Result
        bodyStat = (close >= open).rename('bodystat').replace({True: 1 , False:-1})
        isIn = ((high < high.shift(prevBar)) & (low > low.shift(prevBar))).rename('isin')
        res = pd.Series(index = close.index , dtype = 'int64')
        
        for i in close.index:
            if isIn[i] == True:
                res[i] = bodyStat[i]
            else:
                res[i] = 0

        # Offset
        if offset != 0:
            res = res.shift(offset)

        # Handle fills
        if 'fillna' in kwargs:
            res.fillna(kwargs['fillna'], inplace=True)

        if 'fill_method' in kwargs:
            res.fillna(method=kwargs['fill_method'], inplace=True)

        # Name and Categorize it
        res.name = "InBar"
        res.category = 'insidebar'
        
        return res

inbar.__doc__ = \
"""Inside Bar
Sources:
    https://www.tradingview.com/script/IyIGN1WO-Inside-Bar/
Calculation:
    Default Inputs:
        drift=1
    isIn = ((high < high.shift(prevBar)) & (low > low.shift(prevBar)))
    bodyStat = (close >= open)
Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    offset (int): How many periods to offset the result.  Default: 0
Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method
Returns:
    pd.Series: New feature
"""
