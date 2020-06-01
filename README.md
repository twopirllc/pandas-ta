[![Python Version](https://img.shields.io/pypi/pyversions/pandas_ta.svg)](https://pypi.org/project/pandas_ta/)
[![PyPi Version](https://img.shields.io/pypi/v/pandas_ta.svg)](https://pypi.org/project/pandas_ta/)
[![Package Status](https://img.shields.io/pypi/status/pandas_ta.svg)](https://pypi.org/project/pandas_ta/)
[![Downloads](https://img.shields.io/pypi/dm/pandas_ta.svg?style=flat)](https://pypistats.org/packages/pandas_ta)

# __Technical Analysis Library in Python 3.7__
![Example Chart](/images/TA_Chart.png)

__Pandas Technical Analysis__ (Pandas TA) is an easy to use library that is built upon Python's Pandas library with more than 100 Indicators.  These indicators are comminly used for financial time series datasets with columns or labels similar to: datetime, open, high, low, close, volume, et al.  Many commonly used indicators are included, such as: _Simple Moving Average_ (*SMA*) _Moving Average Convergence Divergence_ (*MACD*), _Hull Exponential Moving Average_ (*HMA*), _Bollinger Bands_ (*BBANDS*), _On-Balance Volume_ (*OBV*), _Aroon & Aroon Oscillator_ (*AROON*) and more.

This version contains both the orignal code branch as well as a newly refactored branch with the option to use [Pandas DataFrame Extension](https://pandas.pydata.org/pandas-docs/stable/extending.html) mode. 
All the indicators return a named Series or a DataFrame in uppercase underscore parameter format.  For example, MACD(fast=12, slow=26, signal=9) will return a DataFrame with columns: ['MACD_12_26_9', 'MACDH_12_26_9', 'MACDS_12_26_9'].


## __Features__

* Has 100+ indicators and utility functions.
* Example Jupyter Notebook under the examples directory.
* A new 'ta' method called 'strategy' that be default, runs __all__ the indicators.
* Abbreviated Indicator names as listed below.
* __Extended Pandas DataFrame__ as 'ta'. 
* Easily add prefixes or suffixes or both to columns names.
* Categories similar to [TA-lib](https://github.com/mrjbq7/ta-lib/tree/master/docs/func_groups).


## __Recent Changes__

### __New DataFrame Method:__
    strategy (strategy)

### __Added indicators:__
    Bias (bias)
    Choppiness Index (chop)
    Chande Kroll Stop (cksp)
    Entropy (entropy)
    Heikin-Ashi Candles (ha)
    KDJ (kdj)
    Parabolic Stop and Reverse (psar)
    Price Distance (pdist)
    Psycholigical Line (psl)
    Supertrend (supertrend)
    Weighted Closing Price (wcp)
### __Added utilities:__
    Above (above)
    Above Value (above_value)
    Below (below)
    Below Value (below_value)
    Cross Value (cross_value)
### __User Added Indicators:__
    Aberration (aberration)
    BRAR (brar)
### __Corrected Indicators:__
    Absolute Price Oscillator (apo)
    Aroon & Aroon Oscillator (aroon)
        * Fixed indicator and included oscillator in returned dataframe
    Bollinger Bands (bbands)
    Commodity Channel Index (cci)
    Chande Momentum Oscillator (cmo)

## What is a Pandas DataFrame Extension?

A [Pandas DataFrame Extension](https://pandas.pydata.org/pandas-docs/stable/extending.html), extends a DataFrame allowing one to add more functionality and features to Pandas to suit your needs.  As such, it is now easier to run Technical Analysis on existing Financial Time Series without leaving the current DataFrame.  This extension by default returns the Indicator result or it can append the result to the existing DataFrame by including the parameter 'append=True' in the method call. Examples below.



# __Getting Started and Examples__

## __Installation__ (python 3)

```sh
$ pip install pandas_ta
```

## __Latest Version__
```sh
$ pip install -U git+https://github.com/twopirllc/pandas-ta
```

## __Quick Start__ using the DataFrame Extension

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

## __Module and Indicator Help__

```python
import pandas as pd
import pandas_ta as ta

# Help about this, 'ta', extension
help(pd.DataFrame().ta)

# List of all indicators
pd.DataFrame().ta.indicators()

# Help about the log_return indicator
help(ta.log_return)
```

## __New DataFrame Method__: _strategy_

Strategy is a new __Pandas (TA)__ method to facilitate bulk indicator processing. By default, running ```df.ta.strategy()``` will append __all
applicable__ indicators to DataFrame ```df```.  Utility methods like ```above```, ```below``` et al are not included.

* The ```ta.strategy()``` method is still __under development__. Future iterations will allow you to load a ```ta.json``` config file with your specific strategy name and parameters to automatically run you bulk indicators.


```python
# Runs and appends all indicators to the current DataFrame by default
# The resultant DataFrame will be large.
df.ta.strategy()
# Or equivalently use name='all'
df.ta.strategy(name='all')

# Use verbose if you want to make sure it is running.
df.ta.strategy(verbose=True)

# Maybe you do not want certain indicators.
# Just exclude (a list of) them.
df.ta.strategy(exclude=['bop', 'mom', 'percent_return', 'wcp', 'pvi'], verbose=True)

# Perhaps you want to use different values for indicators.
# This will run ALL indicators that have fast or slow as parameters.
# Check your results and exclude as necessary.
df.ta.strategy(fast=10, slow=50, verbose=True)

# Sanity check. Make sure all the columns are there
df.columns
```

## __New DataFrame kwargs__: _prefix_ and _suffix_

```python
prehl2 = df.ta.hl2(prefix="pre")
print(prehl2.name)  # "pre_HL2"

endhl2 = df.ta.hl2(suffix="end")
print(endhl2.name)  # "HL2_end"

bothhl2 = df.ta.hl2(prefix="pre", suffix="end")
print(bothhl2.name)  # "pre_HL2_end"
```

## __New DataFrame Properties__: _reverse_ & _datetime_ordered_

```python
# The 'reverse' is a helper property that returns the DataFrame
# in reverse order
df = df.ta.reverse

# The 'datetime_ordered' property returns True if the DataFrame
# index is of Pandas datetime64 and df.index[0] < df.index[-1]
# Otherwise it return False
time_series_in_order = df.ta.datetime_ordered
```

## __DataFrame Property__: *adjusted*

```python
# Set ta to default to an adjusted column, 'adj_close', overriding default 'close'
df.ta.adjusted = 'adj_close'
df.ta.sma(length=10, append=True)

# To reset back to 'close', set adjusted back to None
df.ta.adjusted = None
```

# __Technical Analysis Indicators__ (_by Category_)

## _Candles_ (1)

* _Heikin-Ashi_: **ha**

## _Momentum_ (25)

* _Awesome Oscillator_: **ao**
* _Absolute Price Oscillator_: **apo**
* _Bias_: **bias**
* _Balance of Power_: **bop**
* _BRAR_: **brar**
* _Commodity Channel Index_: **cci**
* _Center of Gravity_: **cg**
* _Chande Momentum Oscillator_: **cmo**
* _Coppock Curve_: **coppock**
* _Fisher Transform_: **fisher**
* _KDJ_: **kdj**
* _KST Oscillator_: **kst**
* _Moving Average Convergence Divergence_: **macd**
* _Momentum_: **mom**
* _Percentage Price Oscillator_: **ppo**
* _Psychological Line_: **psl**
* _Rate of Change_: **roc**
* _Relative Strength Index_: **rsi**
* _Relative Vigor Index_: **rvi**
* _Slope_: **slope*
* _Stochastic Oscillator_: **stoch**
* _Trix_: **trix**
* _True strength index_: **tsi**
* _Ultimate Oscillator_: **uo**
* _Williams %R_: **willr**


| _Moving Average Convergence Divergence_ (MACD) |
|:--------:|
| ![Example MACD](/images/SPY_MACD.png) |

## _Overlap_ (26)

* _Double Exponential Moving Average_: **dema**
* _Exponential Moving Average_: **ema**
* _Fibonacci's Weighted Moving Average_: **fwma**
* _High-Low Average_: **hl2**
* _High-Low-Close Average_: **hlc3**
    * Commonly known as 'Typical Price' in Technical Analysis literature
* _Hull Exponential Moving Average_: **hma**
* _Ichimoku Kinkō Hyō_: **ichimoku**
    * Use: help(ta.ichimoku). Returns two DataFrames.
* _Kaufman's Adaptive Moving Average_: **kama**
* _Linear Regression_: **linreg**
* _Midpoint_: **midpoint**
* _Midprice_: **midprice**
* _Open-High-Low-Close Average_: **ohlc4**
* _Pascal's Weighted Moving Average_: **pwma**
* _William's Moving Average_: **rma**
* _Sine Weighted Moving Average_: **sinwma**
* _Simple Moving Average_: **sma**
* _Supertrend_: **supertrend**
* _Symmetric Weighted Moving Average_: **swma**
* _T3 Moving Average_: **t3**
* _Triple Exponential Moving Average_: **tema**
* _Triangular Moving Average_: **trima**
* _Volume Weighted Average Price_: **vwap** 
* _Volume Weighted Moving Average_: **vwma**
* _Weighted Closing Price_: **wcp**
* _Weighted Moving Average_: **wma**
* _Zero Lag Moving Average_: **zlma**

| _Simple Moving Averages_ (SMA) and _Bollinger Bands_ (BBANDS) |
|:--------:|
| ![Example Chart](/images/TA_Chart.png) |

## _Performance_ (3)

Use parameter: cumulative=**True** for cumulative results.

* _Log Return_: **log_return**
* _Percent Return_: **percent_return**
* _Trend Return_: **trend_return**

| _Percent Return_ (Cumulative) with _Simple Moving Average_ (SMA) |
|:--------:|
| ![Example Cumulative Percent Return](/images/SPY_CumulativePercentReturn.png) |

## _Statistics_ (9)

* _Entropy_: **entropy**
* _Kurtosis_: **kurtosis**
* _Mean Absolute Deviation_: **mad**
* _Median_: **median**
* _Quantile_: **quantile**
* _Skew_: **skew**
* _Standard Deviation_: **stdev**
* _Variance_: **variance**
* _Z Score_: **zscore**

| _Z Score_ |
|:--------:|
| ![Example Z Score](/images/SPY_ZScore.png) |

## _Trend_ (14)

* _Average Directional Movement Index_: **adx**
* _Archer Moving Averages Trends_: **amat**
* _Aroon & Aroon Oscillator_: **aroon**
* _Choppiness Index_: **chop**
* _Chande Kroll Stop_: **cksp**
* _Decreasing_: **decreasing**
* _Detrended Price Oscillator_: **dpo**
* _Increasing_: **increasing**
* _Linear Decay_: **linear_decay**
* _Long Run_: **long_run**
* _Parabolic Stop and Reverse_: **psar**
* _Q Stick_: **qstick**
* _Short Run_: **short_run**
* _Vortex_: **vortex**

| _Average Directional Movement Index_ (ADX) |
|:--------:|
| ![Example ADX](/images/SPY_ADX.png) |

## _Utility_ (5)

* _Above_: **above**
* _Above Value_: **above_value**
* _Below_: **below**
* _Below Value_: **below_value**
* _Cross_: **cross**

## _Volatility_ (10)

* _Aberration_: **aberration**
* _Acceleration Bands_: **accbands**
* _Average True Range_: **atr**
* _Bollinger Bands_: **bbands**
* _Donchian Channel_: **donchian**
* _Keltner Channel_: **kc**
* _Mass Index_: **massi**
* _Normalized Average True Range_: **natr**
* _Price Distance_: **pdist**
* _True Range_: **true_range**

| _Average True Range_ (ATR) |
|:--------:|
| ![Example ATR](/images/SPY_ATR.png) |

## _Volume_ (13)

* _Accumulation/Distribution Index_: **ad**
* _Accumulation/Distribution Oscillator_: **adosc**
* _Archer On-Balance Volume_: **aobv**
* _Chaikin Money Flow_: **cmf**
* _Elder's Force Index_: **efi**
* _Ease of Movement_: **eom**
* _Money Flow Index_: **mfi**
* _Negative Volume Index_: **nvi**
* _On-Balance Volume_: **obv**
* _Positive Volume Index_: **pvi**
* _Price-Volume_: **pvol**
* _Price Volume Trend_: **pvt**
* _Volume Profile_: **vp**

| _On-Balance Volume_ (OBV) |
|:--------:|
| ![Example OBV](/images/SPY_OBV.png) |


# Contributors
* [allahyarzadeh](https://github.com/allahyarzadeh)
* [FGU1](https://github.com/FGU1)
* [lluissalord](https://github.com/lluissalord)


# Inspiration
* TradingView: http://www.tradingview.com
* Original TA-LIB: http://ta-lib.org/
* Bukosabino: https://github.com/bukosabino/ta

Please leave any comments, feedback, suggestions, or indicator requests.