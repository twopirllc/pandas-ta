# Technical Analysis Library in Python
![Example Chart](/images/TA_Chart.png)

Technical Analysis (TA) is an easy to use library that is built upon Python's Pandas library with more than 60 Indicators.  These indicators are comminly used for financial time series datasets with columns or labels similar to: datetime, open, high, low, close, volume, et al.  Many commonly used indicators are included, such as: _Moving Average Convergence Divergence_ (*MACD*), _Hull Exponential Moving Average_ (*HMA*), _Bollinger Bands_ (*BBANDS*), _On-Balance Volume_ (*OBV*), _Aroon Oscillator_ (*AROON*) and more.

This version contains both the orignal code branch as well as a newly refactored branch with the option to use [Pandas DataFrame Extension](https://pandas.pydata.org/pandas-docs/stable/extending.html) mode. 
All the indicators return a named Series or a DataFrame in uppercase underscore parameter format.  For example, MACD(fast=12, slow=26, signal=9) will return a DataFrame with columns: ['MACD_12_26_9', 'MACDH_12_26_9', 'MACDS_12_26_9'].

## New Changes

* At 70+ indicators.
* Abbreviated Indicator names as listed below.
* *Extended Pandas DataFrame* as 'ta'.  See examples below.
* Parameter names are more consistent.
* Former indicators still exist and are renamed with '_depreciated' append to it's name.  For example, 'average_true_range' is now 'average_true_range_depreciated'.
* Refactoring indicators into categories similar to [TA-lib](https://github.com/mrjbq7/ta-lib/tree/master/docs/func_groups).

### What is a Pandas DataFrame Extension?

A [Pandas DataFrame Extension](https://pandas.pydata.org/pandas-docs/stable/extending.html), extends a DataFrame allowing one to add more functionality and features to Pandas to suit your needs.  As such, it is now easier to run Technical Analysis on existing Financial Time Series without leaving the current DataFrame.  This extension by default returns the Indicator result or, inclusively, it can append the result to the existing DataFrame by including the parameter 
'append=True' in the method call. See examples below.


# Getting Started and Examples

## **Quick Start** using the DataFrame Extension

```python
import pandas as pd
import pandas_ta as ta

# Load data
df = pd.read_csv('symbol.csv', sep=',')

# Calculate Returns and append to the df DataFrame
df.ta.log_return(cumulative=True, append=True)
df.ta.percent_return(cumulative=True, append=True)

# New Columns with results
df.columns

# Take a peek
df.tail()

# vv Continue Post Processing vv
```

## Module and Indicator Help

```python
import pandas as pd
import pandas_ta as ta

# Help about this, 'ta', extension
help(pd.DataFrame().ta)

# List of all indicators
pd.DataFrame().ta.indicators()

# Help about the log_return indicator
help(ta.log_return)

# Help about the log_return indicator as a DataFrame Extension
help(pd.DataFrame().ta.log_return)
```



# Technical Analysis Indicators (by Category)

## _Performance_ (2)

Use parameter: cumulative=**True** for cumulative results.

* _Log Return_: **log_return**
* _Percent Return_: **percent_return**

| _Percent Return_ (Cumulative) with _Simple Moving Average_ (SMA) |
|:--------:|
| ![Example Cumulative Percent Return](/images/SPY_CumulativePercentReturn.png) |


# Inspiration
Inspired by Bukosabino: https://github.com/bukosabino/ta

Please leave any comments, feedback, or suggestions.