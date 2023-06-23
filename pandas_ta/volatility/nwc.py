# -*- coding: utf-8 -*-
from pandas import DataFrame
from pandas_ta import Imports
from pandas_ta.utils import verify_series
import numpy as np
from .atr import atr

def nwc(close, high, low, length=None, kernel=None, scalar=None, **kwargs):
    '''Indicator: Nadaraya-Watson Channel'''
    # Validate arguments
    length = int(length) if length and length > 0 else 8
    close = verify_series(close,length)
    high = verify_series(high,length)
    low = verify_series(low,length)
    scalar = float(scalar) if scalar and scalar > 0 else 1.5
    kernel = kernel.lower() if kernel and issubclass(kernel) else quadratickernel

    # Calculate regression for each input price column (close, high, low)
    kernelClose = nadarayawatsonregression(close, kernel, length)
    kernelHigh = nadarayawatsonregression(high, kernel, length)
    kernelLow = nadarayawatsonregression(low, kernel, length)
    
    # Calculte Average True Range to allow for smoother results 
    kernelsAtr = atr(kernelHigh['kernel'], kernelLow['kernel'], kernelClose['kernel'],length).fillna(0)
    
    # Calculates upper and lower bands
    upper = kernelClose['kernel'] + scalar*kernelsAtr
    lower = kernelClose['kernel'] - scalar*kernelsAtr
    mid = kernelClose['kernel']

        # Handle fills
    if "fillna" in kwargs:
        lower.fillna(kwargs["fillna"], inplace=True)
        mid.fillna(kwargs["fillna"], inplace=True)
        upper.fillna(kwargs["fillna"], inplace=True)        
    if "fill_method" in kwargs:
        lower.fillna(method=kwargs["fill_method"], inplace=True)
        mid.fillna(method=kwargs["fill_method"], inplace=True)
        upper.fillna(method=kwargs["fill_method"], inplace=True)        

    # Name and Categorize it
    lower.name = f"NWCL_{length}"
    mid.name = f"NWCM_{length}"
    upper.name = f"NWCU_{length}"
    upper.category = lower.category = mid.category = "volatility"    

    # Prepare DataFrame to return
    data = {
        lower.name: lower, mid.name: mid, upper.name: upper        
    }
    nwcdf = DataFrame(data)
    nwcdf.name = f"NWC_{length}"
    nwcdf.category = mid.category    
    
    return nwcdf


def nadarayawatsonregression(df, kernel, h):
    """
    Perform Nadaraya-Watson regression on a column of a Pandas DataFrame.

    Args:
    df: pandas DataFrame, input data, containing one column
    kernel: function, kernel function that computes weights
    h: float, bandwidth parameter

    Returns:
    y_pred: pandas Series, predicted response variable
    """

    X_train = np.arange(df.shape[0])
    y_train = df.values.flatten()

    n_train = X_train.shape[0]
    y_pred = np.zeros(n_train)

    for i in range(n_train):
        distances = np.abs(X_train - X_train[i])
        weights = kernel(distances, h)
        y_pred[i] = np.sum(weights * y_train) / np.sum(weights)

    return DataFrame(y_pred, columns=['kernel'])    

# Define a kernel function.
def gaussiankernel(distances, h):
    weights = np.exp(-0.5 * (distances / h) ** 2)
    return weights

def quadratickernel(distances, h):
    weights = np.maximum(1 - (distances / h) ** 2, 0)
    return weights

def epanechnikovkernel(distances, h):
    return 0.75 * (1 - (distances / h) ** 2) * ((distances <= h).astype(float))  

nwc.__doc__ = \
"""Nadaraya-Watson Channel (NWC)

The Nadaraya-Watson trading indicator is a non-parametric regression technique used to estimate a target variable based on a weighted average of nearby data points. It assigns higher weights to closer data points, making it suitable for smoothing noisy price data and identifying potential trends or support/resistance levels in trading.

https://in.tradingview.com/script/WeLssFxl-Nadaraya-Watson-Envelope-Non-Repainting/

Sources:
    https://in.tradingview.com/script/WeLssFxl-Nadaraya-Watson-Envelope-Non-Repainting/ it's not an exact replica, calculations are done differently, but reach same result or different if you choose other kernels.

Calculation:
    length = int(length) if length and length > 0 else 8
    close = verify_series(close,length)
    high = verify_series(high,length)
    low = verify_series(low,length)
    scalar = float(scalar) if scalar and scalar > 0 else 1.5
    kernel = kernel.lower() if kernel and issubclass(kernel) else quadratickernel

    Default Inputs:
        length=8, scalar=1.5, kernel=quadratickernel
    
    REGRESSION:     
    Iterates over the input data (high, low and close), computing the distances between data points, 
    and applying the specified kernel to compute the weights. 
    The predicted response variable is then computed based on these weights. 
    Finally, the predicted response variable is returned as a DataFrame with the column name 'kernel'.

    UPPER = REGRESSION + SCALAR * ATR(REGRESSIONs(high,low,close))
    LOWER = REGRESSION - SCALAR * ATR(REGRESSIONs(high,low,close))
    MID = REGRESSION    

Args:
    close (pd.Series): Series of 'close's
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    length (int): The loockback period. Default: 8
    kernel (int): The weighting method. Default: quadratickernel
    scalar (float): The multiplier to form the upper and lower channels. Default: 1.5
    
Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: lower, mid and upper.
"""
