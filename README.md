[![Python Version](https://img.shields.io/pypi/pyversions/pandas_ta.svg)](https://pypi.org/project/pandas_ta/)
[![PyPi Version](https://img.shields.io/pypi/v/pandas_ta.svg)](https://pypi.org/project/pandas_ta/)
[![Package Status](https://img.shields.io/pypi/status/pandas_ta.svg)](https://pypi.org/project/pandas_ta/)
[![Downloads](https://img.shields.io/pypi/dm/pandas_ta.svg?style=flat)](https://pypistats.org/packages/pandas_ta)

# **Pandas TA**

![Example Chart](/images/TA_Chart.png)

## A Pandas Technical Analysis Library in _Python 3_

_Pandas Technical Analysis_ (**Pandas TA**) is an easy to use library that is built upon Python's Pandas library with more than 120 Indicators and Utility functions.  These indicators are commonly used for financial time series datasets with columns or labels: datetime, _open_, _high_, _low_, _close_, _volume_, et al.  Many commonly used indicators are included, such as: _Simple Moving Average_ (**sma**) _Moving Average Convergence Divergence_ (**macd**), _Hull Exponential Moving Average_ (**hma**), _Bollinger Bands_ (**bbands**), _On-Balance Volume_ (**obv**), _Aroon & Aroon Oscillator_ (**aroon**), _Squeeze_ (**squeeze**) and **many more**.

* **Pandas TA** has multiple ways of processing Technical Indicators to fit your programming style.
* The **primary** requirement to run indicators in [Pandas DataFrame Extension](https://pandas.pydata.org/pandas-docs/stable/extending.html) mode, is that _open, high, low, close, volume_ are **lowercase**.
* Each indicator either returns a Series or a DataFrame in Uppercase Underscore format.
    * For example, ```df.ta.macd(fast=12, slow=26, signal=9)``` will return a DataFrame with columns: ```['MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9']```.
        * When in doubt, use help(): ```help(ta.macd)```

## Pandas TA Issues, Ideas and Contributions

#### Thanks for trying **Pandas TA**!

Please take a moment to read **this** and the rest of this **README** before posting any issue.

* ### [Comments and Feedback](https://github.com/twopirllc/pandas-ta/issues)
    * Have you read the rest of **this** document?
    * Are you running the latest version?
        * ```pip install -U git+https://github.com/twopirllc/pandas-ta```
    * Have you tried the [Examples](https://github.com/twopirllc/pandas-ta/tree/master/examples/)?
        * Did they help?
        * What is missing?
        * Could you help improve them?
    * Did you know you can easily build _Custom Strategies_ with the **[Strategy](https://github.com/twopirllc/pandas-ta/blob/master/examples/PandasTA_Strategy_Examples.ipynb) Class**?
    * Documentation could always use improvement. Can you contribute?

* ### [Indicator or Feature Requests & Contributions](https://github.com/twopirllc/pandas-ta/issues)
    * Please be as detailed as possible. Links, screenshots, and sometimes data samples are welcome.
        * You want a new indicator not currently listed.
        * You want an alternate version of an existing indicator.
        * The indicator does not match another website, library, broker platform, language, et al.
            * Can you contribute?

## __Contributors__
Thank you for your contribution!

[alexonab](https://github.com/alexonab) | [allahyarzadeh](https://github.com/allahyarzadeh) | [codesutras](https://github.com/codesutras) | [DrPaprikaa](https://github.com/DrPaprikaa) | [FGU1](https://github.com/FGU1) | [lluissalord](https://github.com/lluissalord) | [maxdignan](https://github.com/maxdignan) | [SoftDevDanial](https://github.com/SoftDevDanial) | [YuvalWein](https://github.com/YuvalWein)

# __Pandas TA__ Features

* Has 120+ indicators and utility functions.
* Need _multiprocessing_ speed? Use the _strategy_ method.
* Easily add _prefixes_ or _suffixes_ or both to columns names. Useful for building Custom Strategies.
* __Extended Pandas DataFrame__ as 'ta'.
* Indicators are tightly correlated with the de facto [TA Lib](https://mrjbq7.github.io/ta-lib/) if they share common indicators.
* Example Jupyter Notebooks under the [examples](https://github.com/twopirllc/pandas-ta/tree/master/examples) directory, including how to create Custom Strategies using the new [__Strategy__ Class](https://github.com/twopirllc/pandas-ta/tree/master/examples/PandaTA_Strategy_Examples.ipynb)


# Changes
## __Recent Changes__
* A __Strategy__ Class to help name and group your favorite indicators.
* An experimental and independent __Watchlist__ Class located in the [Examples](https://github.com/twopirllc/pandas-ta/tree/master/examples/watchlist.py) Directory that can be used in conjunction with the new __Strategy__ Class.


## __Breaking Indicators__
* _Stochastic Oscillator_ (**stoch**): Now in line with Trading View's calculation. See: ```help(ta.stoch)```
* _Linear Decay_ (**linear_decay**): Renamed to _Decay_ (**decay**) and with the option for Exponential decay using ```mode="exp"```. See: ```help(ta.decay)```

## __New Indicators__
* _Chande Forecast Oscillator_ (**cfo**) It calculates the percentage difference between the actual price and the Time Series Forecast (the endpoint of a linear regression line).
* _Gann High-Low Activator_ (**hilo**) The Gann High Low Activator Indicator was created by Robert Krausz in a 1998.
* _Inside Bar_ (**cdl_inside**) An Inside Bar is a bar contained within it's previous bar's high and low See: ```help(ta.cdl_inside)```
* _SMI Ergodic_ (**smi**) Developed by William Blau, the SMI Ergodic Indicator is the same as the True Strength Index (TSI) except the SMI includes a signal line and oscillator.
* _Squeeze_ (**squeeze**). A Momentum indicator. Both John Carter's TTM **and** Lazybear's TradingView versions are implemented. The default is John Carter's, or ```lazybear=False```. Set ```lazybear=True``` to enable Lazybear's.
* _Stochastic RSI_ (**stochrsi**) "Stochastic RSI and Dynamic Momentum Index" was created by Tushar Chande and Stanley Kroll. In line with Trading View's calculation. See: ```help(ta.stochrsi)```
* _TTM Trend_ (**ttm_trend**). A trend indicator inspired from John Carter's book "Mastering the Trade".
issue of Stocks & Commodities Magazine. It is a moving average based trend
indicator consisting of two different simple moving averages.

## __Updated Indicators__
* _Average True Range_ (**atr**): Added option to return **atr** as a percentage. See: ```help(ta.atr)```
* _Fisher Transform_ (**fisher**): Added Fisher's default **ema** signal line. To change the length of the signal line, use the argument: ```signal=5```. Default: 5
* _Fisher Transform_ (**fisher**) and _Kaufman's Adaptive Moving Average_ (**kama**): Fixed a bug where their columns were not added to final DataFrame when using the _strategy_ method.
* _Trend Return_ (**trend_return**): Returns a DataFrame now instead of Series with pertinenet trade info for a _trend_. An example can be found in the [AI Example Notebook](https://github.com/twopirllc/pandas-ta/tree/master/examples/AIExample.ipynb). The notebook is still a work in progress and open to colloboration.

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
df = pd.read_csv("path/symbol.csv", sep=",")

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

## New Class: __Strategy__
### What is a Pandas TA Strategy?
A _Strategy_ is a simple way to name and group your favorite TA indicators. The _Strategy_ Class is a simple _Data Class_ to contain a list of indicators and their parameters.

* **Pandas** TA comes with two basic Strategies: __AllStrategy__ and __CommonStrategy__ to help you get started.

* A _Strategy_ Class can be as simple as the __CommonStrategy__ or more complex with a Composition of indicators such as the **ChainedTA** Example below.
    * You are using a Chained Strategy when you have the output of one indicator as input into one or more indicators in the same _Strategy_.
    * Use the 'prefix' and/or 'suffix' keywords to distuished the composed indicator from it's default Series.

* See the [Pandas TA Strategy Examples Notebook](https://github.com/twopirllc/pandas-ta/tree/master/examples/PandasTA_Strategy_Examples.ipynb) for examples including _Indicator Composition/Chaining_.

* __Note__: _Strategy_ is experimental and subject to change.

### Strategy Requirements:
- _name_: Some short memorable string.  _Note_: Case-insensitive "All" is reserved.
- _ta_: A list of dicts containing keyword arguments to identify the indicator and the indicator's arguments

### Optional Requirements:
- _description_: A more detailed description of what the Strategy tries to capture. Default: None
- _created_: At datetime string of when it was created. Default: Automatically generated.

#### Things to note:
- A Strategy will __fail__ when consumed by Pandas TA if there is no {"kind": "indicator name"} attribute. __Remember__ to check your spelling.

#### Examples
```python
# The Builtin "All" Strategy
ta.AllStrategy = ta.Strategy(
    name="All",
    description="All the indicators with their default settings. Pandas TA default.",
    ta=None
)

# The Builtin "Common" Strategy with Volume Chaining
ta.CommonStrategy = ta.Strategy(
    name="Common Price and Volume SMAs",
    description="Common Price SMAs: 10, 20, 50, 200 and Volume SMA: 20.",
    ta=[
        {"kind": "sma", "length": 10},
        {"kind": "sma", "length": 20},
        {"kind": "sma", "length": 50},
        {"kind": "sma", "length": 200},
        {"kind": "sma", "close": "volume", "length": 20, "prefix": "VOL"}
    ]
)

# Custom Strategy Example
CustomStrategy = ta.Strategy(
    name="Momo and Volatility",
    description="SMA 50,200, BBANDS, RSI, and MACD and TTM Squeeze",
    ta=[
        {"kind": "sma", "length": 50},
        {"kind": "sma", "length": 200},
        {"kind": "bbands", "length": 20},
        {"kind": "rsi"},
        {"kind": "macd", "fast": 8, "slow": 21},
        {"kind": "squeeze", "bb_std": 2.25, "mom_length": 10}
    ]
)

# Custom Chained Strategy
ChainedTA = ta.Strategy({
    "name": "HMA BBANDS",
    "description": "Bollinger Bands of an HMA(10) Chain",
    "name": [
        {"kind": "hma", "length": 10},
        # BBands close is now linked to HMA(10)'s result column
        # A prefix is used to distinguish it from BBands default close column
        {"kind": "bbands", "close": "HMA_10", "length": 20, "prefix": "HMA10"}, 
    ]
})
```

## __DataFrame Method__: _strategy_ with Multiprocessing

The new __Pandas (TA)__ method __strategy__ utilizes **multiprocessing**, for all Strategy types, to facilitate bulk indicator processing.

* This method **will** append __all applicable__ indicators to current DataFrame.
* Utility methods like ```above```, ```below``` et al are not included, however they can be included with Custom Strategies.
* **Known Issue:** Changing the default core count with a Custom Strategy that has Composition/Chaining may not append all columns.
    * **Solution:** leave the default core count alone.
* __Note__: The _strategy_ method is experimental and subject to change.


```python
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

## Running a Builtin, Categorical or Custom Strategy

### __Builtin__
```python
# Running the Builtin CommonStrategy as mentioned above
df.ta.strategy(ta.CommonStrategy)

# The Default Strategy is the ta.AllStrategy. The following are equivalent:
df.ta.strategy()
df.ta.strategy("All")
df.ta.strategy(ta.AllStrategy)
```

### __Categorical__
```python
# List of indicator categories
df.ta.categories

# Running a Categorical Strategy only requires the Category name
df.ta.strategy("Momentum") # Default values for all Momentum indicators
df.ta.strategy("overlap", length=42) # Override all Overlap 'length' attributes
```

### __Custom__
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

# __DataFrame Properties__:

## _adjusted_

```python
# Set ta to default to an adjusted column, 'adj_close', overriding default 'close'
df.ta.adjusted = "adj_close"
df.ta.sma(length=10, append=True)

# To reset back to 'close', set adjusted back to None
df.ta.adjusted = None
```

## _categories_

```python
# List of Pandas TA categories
df.ta.categories
```

## _cores_

```python
# Set the number of cores to use for strategy multiprocessing
# Defaults to the number of cpus you have
df.ta.cores = 4

# Returns the number of cores you set or your default number of cpus.
df.ta.cores
```

## _datetime_ordered_

```python
# The 'datetime_ordered' property returns True if the DataFrame
# index is of Pandas datetime64 and df.index[0] < df.index[-1]
# Otherwise it returns False
df.ta.datetime_ordered
```

## _reverse_

```python
# The 'datetime_ordered' property returns True if the DataFrame
# index is of Pandas datetime64 and df.index[0] < df.index[-1]
# Otherwise it returns False
df.ta.datetime_ordered

# The 'reverse' is a helper property that returns the DataFrame
# in reverse order
df.ta.reverse
```

## _prefix_ & _suffix_

```python
# Applying a prefix to the name of an indicator
prehl2 = df.ta.hl2(prefix="pre")
print(prehl2.name)  # "pre_HL2"

# Applying a suffix to the name of an indicator
endhl2 = df.ta.hl2(suffix="post")
print(endhl2.name)  # "HL2_post"

# Applying a prefix and suffix to the name of an indicator
bothhl2 = df.ta.hl2(prefix="pre", suffix="post")
print(bothhl2.name)  # "pre_HL2_post"
```

# __Technical Analysis Indicators__ (_by Category_)

## _Candles_ (3)

* _Doji_: **cdl_doji**
* _Inside Bar_: **cdl_inside**
* _Heikin-Ashi_: **ha**

## _Momentum_ (34)

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
* _Rate of Change_: **roc**
* _Relative Strength Index_: **rsi**
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

## _Overlap_ (27)

* _Double Exponential Moving Average_: **dema**
* _Exponential Moving Average_: **ema**
* _Fibonacci's Weighted Moving Average_: **fwma**
* _Gann High-Low Activator_: **hilo**
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

## _Trend_ (15)

* _Average Directional Movement Index_: **adx**
* _Archer Moving Averages Trends_: **amat**
* _Aroon & Aroon Oscillator_: **aroon**
* _Choppiness Index_: **chop**
* _Chande Kroll Stop_: **cksp**
* _Decay_: **decay**
    * Formally: **linear_decay**
* _Decreasing_: **decreasing**
* _Detrended Price Oscillator_: **dpo**
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

## _Utility_ (5)

* _Above_: **above**
* _Above Value_: **above_value**
* _Below_: **below**
* _Below Value_: **below_value**
* _Cross_: **cross**

## _Volatility_ (12)

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
* _True Range_: **true_range**
* _Ulcer Index_: **ui**

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


# Sources
* [Original TA-LIB](http://ta-lib.org/)
* [TradingView](http://www.tradingview.com)
* [Sierra Chart](https://search.sierrachart.com/?Query=indicators&submitted=true)
* [FM Labs](https://www.fmlabs.com/reference/default.htm)
* [User 42](https://user42.tuxfamily.org/chart/manual/index.html)

# Miscellaneous
## What is a Pandas DataFrame Extension?

A [Pandas DataFrame Extension](https://pandas.pydata.org/pandas-docs/stable/extending.html), extends a DataFrame allowing one to add more functionality and features to Pandas to suit your needs.  As such, it is now easier to run Technical Analysis on existing Financial Time Series without leaving the current DataFrame.  This extension by default returns the Indicator result or it can append the result to the existing DataFrame by including the parameter 'append=True' in the method call. Examples below.