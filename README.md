<p align="center">
  <a href="https://github.com/twopirllc/pandas_ta">
    <img src="images/logo.png" alt="Pandas TA">
  </a>
</p>

Pandas TA - A Technical Analysis Library in Python 3
=================

[![Python Version](https://img.shields.io/pypi/pyversions/pandas_ta.svg)](https://pypi.org/project/pandas_ta/)
[![PyPi Version](https://img.shields.io/pypi/v/pandas_ta.svg)](https://pypi.org/project/pandas_ta/)
[![Package Status](https://img.shields.io/pypi/status/pandas_ta.svg)](https://pypi.org/project/pandas_ta/)
[![Downloads](https://img.shields.io/pypi/dm/pandas_ta.svg?style=flat)](https://pypistats.org/packages/pandas_ta)
[![Contributors](https://img.shields.io/badge/contributors-19-orange.svg?style=flat)](#contributors-)
![Example Chart](/images/TA_Chart.png)


_Pandas Technical Analysis_ (**Pandas TA**) is an easy to use library that leverages the Pandas library with more than 130 Indicators and Utility functions. Many commonly used indicators are included, such as: _Simple Moving Average_ (**sma**) _Moving Average Convergence Divergence_ (**macd**), _Hull Exponential Moving Average_ (**hma**), _Bollinger Bands_ (**bbands**), _On-Balance Volume_ (**obv**), _Aroon & Aroon Oscillator_ (**aroon**), _Squeeze_ (**squeeze**) and **_many more_**.

<br/>

# **Table of contents**

<!--ts-->
* [Features](#features)
* [Installation](#installation)
    * [Stable](#stable)
    * [Latest Version](#latest-version)
    * [Cutting Edge](#cutting-edge)
* [Quick Start](#quick-start)
* [Help](#help)
* [Issues and Contributions](#issues-and-contributions)
* [Programming Conventions](#programming-conventions)
* [Pandas TA Strategies](#pandas-ta-strategies)
    * [Types of Strategies](#types-of-strategies)
* [DataFrame Properties](#dataframe-properties)
* [Indicators by Category](#indicators-by-category)
    * [Candles](#candles-3)
    * [Cycles](#cycles-1)
    * [Momentum](#momentum-36)
    * [Overlap](#overlap-31)
    * [Performance](#performance-4)
    * [Statistics](#statistics-9)
    * [Trend](#trend-15)
    * [Utility](#utility-5)
    * [Volatility](#volatility-13)
    * [Volume](#volume-14)
* [Performance Metrics](#performance-metrics)
* [Changes](#changes)
    * [General](#general)
    * [Breaking Indicators](#breaking-indicators)
    * [New Indicators](#new-indicators)
    * [Updated Indicators](#updated-indicators)
<!--te-->

<!-- * [Specifying Strategies in **Pandas TA**](#specifying-strategies-in-pandas-ta) -->
<!-- * [Multiprocessing](#multiprocessing) -->


<br/>

# **Features**

* Has 130+ indicators and utility functions.
* Indicators are tightly correlated with the de facto [TA Lib](https://mrjbq7.github.io/ta-lib/) if they share common indicators.
* Have the need for speed? By using the DataFrame _strategy_ method, you get **multiprocessing** for free!
* Easily add _prefixes_ or _suffixes_ or both to columns names. Useful for Custom Chained Strategies.
* Example Jupyter Notebooks under the [examples](https://github.com/twopirllc/pandas-ta/tree/master/examples) directory, including how to create Custom Strategies using the new [__Strategy__ Class](https://github.com/twopirllc/pandas-ta/tree/master/examples/PandaTA_Strategy_Examples.ipynb)
* Potential Data Leaks: **ichimoku** and **dpo**. See indicator list below for details.
* **UNDER DEVELOPMENT:** Performance Metrics

<br/>

**Installation**
===================

Stable
------
The ```pip``` version is the last most stable release. Version: *0.2.23b*
```sh
$ pip install pandas_ta
```

Latest Version
--------------
Best choice! Version: *0.2.45b*
```sh
$ pip install -U git+https://github.com/twopirllc/pandas-ta
```

Cutting Edge
------------
This is the _Development Version_ which could have bugs and other undesireable side effects. Use at own risk!
```sh
$ pip install -U git+https://github.com/twopirllc/pandas-ta.git@development
```

<br/>

 # **Quick Start**
```python
import pandas as pd
import pandas_ta as ta

# Load data
df = pd.read_csv("path/to/symbol.csv", sep=",")

# VWAP requires the DataFrame index to be a DatetimeIndex.
# Replace "datetime" with the appropriate column from your DataFrame
df.set_index(pd.DatetimeIndex(df["datetime"]), inplace=True)

# Calculate Returns and append to the df DataFrame
df.ta.log_return(cumulative=True, append=True)
df.ta.percent_return(cumulative=True, append=True)

# New Columns with results
df.columns

# Take a peek
df.tail()

# vv Continue Post Processing vv
```

<br/>

# **Help**
```python
import pandas as pd
import pandas_ta as ta

# Create a DataFrame so 'ta' can be used.
df = pd.DataFrame()

# Help about this, 'ta', extension
help(df.ta)

# List of all indicators
df.ta.indicators()

# Help about the log_return indicator
help(ta.log_return)
```
<br/>

# **Issues and Contributions**

Thanks for using **Pandas TA**!
<br/>

* ### [Comments and Feedback](https://github.com/twopirllc/pandas-ta/issues)
    * Have you read **_this_** document?
    * Are you running the latest version?
        * ```$ pip install -U git+https://github.com/twopirllc/pandas-ta```
    * Have you tried the [Examples](https://github.com/twopirllc/pandas-ta/tree/master/examples/)?
        * Did they help?
        * What is missing?
        * Could you help improve them?
    * Did you know you can easily build _Custom Strategies_ with the **[Strategy](https://github.com/twopirllc/pandas-ta/blob/master/examples/PandasTA_Strategy_Examples.ipynb) Class**?
    * Documentation could _always_ be improved. Can you help contribute?

* ### [Bugs, Indicators or Feature Requests](https://github.com/twopirllc/pandas-ta/issues)
    * First, search the _Closed_ Issues **before** you _Open_ a new Issue; it may have already been solved.
    * Please be as **detailed** as possible _with_ reproducible code, links if any, applicable screenshots, errors, logs, and data samples. You **will** be asked again if you provide nothing.
        * You want a new indicator not currently listed.
        * You want an alternate version of an existing indicator.
        * The indicator does not match another website, library, broker platform, language, et al.
            * Do you have correlation analysis to back your claim?
            * Can you contribute?
    * You will be asked to fill out an Issue even if you email my personal email address.


<br/>

**Contributors**
================

_Thank you for your contributions!_

[alexonab](https://github.com/alexonab) | [allahyarzadeh](https://github.com/allahyarzadeh) | [codesutras](https://github.com/codesutras) | [daikts](https://github.com/daikts) | [DrPaprikaa](https://github.com/DrPaprikaa) | [FGU1](https://github.com/FGU1) | [lluissalord](https://github.com/lluissalord) | [maxdignan](https://github.com/maxdignan) | [NkosenhleDuma](https://github.com/NkosenhleDuma) | [pbrumblay](https://github.com/pbrumblay) | [RajeshDhalange](https://github.com/RajeshDhalange) | [rengel8](https://github.com/rengel8) | [rluong003](https://github.com/rluong003) | [SoftDevDanial](https://github.com/SoftDevDanial) | [tg12](https://github.com/tg12) | [twrobel](https://github.com/twrobel) | [whubsch](https://github.com/whubsch) | [YuvalWein](https://github.com/YuvalWein)

<br/>

**Programming Conventions**
===========================

**Pandas TA** has three primary "styles" of processing Technical Indicators for your use case and/or requirements. They are: _Standard_, _DataFrame Extension_, and the _Pandas TA Strategy_. Each with increasing levels of abstraction for ease of use. As you become more familiar with **Pandas TA**, the simplicity and speed of using a _Pandas TA Strategy_ may become more apparent. Furthermore, you can create your own indicators through Chaining or Composition. Lastly, each indicator either returns a _Series_ or a _DataFrame_ in Uppercase Underscore format regardless of style.

<br/>

_Standard_
====================
You explicitly define the input columns and take care of the output.

* ```sma10 = ta.sma(df["Close"], length=10)```
    * Returns a Series with name: ```SMA_10```
* ```donchiandf = ta.donchian(df["HIGH"], df["low"], lower_length=10, upper_length=15)```
    * Returns a DataFrame named ```DC_10_15``` and column names: ```DCL_10_15, DCM_10_15, DCU_10_15```
* ```ema10_ohlc4 = ta.ema(ta.ohlc4(df["Open"], df["High"], df["Low"], df["Close"]), length=10)```
    * Chaining indicators is possible but you have to be explicit.
    * Since it returns a Series named ```EMA_10```. If needed, you may need to uniquely name it.

<br/>

_Pandas TA DataFrame Extension_
====================

Calling ```df.ta``` will automatically lowercase _OHLCVA_ to _ohlcva_: _open, high, low, close, volume_, _adj_close_. By default, ```df.ta``` will use the _ohlcva_ for the indicator arguments removing the need to specify input columns directly.
* ```sma10 = df.ta.sma(length=10)```
    * Returns a Series with name: ```SMA_10```
* ```ema10_ohlc4 = df.ta.ema(close=df.ta.ohlc4(), length=10, suffix="OHLC4")```
    * Returns a Series with name: ```EMA_10_OHLC4```
    * Chaining Indicators _require_ specifying the input like: ```close=df.ta.ohlc4()```.
* ```donchiandf = df.ta.donchian(lower_length=10, upper_length=15)```
    * Returns a DataFrame named ```DC_10_15``` and column names: ```DCL_10_15, DCM_10_15, DCU_10_15```

Same as the last three examples, but appending the results directly to the DataFrame ```df```.
* ```df.ta.sma(length=10, append=True)```
    * Appends to ```df``` column name: ```SMA_10```.
* ```df.ta.ema(close=df.ta.ohlc4(append=True), length=10, suffix="OHLC4", append=True)```
    * Chaining Indicators _require_ specifying the input like: ```close=df.ta.ohlc4()```.
* ```df.ta.donchian(lower_length=10, upper_length=15, append=True)```
    * Appends to ```df``` with column names: ```DCL_10_15, DCM_10_15, DCU_10_15```.

<br/>

_Pandas TA Strategy_
====================

A **Pandas TA** Strategy is a named group of indicators to be run by the _strategy_ method. All Strategies use **mulitprocessing** _except_ when using the ```col_names``` parameter (see [below](#multiprocessing)). There are different types of _Strategies_ listed in the following section.

<br/>

### Here are the previous _Styles_ implemented using a Strategy Class:
```python
# (1) Create the Strategy
MyStrategy = ta.Strategy(
    name="DCSMA10",
    ta=[
        {"kind": "ohlc4"},
        {"kind": "sma", "length": 10},
        {"kind": "donchian", "lower_length": 10, "upper_length": 15},
        {"kind": "ema", "close": "OHLC4", "length": 10, "suffix": "OHLC4"},
    ]
)

# (2) Run the Strategy
df.ta.strategy(MyStrategy, **kwargs)
```

<br/><br/>

# **Pandas TA** _Strategies_

The _Strategy_ Class is a simple way to name and group your favorite TA Indicators by using a _Data Class_. **Pandas TA** comes with two prebuilt basic Strategies to help you get started: __AllStrategy__ and __CommonStrategy__. A _Strategy_ can be as simple as the __CommonStrategy__ or as complex as needed using Composition/Chaining.

* When using the _strategy_ method, **all** indicators will be automatically appended to the DataFrame ```df```.
* You are using a Chained Strategy when you have the output of one indicator as input into one or more indicators in the same _Strategy_.
* **Note:** Use the 'prefix' and/or 'suffix' keywords to distinguish the composed indicator from it's default Series.

See the [Pandas TA Strategy Examples Notebook](https://github.com/twopirllc/pandas-ta/tree/master/examples/PandasTA_Strategy_Examples.ipynb) for examples including _Indicator Composition/Chaining_.

Strategy Requirements
---------------------
- _name_: Some short memorable string.  _Note_: Case-insensitive "All" is reserved.
- _ta_: A list of dicts containing keyword arguments to identify the indicator and the indicator's arguments
- **Note:** A Strategy will fail when consumed by Pandas TA if there is no ```{"kind": "indicator name"}``` attribute. _Remember_ to check your spelling.

Optional Parameters
-------------------
- _description_: A more detailed description of what the Strategy tries to capture. Default: None
- _created_: At datetime string of when it was created. Default: Automatically generated.

<br/>

Types of Strategies
=======================

## _Builtin_
```python
# Running the Builtin CommonStrategy as mentioned above
df.ta.strategy(ta.CommonStrategy)

# The Default Strategy is the ta.AllStrategy. The following are equivalent:
df.ta.strategy()
df.ta.strategy("All")
df.ta.strategy(ta.AllStrategy)
```

## _Categorical_
```python
# List of indicator categories
df.ta.categories

# Running a Categorical Strategy only requires the Category name
df.ta.strategy("Momentum") # Default values for all Momentum indicators
df.ta.strategy("overlap", length=42) # Override all Overlap 'length' attributes
```

## _Custom_
```python
# Create your own Custom Strategy
CustomStrategy = ta.Strategy(
    name="Momo and Volatility",
    description="SMA 50,200, BBANDS, RSI, MACD and Volume SMA 20",
    ta=[
        {"kind": "sma", "length": 50},
        {"kind": "sma", "length": 200},
        {"kind": "bbands", "length": 20},
        {"kind": "rsi"},
        {"kind": "macd", "fast": 8, "slow": 21},
        {"kind": "sma", "close": "volume", "length": 20, "prefix": "VOLUME"},
    ]
)
# To run your "Custom Strategy"
df.ta.strategy(CustomStrategy)
```

<br/>

**Multiprocessing**
=======================

The **Pandas TA** _strategy_ method utilizes **multiprocessing** for bulk indicator processing of all Strategy types with **ONE EXCEPTION!** When using the ```col_names``` parameter to rename resultant column(s), the indicators in ```ta``` array will be ran in order.

```python
# VWAP requires the DataFrame index to be a DatetimeIndex.
# * Replace "datetime" with the appropriate column from your DataFrame
df.set_index(pd.DatetimeIndex(df["datetime"]), inplace=True)

# Runs and appends all indicators to the current DataFrame by default
# The resultant DataFrame will be large.
df.ta.strategy()
# Or the string "all"
df.ta.strategy("all")
# Or the ta.AllStrategy
df.ta.strategy(ta.AllStrategy)

# Use verbose if you want to make sure it is running.
df.ta.strategy(verbose=True)

# Use timed if you want to see how long it takes to run.
df.ta.strategy(timed=True)

# Choose the number of cores to use. Default is all available cores.
# For no multiprocessing, set this value to 0.
df.ta.cores = 4

# Maybe you do not want certain indicators.
# Just exclude (a list of) them.
df.ta.strategy(exclude=["bop", "mom", "percent_return", "wcp", "pvi"], verbose=True)

# Perhaps you want to use different values for indicators.
# This will run ALL indicators that have fast or slow as parameters.
# Check your results and exclude as necessary.
df.ta.strategy(fast=10, slow=50, verbose=True)

# Sanity check. Make sure all the columns are there
df.columns
```

<br/>

## Custom Strategy without Multiprocessing
**Remember** These will not be utilizing **multiprocessing** 
```python
NonMPStrategy = ta.Strategy(
    name="EMAs, BBs, and MACD",
    description="Non Multiprocessing Strategy by rename Columns",
    ta=[
        {"kind": "ema", "length": 8},
        {"kind": "ema", "length": 21},
        {"kind": "bbands", "length": 20, "col_names": ("BBL", "BBM", "BBU")},
        {"kind": "macd", "fast": 8, "slow": 21, "col_names": ("MACD", "MACD_H", "MACD_S")}
    ]
)
# Run it
df.ta.strategy(NonMPStrategy)
```

<br/><br/>


# **DataFrame Properties**

## **adjusted**

```python
# Set ta to default to an adjusted column, 'adj_close', overriding default 'close'.
df.ta.adjusted = "adj_close"
df.ta.sma(length=10, append=True)

# To reset back to 'close', set adjusted back to None.
df.ta.adjusted = None
```

## **categories**

```python
# List of Pandas TA categories.
df.ta.categories
```

## **cores**

```python
# Set the number of cores to use for strategy multiprocessing
# Defaults to the number of cpus you have.
df.ta.cores = 4

# Set the number of cores to 0 for no multiprocessing.
df.ta.cores = 0

# Returns the number of cores you set or your default number of cpus.
df.ta.cores
```

## **datetime_ordered**

```python
# The 'datetime_ordered' property returns True if the DataFrame
# index is of Pandas datetime64 and df.index[0] < df.index[-1].
# Otherwise it returns False.
df.ta.datetime_ordered
```

## **reverse**

```python
# The 'reverse' is a helper property that returns the DataFrame
# in reverse order.
df.ta.reverse
```

## **prefix & suffix**

```python
# Applying a prefix to the name of an indicator.
prehl2 = df.ta.hl2(prefix="pre")
print(prehl2.name)  # "pre_HL2"

# Applying a suffix to the name of an indicator.
endhl2 = df.ta.hl2(suffix="post")
print(endhl2.name)  # "HL2_post"

# Applying a prefix and suffix to the name of an indicator.
bothhl2 = df.ta.hl2(prefix="pre", suffix="post")
print(bothhl2.name)  # "pre_HL2_post"
```

<br/><br/>

# **Indicators** (_by Category_)
### **Candles** (3)

* _Doji_: **cdl_doji**
* _Inside Bar_: **cdl_inside**
* _Heikin-Ashi_: **ha**


### **Cycles** (1)

* _Even Better Sinewave_: **ebsw**

### **Momentum** (36)

* _Awesome Oscillator_: **ao**
* _Absolute Price Oscillator_: **apo**
* _Bias_: **bias**
* _Balance of Power_: **bop**
* _BRAR_: **brar**
* _Commodity Channel Index_: **cci**
* _Chande Forecast Oscillator_: **cfo**
* _Center of Gravity_: **cg**
* _Chande Momentum Oscillator_: **cmo**
* _Coppock Curve_: **coppock**
* _Efficiency Ratio_: **er**
* _Elder Ray Index_: **eri**
* _Fisher Transform_: **fisher**
* _Inertia_: **inertia**
* _KDJ_: **kdj**
* _KST Oscillator_: **kst**
* _Moving Average Convergence Divergence_: **macd**
* _Momentum_: **mom**
* _Pretty Good Oscillator_: **pgo**
* _Percentage Price Oscillator_: **ppo**
* _Psychological Line_: **psl**
* _Percentage Volume Oscillator_: **pvo**
* _Quantitative Qualitative Estimation_: **qqe**
* _Rate of Change_: **roc**
* _Relative Strength Index_: **rsi**
* _Relative Strength Xtra_: **rsx**
* _Relative Vigor Index_: **rvgi**
* _Slope_: **slope**
* _SMI Ergodic_ **smi**
* _Squeeze_: **squeeze**
    * Default is John Carter's. Enable Lazybear's with ```lazybear=True```
* _Stochastic Oscillator_: **stoch**
* _Stochastic RSI_: **stochrsi**
* _Trix_: **trix**
* _True strength index_: **tsi**
* _Ultimate Oscillator_: **uo**
* _Williams %R_: **willr**


| _Moving Average Convergence Divergence_ (MACD) |
|:--------:|
| ![Example MACD](/images/SPY_MACD.png) |

### **Overlap** (31)

* _Arnaud Legoux Moving Average_: **alma**
* _Double Exponential Moving Average_: **dema**
* _Exponential Moving Average_: **ema**
* _Fibonacci's Weighted Moving Average_: **fwma**
* _Gann High-Low Activator_: **hilo**
* _High-Low Average_: **hl2**
* _High-Low-Close Average_: **hlc3**
    * Commonly known as 'Typical Price' in Technical Analysis literature
* _Hull Exponential Moving Average_: **hma**
* _Holt-Winter Moving Average_: **hwma**
* _Ichimoku Kinkō Hyō_: **ichimoku**
    * Use: help(ta.ichimoku). Returns two DataFrames.
    * Drop the Chikou Span Column, the final column of the first resultant DataFrame, remove potential data leak.
* _Kaufman's Adaptive Moving Average_: **kama**
* _Linear Regression_: **linreg**
* _McGinley Dynamic_: **mcgd**
* _Midpoint_: **midpoint**
* _Midprice_: **midprice**
* _Open-High-Low-Close Average_: **ohlc4**
* _Pascal's Weighted Moving Average_: **pwma**
* _WildeR's Moving Average_: **rma**
* _Sine Weighted Moving Average_: **sinwma**
* _Simple Moving Average_: **sma**
* _Ehler's Super Smoother Filter_: **ssf**
* _Supertrend_: **supertrend**
* _Symmetric Weighted Moving Average_: **swma**
* _T3 Moving Average_: **t3**
* _Triple Exponential Moving Average_: **tema**
* _Triangular Moving Average_: **trima**
* _Variable Index Dynamic Average_: **vidya**
* _Volume Weighted Average Price_: **vwap**
    * **Requires** the DataFrame index to be a DatetimeIndex
* _Volume Weighted Moving Average_: **vwma**
* _Weighted Closing Price_: **wcp**
* _Weighted Moving Average_: **wma**
* _Zero Lag Moving Average_: **zlma**

| _Simple Moving Averages_ (SMA) and _Bollinger Bands_ (BBANDS) |
|:--------:|
| ![Example Chart](/images/TA_Chart.png) |


### **Performance** (4)

Use parameter: cumulative=**True** for cumulative results.

* _Draw Down_: **drawdown**
* _Log Return_: **log_return**
* _Percent Return_: **percent_return**
* _Trend Return_: **trend_return**

| _Percent Return_ (Cumulative) with _Simple Moving Average_ (SMA) |
|:--------:|
| ![Example Cumulative Percent Return](/images/SPY_CumulativePercentReturn.png) |


### **Statistics** (9)

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

### **Trend** (15)

* _Average Directional Movement Index_: **adx**
    * Also includes **dmp** and **dmn** in the resultant DataFrame.
* _Archer Moving Averages Trends_: **amat**
* _Aroon & Aroon Oscillator_: **aroon**
* _Choppiness Index_: **chop**
* _Chande Kroll Stop_: **cksp**
* _Decay_: **decay**
    * Formally: **linear_decay**
* _Decreasing_: **decreasing**
* _Detrended Price Oscillator_: **dpo**
    * Set ```centered=False``` to remove potential data leak.
* _Increasing_: **increasing**
* _Long Run_: **long_run**
* _Parabolic Stop and Reverse_: **psar**
* _Q Stick_: **qstick**
* _Short Run_: **short_run**
* _TTM Trend_: **ttm_trend**
* _Vortex_: **vortex**

| _Average Directional Movement Index_ (ADX) |
|:--------:|
| ![Example ADX](/images/SPY_ADX.png) |

### **Utility** (5)

* _Above_: **above**
* _Above Value_: **above_value**
* _Below_: **below**
* _Below Value_: **below_value**
* _Cross_: **cross**

### **Volatility** (13)

* _Aberration_: **aberration**
* _Acceleration Bands_: **accbands**
* _Average True Range_: **atr**
* _Bollinger Bands_: **bbands**
* _Donchian Channel_: **donchian**
* _Keltner Channel_: **kc**
* _Mass Index_: **massi**
* _Normalized Average True Range_: **natr**
* _Price Distance_: **pdist**
* _Relative Volatility Index_: **rvi**
* _Elder's Thermometer_: **thermo**
* _True Range_: **true_range**
* _Ulcer Index_: **ui**

| _Average True Range_ (ATR) |
|:--------:|
| ![Example ATR](/images/SPY_ATR.png) |

### **Volume** (14)

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
* _Price Volume Rank_: **pvr**
* _Price Volume Trend_: **pvt**
* _Volume Profile_: **vp**

| _On-Balance Volume_ (OBV) |
|:--------:|
| ![Example OBV](/images/SPY_OBV.png) |

<br/><br/>

# **Performance Metrics** &nbsp; _BETA_
_Performance Metrics_ are a **new** addition to the package and consequentially are likely unreliable. **Use at your own risk.** These metrics return a _float_ and are _not_ part of the _DataFrame_ Extension. They are called the Standard way. For Example:

```python
import pandas_ta as ta
result = ta.cagr(df.close)
```

### Available Metrics
* _Compounded Annual Growth Rate_: **cagr**
* _Calmar Ratio_: **calmar_ratio**
* _Downside Deviation_: **downside_deviation**
* _Jensen's Alpha_: **jensens_alpha**
* _Log Max Drawdown_: **log_max_drawdown**
* _Max Drawdown_: **max_drawdown**
* _Pure Profit Score_: **pure_profit_score**
* _Sharpe Ratio_: **sharpe_ratio**
* _Sortino Ratio_: **sortino_ratio**
* _Volatility_: **volatility**


<br/><br/>

# **Changes**
## **General**
* A __Strategy__ Class to help name and group your favorite indicators.
* Some indicators have had their ```mamode``` _kwarg_ updated with more _moving average_ choices with the **Moving Average Utility** function ```ta.ma()```. For simplicity, all _choices_ are single source _moving averages_. This is primarily an internal utility used by indicators that have a ```mamode``` _kwarg_. This includes indicators: _accbands_, _amat_, _aobv_, _atr_, _bbands_, _bias_, _efi_, _hilo_, _kc_, _natr_, _qqe_, _rvi_, and _thermo_; the default ```mamode``` parameters have not changed. However, ```ta.ma()``` can be used by the user as well if needed. For more information: ```help(ta.ma)```
    * **Moving Average Choices**: dema, ema, fwma, hma, linreg, midpoint, pwma, rma, sinwma, sma, swma, t3, tema, trima, vidya, wma, zlma.
* An _experimental_ and independent __Watchlist__ Class located in the [Examples](https://github.com/twopirllc/pandas-ta/tree/master/examples/watchlist.py) Directory that can be used in conjunction with the new __Strategy__ Class.
* _Linear Regression_ (**linear_regression**) is a new utility method for Simple Linear Regression using _Numpy_ or _Scikit Learn_'s implementation.
* Added utility/convience function, ```to_utc```, to convert the DataFrame index to UTC. See: ```help(ta.to_utc)```

<br />

## **Breaking Indicators**
* _Bollinger Bands_ (**bbands**): New column 'bandwidth' appended to the returning DataFrame. See: ```help(ta.bbands)```
* _Volume Weighted Average Price_ (**vwap**): **Requires** the DataFrame index to be a DatetimeIndex.


## **New Indicators**
* _Arnaud Legoux Moving Average_ (**alma**) uses the curve of the Normal (Gauss) distribution to allow regulating the smoothness and high sensitivity of the indicator. See: ```help(ta.alma)```
* _Drawdown_ (**drawdown**) shows the peak-to-trough decline during a specific period for an investment,
trading account, or fund. See: ```help(ta.drawdown)```
* _Even Better Sinewave_ (**ebsw**) measures market cycles and uses a low pass filter to remove noise. See: ```help(ta.ebsw)```
* _Gann High-Low Activator_ (**hilo**) was created by Robert Krausz in a 1998. See: ```help(ta.hilo)```
* _Holt-Winter Moving Average_ (**hwma**) is a three-parameter moving average by the Holt-Winter method.
* _McGinley Dynamic_ (**mcgd**) is an overlap indicator developed by John R. McGinley, a Certified Market Technician. See: ```help(ta.mcgd)```
* _Price Volume Rank_ (**pvr**) was created by Anthony J. Macek. See: ```help(ta.pvr)```
* _Quantitative Qualitative Estimation_ (**qqe**) is like SuperTrend for a Smoothed RSI. See: ```help(ta.qqe)```
article in the June, 1994 issue of Technical Analysis of Stocks & Commodities Magazine. See: ```help(ta.pvr)```
* _Relative Strength Xtra_ (**rsx**) is based on the popular RSI indicator and inspired by the work Jurik Research. See: ```help(ta.rsx)```
* _Ehler's Super Smoother Filter_ (**ssf**). Ehler's solution to reduce lag and remove aliasing noise compared to other common moving average indicators. See: ```help(ta.ssf)```
* _Elder's Thermometer_ (**thermo**) measures price volatility. See: ```help(ta.thermo)```
* _TTM Trend_ (**ttm_trend**) is a trend indicator inspired from John Carter's book "Mastering the Trade" issue of Stocks & Commodities Magazine. It is a moving average based trend indicator consisting of two different simple moving averages. See: ```help(ta.ttm_trend)```
* _Variable Index Dynamic Average_ (**vidya**) is a popular Dynamic Moving Average created by Tushar Chande. See: ```help(ta.vidya)```

## **Updated Indicators**
* _Average True Range_ (**atr**): The default ```mamode``` is now "**RMA**" and with the same ```mamode``` options as TradingView. See ```help(ta.atr)```.
* _Decreasing_ (**decreasing**): New argument ```strict``` checks if the series is continuously decreasing over period ```length```. Default: ```False```. See ```help(ta.decreasing)```.
* _Increasing_ (**increasing**): New argument ```strict``` checks if the series is continuously increasing over period ```length```. Default: ```False```. See ```help(ta.increasing)```.
* _Trend Return_ (**trend_return**): Returns a DataFrame now instead of Series with pertinenet trade info for a _trend_. An example can be found in the [AI Example Notebook](https://github.com/twopirllc/pandas-ta/tree/master/examples/AIExample.ipynb). The notebook is still a work in progress and open to colloboration.
* _Volume Weighted Average Price_ (**vwap**) Added a new parameter called ```anchor```. Default: "D" for "Daily". See [Timeseries Offset Aliases](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases) for additional options. **Requires** the DataFrame index to be a DatetimeIndex

<br />

# **Sources**
[Original TA-LIB](http://ta-lib.org/) | [TradingView](http://www.tradingview.com) | [Sierra Chart](https://search.sierrachart.com/?Query=indicators&submitted=true) | [MQL5](https://www.mql5.com) | [FM Labs](https://www.fmlabs.com/reference/default.htm) | [Pro Real Code](https://www.prorealcode.com/prorealtime-indicators) | [User 42](https://user42.tuxfamily.org/chart/manual/index.html)