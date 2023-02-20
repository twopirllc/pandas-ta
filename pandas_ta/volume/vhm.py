from statistics import pstdev
import pandas_ta as panta

def vhm(volume ,length):

    # Default values
    if length == None:
        length = 610

    mean = panta.sma(volume, length)
    std = pstdev(volume, length)
    stdbar = (volume - mean) / std

    """Volume Heatmap 
    
    Volume Heatmap is a volume indicator. It is used to indicate market/trend strength in a given time. 
    
    Sources:
        https://www.tradingview.com/script/unWex8N4-Heatmap-Volume-xdecow/
    Calculation:
        Take the volume's very long term SMA(Preferably above 150 period).
        Calculate population standart deviation(pstdev) of volume.
        Subtract SMA from volume and divide it by pstdev and look at the truth table for interpretation.

        Truth table for signals:
        ==========================
        - extremely_cold <= -0.5
        - cold <= 1.0
        - medium <= 2.5
        - hot <= 4.0 
        - extremely_hot >= 4+ (4 or more)

    Example:
        ta.vhm(volume, length=n) > 2 gives True when signal is medium or above 

    Args:
        volume (pd.Series): Series of 'volume's
        length (int): Length of input data for vhm calculation
    
    Returns:
        pd.DataFrame: stdbar (signed float) 
    """

    return stdbar

