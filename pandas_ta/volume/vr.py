# -*- coding: utf-8 -*-
"""
VR Volatility Volume Ratio
TODO: change input to rows and not entire dataframe
"""
import numpy as np

def vr(data, n=None):
    n = n if n and n > 0 else 26
    

    VR = []

    AV_volumes, BV_volumes, CV_volumes = [], [], []
    for index, row in data.iterrows():

        if row["close"] > row["open"]:
            AV_volumes.append(row["volume"])
        elif row["close"] < row["open"]:
            BV_volumes.append(row["volume"])
        else:
            CV_volumes.append(row["volume"])

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

    return np.asarray(VR)