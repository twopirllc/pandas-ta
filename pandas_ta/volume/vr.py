"""
VR Volatility Volume Ratio
"""
import numpy as np
from pandas_ta.utils import verify_series
import pandas as pd

def vr(close, open, volume, n=None):
        
    # Validate arguments
    n = n if n and n > 0 else 26
    
    close = verify_series(close)
    open = verify_series(open)
    volume = verify_series(volume)
    
    if close is None: return
    if volume is None: return
    if open is None: return
    
    #calculate

    VR = []

    AV_volumes, BV_volumes, CV_volumes = [], [], []
    for i in range(0,len(close)):

        if close[i] > open[i]:
            AV_volumes.append(volume[i])
        elif close[i] < open[i]:
            BV_volumes.append(volume[i])
        else:
            CV_volumes.append(volume[i])

        if len(AV_volumes) == n:
            del AV_volumes[0]
        if len(BV_volumes) == n:
            del BV_volumes[0]
        if len(CV_volumes) == n:
            del CV_volumes[0]

        avs = sum(AV_volumes)
        bvs = sum(BV_volumes)
        cvs = sum(CV_volumes)

        if (bvs + (1 / 2) * cvs) != 0:
            vr = (avs + (1 / 2) * cvs) / (bvs + (1 / 2) * cvs)
        else:
            vr = 0
        VR.append(vr)
    # Prepare DataFrame to return
    VR = pd.DataFrame(VR)
    VR.name = "Volatility_Volume_Ratio"
    VR.category = "volume"
        

    return VR
