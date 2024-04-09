<p align="center">
  <a href="https://github.com/twopirllc/pandas_ta">
    <img src="images/logo.png" alt="Pandas TA">
  </a>
</p>

# Pandas TA - A Technical Analysis Library in Python 3

[![license](https://img.shields.io/github/license/twopirllc/pandas-ta)](#license)
[![Python Version](https://img.shields.io/pypi/pyversions/pandas-ta?style=flat)](https://pypi.org/project/pandas_ta/)
[![PyPi Version](https://img.shields.io/pypi/v/pandas-ta?style=flat)](https://pypi.org/project/pandas_ta/)
[![Package Status](https://img.shields.io/pypi/status/pandas-ta?style=flat)](https://pypi.org/project/pandas_ta/)
[![Downloads](https://img.shields.io/pypi/dm/pandas_ta?style=flat)](https://pypistats.org/packages/pandas_ta)
[![Stars](https://img.shields.io/github/stars/twopirllc/pandas-ta?style=flat)](#stars)
[![Forks](https://img.shields.io/github/forks/twopirllc/pandas-ta?style=flat)](#forks)
[![Used By](https://img.shields.io/badge/used_by-258-orange.svg?style=flat)](#usedby)
[![Contributors](https://img.shields.io/github/contributors/twopirllc/pandas-ta?style=flat)](#contributors)
[![Issues](https://img.shields.io/github/issues-raw/twopirllc/pandas-ta?style=flat)](#issues)
[![Closed Issues](https://img.shields.io/github/issues-closed-raw/twopirllc/pandas-ta?style=flat)](#closed-issues)
[![Buy Me a Coffee](https://img.shields.io/badge/buy_me_a_coffee-orange.svg?style=flat)](https://www.buymeacoffee.com/twopirllc)

<br/>

![Example Chart](/images/SPY_Chart.png)
![Example Chart](/images/SPY_VOL.png)

<br/>

_Pandas Technical Analysis_ (**Pandas TA**) is a free, Open Source, and easy to use Technical Analysis library with a Pandas DataFrame Extension. It has over 200 indicators, utility functions and TA Lib Candlestick Patterns. Beyond TA feature generation, it has a flat library structure, it's own DataFrame Extension (called `ta`), Custom Indicator Sets (called a `Study`) and Custom Directory creation. Lastly, it includes methods to help with Data Acquisition and Stochastic Sampling, Backtesting Support with Signal and Trend methods, and some basic Performance Metrics.

<br/>

# **Contents**

<!--ts-->

- [Features](#features)
- [Used By](#used-by)
- [Sponsors](#sponsors)
- [Installation](#installation)
  - [Stable](#stable)
  - [Latest Version](#latest-version)
  - [Development Version](#development-version)
- [Quick Start](#quick-start)
- [Help](#help)
- [Issues and Contributions](#issues-and-contributions)
- [Programming Conventions](#programming-conventions)
  - [Standard](#standard)
  - [Pandas TA DataFrame Extension](#dataframe-extension)
  - [Pandas TA Study](#pandas-ta-study)
  - [Types of Studies](#types-of-studies)
  - [Multiprocessing](#multiprocessing)
- [DataFrame Extension Properties](#dataframe-extension-properties)
- [DataFrame Extension Methods](#dataframe-extension-methods)
- [Indicators by Category](#indicators-by-category)
  - [Candles](#candles-64)
  - [Cycles](#cycles-2)
  - [Momentum](#momentum-43)
  - [Overlap](#overlap-36)
  - [Performance](#performance-3)
  - [Statistics](#statistics-11)
  - [Transform](#transform-3)
  - [Trend](#trend-22)
  - [Utility](#utility-5)
  - [Volatility](#volatility-16)
  - [Volume](#volume-20)
- [Backtesting](#backtesting)
  - [Vector BT](#vector-bt)
- [BETA](#beta)
  - [Stochastic Samples](#stochastic-samples)
  - [Performance Metrics](#performance-metrics)
- [TODO](#todo)
- [Sources](#sources)
- [Support](#support)
<!--te-->

<br/>

# **Features**

## Large & Lite Weight Library

- Over 200 Indicators, Statistics and Candlestick Patterns.
  - Over 60 Candlestick Patterns with **[TA Lib](https://github.com/TA-Lib/ta-lib-python)** indicator integration.
- Flat library structure similar to **TA Lib**.
- Single dependency: [Pandas](https://pandas.pydata.org/)

## Accuracy

- Indicators are highly correlated, _r > 0.99_, with [TA Lib](https://github.com/TA-Lib/ta-lib-python) and builtin [TradingView](https://www.tradingview.com/) Indicators.
  - :chart_with_upwards_trend: Contributions are welcome for improved accuracy and performance.

## Performance

- Pandas TA is fast, with or without **TA Lib** or **Numba** installed, but one is not penalized if they are installed.
  - **TA Lib** computations are **enabled** by default. They can be disabled per indicator.
  - The library includes a performance method, `help(ta.speed_test)`, to check runtime indicator performance for a given _ohlcv_ DataFrame.
- Optionable **Multiprocessing** for a Pandas TA `Study`.
- Check Indicator Speeds on your system with the [Indicator Speed Check Notebook](https://github.com/twopirllc/pandas-ta/tree/main/examples/Speed_Check.ipynb).

## Bulk Processing

- Easily process many indicators using the DataFrame Extension method `df.ta.study()`.
- Supports two kinds of Studies.
  - **Builtin**: All, Categorical ("candles", "momentum", ...), and Common.
  - **Custom**: User Defined `Study` (formerly `Strategy`).

## Additional Features

- **Examples**
  - Basic usage and workflows. See the [**Example Jupyter Notebooks**](https://github.com/twopirllc/pandas-ta/tree/main/examples).
  - Creating Custom Studies using the [**Study** Class](https://github.com/twopirllc/pandas-ta/tree/main/examples/PandasTA_Study_Examples.ipynb).
    - **Study Customizations** including, but not limited to, applying _prefixes_ or _suffixes_ or _both_ to column/indicators names.
    - Composition/Chained Studies like putting **bbands** on **macd**.
- **Custom Indicators Directory**
  - Create and import a custom directory containing private indicators independent from the main library.
  - Use `help(ta.import_dir)` or read the `import_dir` method in [/pandas_ta/custom.py](https://github.com/twopirllc/pandas-ta/blob/main/pandas_ta/custom.py) for more information.
- **Data Acquisition**
  - Easily download _ohlcv_ data from [yfinance](https://github.com/ranaroussi/yfinance) or with the [Polygon API](https://github.com/pssolanki111/polygon).
  - See `help(ta.ticker)`, `help(ta.yf)`, `help(ta.polygon_api)` and examples below.
- **Stochastic Sample Generation** _BETA_
  - Built upon many of the Stochastic Processes from the [stochastic](https://github.com/crflynn/stochastic) package.
  - See `help(ta.sample)`.
- **Performance Metrics** _BETA_
  - A mini set of Performance Metrics.
    - :chart_with_upwards_trend: Contributions are welcome for improved accuracy and performance.
- **Backtesting Support** _BETA_
  - Easily generate Trading Signals for [**vectorbt**](https://github.com/polakowo/vectorbt) using `ta.tsignals()` or `ta.xsignals()` methods.

<br/>

Back to [Contents](#contents)

<br/>

# **Used By**

Pandas TA is used by Applications and Services like

## [Freqtrade](https://github.com/freqtrade/freqtrade)

> Freqtrade is a free and open source crypto trading bot written in Python. It is designed to support all major exchanges and be controlled via Telegram. It contains backtesting, plotting and money management tools as well as strategy optimization by machine learning.

<br/>

## [Open BB](https://openbb.co/)

#### Previously **Gamestonk Terminal**

> OpenBB is a leading open source investment analysis company.
> We represent millions of investors who want to leverage state-of-the-art data science and machine learning technologies to make sense of raw unrefined data. Our mission is to make investment research effective, powerful and accessible to everyone.

<br/>

## [QUANTCONNECT](https://www.quantconnect.com/)

> QUANTCONNECT powers your quantitative research with a cutting-edge, unified API for research, backtesting, and live trading on the world's leading algorithmic trading platform.

<br/>

## [Tune TA](https://github.com/jmrichardson/tuneta)

> TuneTA optimizes technical indicators using a distance correlation measure to a user defined target feature such as next day return. Indicator parameter(s) are selected using clustering techniques to avoid "peak" or "lucky" values. The set of tuned indicators can be ...

<br/>

## [VectorBT Pro](https://vectorbt.pro/)

> vectorbt PRO is the next-generation engine for backtesting, algorithmic trading, and research. It's a high-performance, actively-developed, commercial successor to the vectorbt library, one of the world's most innovative open-source backtesting engines. The PRO version extends the standard library with new impressive features and useful enhancements for professionals.

<br/>

# **Sponsors**

Thank you for your sponsorship of Pandas TA!

<a href="https://github.com/eervin123"><img src="https://avatars.githubusercontent.com/u/32274861?v=4" class="avatar-user" width="70px;" style="border-radius: 5px;"/></a>

<br/>

# **Installation**

The _minimum_ requirement is [Pandas](https://github.com/pandas-dev/pandas). Though not required, additional features _may_ require `numba`, `polygon`, `sklearn`, `statsmodels`, `stochastic`, `ta-lib`, `tqdm`, `vectorbt`, or `yfinance`.

- **Note**: `vectorbt` requires many of the additional packages listed.

<br/>

## Pip

The `pip` version, _0.3.14b_, is the last stable release. The next **major** release will occur when all the remaining _Hilbert Transform_ indicators from TA Lib are [included](https://github.com/twopirllc/pandas-ta/labels/help%20wanted).

```sh
$ pip install pandas_ta
```

How about **All**?

```sh
$ pip install pandas_ta[full]
```

<br/>

## Development Version

The _development_ version, _0.4.12b_, includes _numerous_ bug fixes, speed improvements and better documentation since release, _0.3.14b_.

```sh
$ pip install -U git+https://github.com/twopirllc/pandas-ta.git@development
```

Back to [Contents](#contents)

<br/>

# **Quick Start**

Indicators return either a Pandas Series or DataFrame.

- **Note:** _Volume Weighted Average Price_ (**vwap**) is the only indicator that requires a DatetimeIndex.

<br/>

## Simple Example

```python
import pandas as pd
import pandas_ta as ta

df = pd.DataFrame() # Empty DataFrame

# Load data
df = pd.read_csv("path/to/symbol.csv", sep=",")
# OR if you have yfinance installed
df = df.ta.ticker("aapl")

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

For a more descriptive Quick Start, please check out Michelangiolo Mazzeschi's Medium post: [Technical Analysis with Python: Quickstart Guide for Pandas TA](https://pub.towardsai.net/technical-analysis-with-python-quickstart-guide-for-pandas-ta-fe4b152e95a2).

<br/>

# **Help**

```python
import pandas as pd
import pandas_ta as ta

# Create a DataFrame so 'ta' can be used.
df = pd.DataFrame()

# Help about the DataFrame Extension: "ta"
help(df.ta)

# List of all indicators
df.ta.indicators()

# Help about an indicator such as adx
help(ta.adx)
```

Back to [Contents](#contents)

<br/>

# **Issues and Contributions**

Contributions, feedback, and bug squashing are integral to the success of this library. If you see something you can fix, _please_ do. Your contributon helps us all!

- :stop*sign: \_Please* **DO NOT** email me personally with Pandas TA Bugs, Issues or Feature Requests that are best handled with Github [Issues](https://github.com/twopirllc/pandas-ta/issues).

<br/>

## [Bugs, Indicators or Feature Requests](https://github.com/twopirllc/pandas-ta/issues)

1. Some bugs and features may already be be fixed or implemented in either the [Latest Version](#latest-version) or the the [Development Version](#development-version). _Please_ try them first.
1. If the _Latest_ or _Development_ Versions do not resolve the bug or address the Issue, try searching both _Open_ and _Closed_ Issues **before** opening a new Issue.
1. When creating a new Issue, please be as **detailed** as possible **with** reproducible code, links if any, applicable screenshots, errors, logs, and data samples.
   - You **will** be asked again for skipping form questions.
   - Do you have correlation analysis to back your claim?

<br/>

# **Contributors**

_Thank you for your contributions!_

<a href="https://github.com/AbyssAlora"><img src="https://avatars.githubusercontent.com/u/32155747?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/AStupidBear"><img src="https://avatars.githubusercontent.com/u/16422976?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/abmyii"><img src="https://avatars.githubusercontent.com/u/52673001?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/alexonab"><img src="https://avatars.githubusercontent.com/u/16689258?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/aligheshlaghi97"><img src="https://avatars.githubusercontent.com/u/121802083?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/allahyarzadeh"><img src="https://avatars.githubusercontent.com/u/11909557?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/amey-P"><img src="https://avatars.githubusercontent.com/u/3169893?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/anthotsang"><img src="https://avatars.githubusercontent.com/u/929793?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/argcast"><img src="https://avatars.githubusercontent.com/u/103273391?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/austinvdubs"><img src="https://avatars.githubusercontent.com/u/34928616?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/baotang2118"><img src="https://avatars.githubusercontent.com/u/42202403?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/bigtonylewis"><img src="https://avatars.githubusercontent.com/u/1799409?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/bizso09"><img src="https://avatars.githubusercontent.com/u/1904536?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/CMobley7"><img src="https://avatars.githubusercontent.com/u/10121829?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/codesutras"><img src="https://avatars.githubusercontent.com/u/56551122?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/DannyMartens"><img src="https://avatars.githubusercontent.com/u/37220423?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/DominiqueGarmier"><img src="https://avatars.githubusercontent.com/u/42445422?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/DrPaprikaa"><img src="https://avatars.githubusercontent.com/u/64958936?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/daikts"><img src="https://avatars.githubusercontent.com/u/64799229?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/danlim-wz"><img src="https://avatars.githubusercontent.com/u/52344837?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/delicateear"><img src="https://avatars.githubusercontent.com/u/167213?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/dorren"><img src="https://avatars.githubusercontent.com/u/27552?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/edwardwang1"><img src="https://avatars.githubusercontent.com/u/15675816?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"></a> <a href="https://github.com/emranalus"><img src="https://avatars.githubusercontent.com/u/39434120?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/FGU1"><img src="https://avatars.githubusercontent.com/u/56175843?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/FuzSolutions"><img src="https://avatars.githubusercontent.com/u/107435492?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/ffhirata"><img src="https://avatars.githubusercontent.com/u/44292530?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/floatinghotpot"><img src="https://avatars.githubusercontent.com/u/2339512?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/FriendlyUser"><img src="https://avatars.githubusercontent.com/u/13860264?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/GF-Huang"><img src="https://avatars.githubusercontent.com/u/4510984?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/GSlinger"><img src="https://avatars.githubusercontent.com/u/24567123?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/hhashim1"><img src="https://avatars.githubusercontent.com/u/62855649?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/jaggas"><img src="https://avatars.githubusercontent.com/u/10492880?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/jhleong"><img src="https://avatars.githubusercontent.com/u/1499913?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/JoeSchr"><img src="https://avatars.githubusercontent.com/u/8218910?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/Karsten-Fyhn"><img src="https://avatars.githubusercontent.com/u/70309439?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/koonom1985"><img src="https://avatars.githubusercontent.com/u/5298953?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/KRaw1"><img src="https://avatars.githubusercontent.com/u/77465250?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/khiemdoan"><img src="https://avatars.githubusercontent.com/u/15646249?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/kush99993s"><img src="https://avatars.githubusercontent.com/u/8145062?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/Larry-u"><img src="https://avatars.githubusercontent.com/u/18108119?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/lluissalord"><img src="https://avatars.githubusercontent.com/u/7021552?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/locupleto"><img src="https://avatars.githubusercontent.com/u/3994906?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/lucasmlofaro"><img src="https://avatars.githubusercontent.com/u/15791696?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/luisbarrancos"><img src="https://avatars.githubusercontent.com/u/387352?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/M6stafa"><img src="https://avatars.githubusercontent.com/u/7975309?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/Matoran"><img src="https://avatars.githubusercontent.com/u/4539516?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/MLpranav"><img src="https://avatars.githubusercontent.com/u/50073021?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/masafumimori"><img src="https://avatars.githubusercontent.com/u/71799690?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/maxdignan"><img src="https://avatars.githubusercontent.com/u/8184722?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/mchant"><img src="https://avatars.githubusercontent.com/u/8502845?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/mihakralj"><img src="https://avatars.githubusercontent.com/u/31756078?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/moritzgun"><img src="https://avatars.githubusercontent.com/u/68067719?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/NkosenhleDuma"><img src="https://avatars.githubusercontent.com/u/51145741?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/neuraldevelopment"><img src="https://avatars.githubusercontent.com/u/106029718?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/nicoloridulfo"><img src="https://avatars.githubusercontent.com/u/49532161?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/olafos"><img src="https://avatars.githubusercontent.com/u/2526551?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/oliver-zehentleitner"><img src="https://avatars.githubusercontent.com/u/47597331?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/patelpritesh"><img src="https://avatars.githubusercontent.com/u/6468739?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/pbrumblay"><img src="https://avatars.githubusercontent.com/u/2146159?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/polakowo"><img src="https://avatars.githubusercontent.com/u/2664108?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/pssolanki111"><img src="https://avatars.githubusercontent.com/u/40393715?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/RajeshDhalange"><img src="https://avatars.githubusercontent.com/u/32175897?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/Rossco8"><img src="https://avatars.githubusercontent.com/u/44757794?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/ramgarg102"><img src="https://avatars.githubusercontent.com/u/47526387?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/rengel8"><img src="https://avatars.githubusercontent.com/u/34138513?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/RichardFevrier"><img src="https://avatars.githubusercontent.com/u/5154754?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/Rossco8"><img src="https://avatars.githubusercontent.com/u/44757794?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/rao-abhishek"><img src="https://avatars.githubusercontent.com/u/59765588?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/rluong003"><img src="https://avatars.githubusercontent.com/u/42408939?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/ryanrussell"><img src="https://avatars.githubusercontent.com/u/523300?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/sampanacharya"><img src="https://avatars.githubusercontent.com/u/69064751?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/sgmheyhey"><img src="https://avatars.githubusercontent.com/u/30946314?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/SoftDevDanial"><img src="https://avatars.githubusercontent.com/u/64815604?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/schwaa"><img src="https://avatars.githubusercontent.com/u/2640598?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/TheWCKD"><img src="https://avatars.githubusercontent.com/u/37099416?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/tg12"><img src="https://avatars.githubusercontent.com/u/12201893?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/twrobel"><img src="https://avatars.githubusercontent.com/u/394724?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/UncleVasya"><img src="https://avatars.githubusercontent.com/u/1286157?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/WellMaybeItIs"><img src="https://avatars.githubusercontent.com/u/84646494?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/wassname"><img src="https://avatars.githubusercontent.com/u/1103714?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/whubsch"><img src="https://avatars.githubusercontent.com/u/24275736?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/winsonluk"><img src="https://avatars.githubusercontent.com/u/20024690?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/witokondoria"><img src="https://avatars.githubusercontent.com/u/5685669?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/wouldayajustlookatit"><img src="https://avatars.githubusercontent.com/u/44936661?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"></a> <a href="https://github.com/YuvalWein"><img src="https://avatars.githubusercontent.com/u/65113623?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a> <a href="https://github.com/zlpatel"><img src="https://avatars.githubusercontent.com/u/3293739?v=4" class="avatar-user" width="35px;" style="border-radius: 5px;"/></a>

<br/>

## How to [Contribute](https://github.com/twopirllc/pandas-ta/labels?sort=count-desc) or what [TODO](#todo)?

|                                |                                                                                                                                       |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| Satisfaction `or` Suggestions? | [Feedback](https://github.com/twopirllc/pandas-ta/labels/feedback)                                                                    |
| Knowledge `and` Experience?    | [Info](https://github.com/twopirllc/pandas-ta/labels/info)                                                                            |
| `!`hard                        | [Good First Issue](https://github.com/twopirllc/pandas-ta/labels/good%20first%20issue)                                                |
| A little more challenging?     | [Bugs](https://github.com/twopirllc/pandas-ta/labels/bug) / [Enhancements](https://github.com/twopirllc/pandas-ta/labels/enhancement) |
| Lonewolf?                      | [Help Wanted](https://github.com/twopirllc/pandas-ta/labels/help%20wanted)                                                            |

Back to [Contents](#contents)

<br/>

# **Programming Conventions**

**Pandas TA** supports _three_ Programming Conventions to make it easy to calculate or apply TA features. This includes the Standard, DataFrame Extension, and Pandas TA Study Conventions.

- **Note**: Each indicator either returns a _Series_ or a _DataFrame_ in Uppercase Underscore format regardless of style.

<br/>

## Standard

The Standard Convention is similar to TA Lib where one has to _explicitly_ define the input arguments and manage the resultant _Series_ or _DataFrame_.

- `sma10 = ta.sma(df["Close"], length=10)`
  - Returns a Series with name: `SMA_10`
- `donchiandf = ta.donchian(df["HIGH"], df["low"], lower_length=10, upper_length=15)`
  - Returns a DataFrame named `DC_10_15` and column names: `DCL_10_15, DCM_10_15, DCU_10_15`
- `ema10_ohlc4 = ta.ema(ta.ohlc4(df["Open"], df["High"], df["Low"], df["Close"]), length=10)`
  - Chaining indicators is possible but you have to be explicit.
  - Since it returns a Series named `EMA_10`. If needed, you may need to uniquely name it.

<br/>

## DataFrame Extension

The [DataFrame Extension](https://pandas.pydata.org/docs/development/extending.html) "ta", extends the DataFrame with additional properties and methods specific to the library. Unlike the _Standard Convention_, `df.ta` uses the _ohlcva_ columns as indicator arguments thus removing the need to specify the columns manually.

- `sma10 = df.ta.sma(length=10)`
  - Returns a Series with name: `SMA_10`
- `ema10_ohlc4 = df.ta.ema(close=df.ta.ohlc4(), length=10, suffix="OHLC4")`
  - Returns a Series with name: `EMA_10_OHLC4`
  - Chaining Indicators _requires_ specifying the input like: `close=df.ta.ohlc4()`.
- `donchiandf = df.ta.donchian(lower_length=10, upper_length=15)`
  - Returns a DataFrame named `DC_10_15` and column names: `DCL_10_15, DCM_10_15, DCU_10_15`

Same as the last three examples, but appending the results directly to the DataFrame `df`.

- `df.ta.sma(length=10, append=True)`
  - Appends to `df` column name: `SMA_10`.
- `df.ta.ema(close=df.ta.ohlc4(append=True), length=10, suffix="OHLC4", append=True)`
  - Chaining Indicators _requires_ specifying the input like: `close=df.ta.ohlc4()`.
- `df.ta.donchian(lower_length=10, upper_length=15, append=True)`
  - Appends to `df` with column names: `DCL_10_15, DCM_10_15, DCU_10_15`.

Back to [Contents](#contents)

<br/>

# **Pandas TA** _Study_

:stop_sign: The `Strategy` Class and `strategy()` are depreciated. Use `Study` Class and `study()` method instead.

The `Study` [_Dataclass_](https://docs.python.org/3/library/dataclasses.html) can be used to name and group indicators and are executed by the Extension `study()` method. A `Study` can range from _complex_ with _Composition/Chaining_ to _simple_ like a `CommonStudy`.

- Two premade _Studies_: `AllStudy` and `CommonStudy`.
- The `study()` method automatically appends to the DataFrame.
  - Can be disabled by using the argument: `append=False`.
- All Studies use **mulitprocessing** _except_ when the cpu `cores` are set to zero or when using the `col_names` argument (see [below](#multiprocessing)).
- A Study will fail when consumed by Pandas TA if there is no `{"kind": "indicator name"}` attribute. _Remember_ to check your spelling.
- For examples, see the [Pandas TA Study Examples Notebook](https://github.com/twopirllc/pandas-ta/blob/main/examples/PandasTA_Study_Examples.ipynb).

## _Required Arguments_

- **name**: Some short memorable string. _Note_: Case-insensitive "All" is reserved.
- **ta**: A list of dicts containing keyword arguments to identify the indicator and the indicator's arguments

## _Optional Arguments_

- **cores**: The number of cores to use for multiprocessing the **Study**. Default: `multiprocessing.cpu_count()`
- **description**: A more detailed description of what the Study tries to capture. Default: None
- **created**: At datetime string of when it was created. Default: Automatically generated.

<br/>

# Types of Studies

## _Builtin_

```python
# The Default Study: ta.AllStudy
# The following are equivalent:
df.ta.study()
df.ta.study("All")
df.ta.study(ta.AllStudy)

# CommonStudy
df.ta.study(ta.CommonStudy)
```

## _Categorical_

```python
# List of indicator categories
df.ta.categories

# Categorical Study requires a Category name
df.ta.study("Momentum") # Default values for all Momentum indicators

# Override all Overlap 'length' attributes
df.ta.study("overlap", length=42)
```

## _Custom_

```python
# Help
help(df.ta.study)

# Create a Custom Study
MyStudy = ta.Study(
    name="DCSMA10",
    description="SMA 50,200, BBANDS, RSI, MACD and Volume SMA 20",
    ta=[
        {"kind": "ohlc4"},
        {"kind": "sma", "length": 10},
        {"kind": "donchian", "lower_length": 10, "upper_length": 15},
        {"kind": "ema", "close": "OHLC4", "length": 10, "suffix": "OHLC4"},
    ]
)
# Run it
df.ta.study(MyStudy, **kwargs)
```

Back to [Contents](#contents)

<br/>

# **Multiprocessing**

The **Pandas TA** `study()` method utilizes **multiprocessing** for bulk indicator processing of all Study types with **ONE EXCEPTION!** When using the `col_names` parameter to rename resultant column(s), the indicators in `ta` array will be ran in order.

- Multiprocessing isn't free, it comes with the cost of spinning up a Multiprocessing Pool, so lowering or disabling the `cores` can improve bulk processing.

```python
# VWAP requires the DataFrame index to be a DatetimeIndex.
# * Replace "datetime" with the appropriate column from your DataFrame
df.set_index(pd.DatetimeIndex(df["datetime"]), inplace=True)

# Runs and appends all indicators to the current DataFrame by default
# The resultant DataFrame will be large.
df.ta.study()
# Or the string "all"
df.ta.study("all")
# Or the ta.AllStudy
df.ta.study(ta.AllStudy)

# Use verbose if you want to make sure it is running.
df.ta.study(verbose=True)

# Use timed if you want to see how long it takes to run.
df.ta.study(timed=True)

# Choose the number of cores to use.
# Default is all available cores.
# For no multiprocessing, set this value to 0.
df.ta.cores = 4

# Maybe you do not want certain indicators.
# Just exclude (a list of) them.
df.ta.study(exclude=["bop", "mom", "percent_return", "wcp", "pvi"], verbose=True)

# Perhaps you want to use different values for indicators.
# This will run ALL indicators that have fast or slow as arguments.
# Check your results and exclude as necessary.
df.ta.study(fast=10, slow=50, verbose=True)

# Sanity check. Make sure all the columns are there
df.columns
```

<br/>

## Custom Study without Multiprocessing

**Remember** These will not be utilizing **multiprocessing**

```python
NonMPStudy = ta.Study(
    name="EMAs, BBs, and MACD",
    description="Non Multiprocessing Study by rename Columns",
    ta=[
        {"kind": "ema", "length": 8},
        {"kind": "ema", "length": 21},
        {"kind": "bbands", "length": 20, "col_names": ("BBL", "BBM", "BBU")},
        {"kind": "macd", "fast": 8, "slow": 21, "col_names": ("MACD", "MACD_H", "MACD_S")}
    ]
)
# Run it
df.ta.study(NonMPStudy)
```

Back to [Contents](#contents)

<br/><br/>

# **DataFrame Extension Properties**

## **adjusted**

```python
# Set ta to default to an adjusted column, 'adj_close', overriding default 'close'.
df.ta.adjusted = "adj_close"
df.ta.sma(length=10, append=True)

# To reset back to 'close', set adjusted back to None.
df.ta.adjusted = None
```

## **cores**

```python
# Set the number of cores to use for Study multiprocessing
# Defaults to the number of cpus you have.
df.ta.cores = 4

# Set the number of cores to 0 for no multiprocessing.
df.ta.cores = 0

# Returns the number of cores you set or your default number of cpus.
df.ta.cores
```

## **exchange**

```python
# Sets the Exchange to use when calculating the last_run property. Default: "NYSE"
df.ta.exchange

# Set the Exchange.
# Available Exchanges: "ASX", "BMF", "DIFX", "FWB", "HKE", "JSE", "LSE", "NSE", "NYSE", "NZSX", "RTS", "SGX", "SSE", "TSE", "TSX"
df.ta.exchange = "LSE"
```

## **last_run**

```python
# Returns the time Pandas TA was last run as a string.
df.ta.last_run
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

## **time_range**

```python
# Returns the time range of the DataFrame as a float.
# By default, it returns the time in "years"
df.ta.time_range

# Available time_ranges include: "years", "months", "weeks", "days", "hours", "minutes". "seconds"
df.ta.time_range = "days"
df.ta.time_range # prints DataFrame time in "days" as float
```

Back to [Contents](#contents)

<br/><br/>

# **DataFrame Extension Methods**

These are some additional methods available to the DataFrame Extension.

<br/>

## **categories**

```python
# Returns a List of Pandas TA categories.
df.ta.categories()
```

<br/>

## **constants**

```python
import numpy as np

# Add constant '1' to the DataFrame
df.ta.constants(True, [1])
# Remove constant '1' to the DataFrame
df.ta.constants(False, [1])

# Adding constants for charting
chart_lines = np.append(np.arange(-4, 5, 1), np.arange(-100, 110, 10))
df.ta.constants(True, chart_lines)
# Removing some constants from the DataFrame
df.ta.constants(False, np.array([-60, -40, 40, 60]))
```

<br/>

## **datetime_ordered**

```python
# The 'datetime_ordered' method returns True if the DataFrame
# index is of Pandas datetime64 and df.index[0] < df.index[-1].
# Otherwise it returns False.
df.ta.datetime_ordered()
```

<br/>

## **indicators**

```python
# Prints the indicators and utility functions
df.ta.indicators()

# Returns a list of indicators and utility functions
ind_list = df.ta.indicators(as_list=True)

# Prints the indicators and utility functions that are not in the excluded list
df.ta.indicators(exclude=["cg", "pgo", "ui"])
# Returns a list of the indicators and utility functions that are not in the excluded list
smaller_list = df.ta.indicators(exclude=["cg", "pgo", "ui"], as_list=True)
```

<br/>

## **reverse**

```python
# The 'reverse' method returns the DataFrame in reverse order.
df.ta.reverse()
```

<br/>

## **study**

The heart of Pandas TA DataFrame Extension; formerly **strategy**. See the [Pandas TA Study](#pandas-ta-study) section for more details.

```python
# The 'study' method returns the DataFrame in reverse order.
df.ta.study(**kwargs)

# For list of arguments, see:
help(ta.study)
```

<br/>

## **ticker**

### [Yahoo Finance](https://github.com/ranaroussi/yfinance)

```python
# Download Chart history using yfinance. (pip install yfinance)
# It uses the same keyword arguments as yfinance (excluding start and end)
# Note: It automatically sets the index to be a DatetimeIndex
df = df.ta.ticker("aapl") # Default ticker is "SPY"

# Period is used instead of start/end
# Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# Default: "max"
df = df.ta.ticker("aapl", period="1y") # Gets this past year

# History by Interval by interval (including intraday if period < 60 days)
# Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# Default: "1d"
df = df.ta.ticker("aapl", period="1y", interval="1wk") # Gets this past year in weeks
df = df.ta.ticker("aapl", period="1mo", interval="1h") # Gets this past month in hours

# A Ticker & DataFrame Dictionary with a Study applied
tickers = ["SPY", "AAPL", "SQ"]
s = ta.CommonStudy
assets = {f"{t}_D": ta.df.ta.ticker(t, period="1y", cores=0, study=s, timed=True, returns=True, ds="yf") for t in tickers}
print(assets.keys())
spydf = assets["SPY_D"]

# For more info
help(ta.yf)
```

<br/>

## **to_utc**

```python
# Sets the DataFrame index to UTC format.
df.ta.to_utc()
```

<br/>

# **Indicators** (_by Category_)

### **Candles** (64)

Patterns that are **not bold**, require TA-Lib to be installed: `pip install TA-Lib`

- 2crows
- 3blackcrows
- 3inside
- 3linestrike
- 3outside
- 3starsinsouth
- 3whitesoldiers
- abandonedbaby
- advanceblock
- belthold
- breakaway
- closingmarubozu
- concealbabyswall
- counterattack
- darkcloudcover
- **doji**
- dojistar
- dragonflydoji
- engulfing
- eveningdojistar
- eveningstar
- gapsidesidewhite
- gravestonedoji
- hammer
- hangingman
- harami
- haramicross
- highwave
- hikkake
- hikkakemod
- homingpigeon
- identical3crows
- inneck
- **inside**
- invertedhammer
- kicking
- kickingbylength
- ladderbottom
- longleggeddoji
- longline
- marubozu
- matchinglow
- mathold
- morningdojistar
- morningstar
- onneck
- piercing
- rickshawman
- risefall3methods
- separatinglines
- shootingstar
- shortline
- spinningtop
- stalledpattern
- sticksandwich
- takuri
- tasukigap
- thrusting
- tristar
- unique3river
- upsidegap2crows
- xsidegap3methods
- _Heikin-Ashi_: **ha**
- _Z Score_: **cdl_z**

<br/>

```python
# Get all candle patterns (Default)
df = df.ta.cdl_pattern(name="all")

# Get only one pattern
df = df.ta.cdl_pattern(name="doji")

# Get some patterns
df = df.ta.cdl_pattern(name=["doji", "inside"])
```

Back to [Contents](#contents)

<br/>

### **Cycles** (2)

- _Even Better Sinewave_: **ebsw**
- _Reflex_: **reflex**
  - **trendflex** companion

<br/>

|     _Even Better Sinewave_ (EBSW)     |
| :-----------------------------------: |
| ![Example EBSW](/images/SPY_EBSW.png) |

<br/>

### **Momentum** (43)

- _Awesome Oscillator_: **ao**
- _Absolute Price Oscillator_: **apo**
- _Bias_: **bias**
- _Balance of Power_: **bop**
- _BRAR_: **brar**
- _Commodity Channel Index_: **cci**
- _Chande Forecast Oscillator_: **cfo**
- _Center of Gravity_: **cg**
- _Chande Momentum Oscillator_: **cmo**
- _Coppock Curve_: **coppock**
- _Connors Relative Strenght Index_: **crsi**
- _Correlation Trend Indicator_: **cti**
  - A wrapper for `ta.linreg(series, r=True)`
- _Directional Movement_: **dm**
- _Efficiency Ratio_: **er**
- _Elder Ray Index_: **eri**
- _Exhaustion Count_: **exhc**
  - Similar to TD Sequential
- _Fisher Transform_: **fisher**
- _Inertia_: **inertia**
- _KDJ_: **kdj**
- _KST Oscillator_: **kst**
- _Moving Average Convergence Divergence_: **macd**
- _Momentum_: **mom**
- _Pretty Good Oscillator_: **pgo**
- _Percentage Price Oscillator_: **ppo**
- _Psychological Line_: **psl**
- _Quantitative Qualitative Estimation_: **qqe**
- _Rate of Change_: **roc**
- _Relative Strength Index_: **rsi**
- _Relative Strength Xtra_: **rsx**
- _Relative Vigor Index_: **rvgi**
- _Schaff Trend Cycle_: **stc**
- _Slope_: **slope**
- _SMI Ergodic_ **smi**
- _Squeeze_: **squeeze**
  - Default is John Carter's. Enable Lazybear's with `lazybear=True`
- _Squeeze Pro_: **squeeze_pro**
- _Stochastic Oscillator_: **stoch**
- _Fast Stochastic Oscillator_: **stochf**
- _Stochastic RSI_: **stochrsi**
- _True Momentum Oscillator_: **tmo**
- _Trix_: **trix**
- _True strength index_: **tsi**
- _Ultimate Oscillator_: **uo**
- _Williams %R_: **willr**

<br/>

| _Moving Average Convergence Divergence_ (MACD) |
| :--------------------------------------------: |
|     ![Example MACD](/images/SPY_MACD.png)      |

Back to [Contents](#contents)

<br/>

### **Overlap** (36)

- _Bill Williams Alligator_: **alligator**
- _Arnaud Legoux Moving Average_: **alma**
- _Double Exponential Moving Average_: **dema**
- _Exponential Moving Average_: **ema**
- _Fibonacci's Weighted Moving Average_: **fwma**
- _Gann High-Low Activator_: **hilo**
- _High-Low Average_: **hl2**
- _High-Low-Close Average_: **hlc3**
  - Commonly known as 'Typical Price' in Technical Analysis literature
- _Hull Exponential Moving Average_: **hma**
- _Holt-Winter Moving Average_: **hwma**
- _Ichimoku Kinkō Hyō_: **ichimoku**
  - Returns two DataFrames. For more information: `help(ta.ichimoku)`.
  - `lookahead=False` drops the Chikou Span Column to prevent potential data leak.
- _Jurik Moving Average_: **jma**
- _Kaufman's Adaptive Moving Average_: **kama**
- _Linear Regression_: **linreg**
- _Ehler's MESA Adaptive Moving Average_: **mama**
  - Includes: **fama**
- _McGinley Dynamic_: **mcgd**
- _Midpoint_: **midpoint**
- _Midprice_: **midprice**
- _Open-High-Low-Close Average_: **ohlc4**
- _Pivots_: **pivots**
- _Pascal's Weighted Moving Average_: **pwma**
- _WildeR's Moving Average_: **rma**
- _Sine Weighted Moving Average_: **sinwma**
- _Simple Moving Average_: **sma**
- _Smoothed Moving Average_: **smma**
- _Ehler's Super Smoother Filter_: **ssf**
  - Potential data leak.
- _Ehler's Super Smoother Filter (3 Poles)_: **ssf3**
- _Supertrend_: **supertrend**
- _Symmetric Weighted Moving Average_: **swma**
- _T3 Moving Average_: **t3**
- _Triple Exponential Moving Average_: **tema**
- _Triangular Moving Average_: **trima**
- _Variable Index Dynamic Average_: **vidya**
- _Weighted Closing Price_: **wcp**
- _Weighted Moving Average_: **wma**
- _Zero Lag Moving Average_: **zlma**

<br/>

| _Exponential Moving Averages_ (EMA) and _Donchian Channels_ (KC) |
| :--------------------------------------------------------------: |
|             ![Example Chart](/images/SPY_Chart.png)              |

Back to [Contents](#contents)

<br/>

### **Performance** (3)

Use parameter: cumulative=**True** for cumulative results.

- _Draw Down_: **drawdown**
- _Log Return_: **log_return**
- _Percent Return_: **percent_return**

<br/>

| _Log Returns_ (Cumulative) with _Exponential Moving Average_ (EMA) |
| :----------------------------------------------------------------: |
|     ![Example Cumulative Percent Return](/images/SPY_CLR.png)      |

<br/>

### **Statistics** (11)

- _Entropy_: **entropy**
- _Kurtosis_: **kurtosis**
  - Potential data leak.
- _Mean Absolute Deviation_: **mad**
- _Median_: **median**
- _Quantile_: **quantile**
- _Skew_: **skew**
  - Potential data leak.
- _Standard Deviation_: **stdev**
- _Think or Swim Standard Deviation All_: **tos_stdevall**
  - Potential data leak.
- _Variance_: **variance**
- _Z Score_: **zscore**

<br/>

|      _Standard Deviation_ (STDEV)       |
| :-------------------------------------: |
| ![Example STDEV](/images/SPY_STDEV.png) |

Back to [Contents](#contents)

<br/>

### **Transform** (3)

- _Cube Transform_: **cube**
  - Potential data leak due to signal shift.
- _Inverse Fisher Transform_: **ifisher**
  - Potential data leak due to signal shift.
- _ReMap_: **remap**

<br/>

### **Trend** (22)

- _Average Directional Movement Index_: **adx**
  - Also includes **adxr**, **dmp** and **dmn** in the resultant DataFrame.
- _Alpha Trend_: **alphatrend**
- _Archer Moving Averages Trends_: **amat**
- _Aroon & Aroon Oscillator_: **aroon**
- _Choppiness Index_: **chop**
- _Chande Kroll Stop_: **cksp**
- _Decay_: **decay**
  - Formally: **linear_decay**
- _Decreasing_: **decreasing**
- _Detrended Price Oscillator_: **dpo**
  - Set `lookahead=False` to disable centering and remove potential data leak.
- _Hilbert Transform Trendline_: **ht_trendline**
- _Increasing_: **increasing**
- _Long Run_: **long_run**
- _Parabolic Stop and Reverse_: **psar**
- _Q Stick_: **qstick**
- _Random Walk Index_: **rwi**
- _Short Run_: **short_run**
- _Trendflex_: **trendflex**
  - **reflex** companion
- _Trend Signals_: **tsignals**
- _TTM Trend_: **ttm_trend**
- _Vertical Horizontal Filter_: **vhf**
- _Vortex_: **vortex**
- _Cross Signals_: **xsignals**

<br/>

| _Average Directional Movement Index_ (ADX) |
| :----------------------------------------: |
|    ![Example ADX](/images/SPY_ADX.png)     |

<br/>

### **Utility** (5)

- _Above_: **above**
- _Above Value_: **above_value**
- _Below_: **below**
- _Below Value_: **below_value**
- _Cross_: **cross**

Back to [Contents](#contents)

<br/>

### **Volatility** (16)

- _Aberration_: **aberration**
- _Acceleration Bands_: **accbands**
- _Average True Range_: **atr**
- _Average True Range Trailing Stop_: **atrts**
- _Bollinger Bands_: **bbands**
- _Chandelier Exit_: **chandelier_exit**
- _Donchian Channel_: **donchian**
- _Holt-Winter Channel_: **hwc**
- _Keltner Channel_: **kc**
- _Mass Index_: **massi**
- _Normalized Average True Range_: **natr**
- _Price Distance_: **pdist**
- _Relative Volatility Index_: **rvi**
- _Elder's Thermometer_: **thermo**
- _True Range_: **true_range**
- _Ulcer Index_: **ui**

<br/>

|     _Average True Range_ (ATR)      |
| :---------------------------------: |
| ![Example ATR](/images/SPY_ATR.png) |

<br/>

### **Volume** (20)

- _Accumulation/Distribution Index_: **ad**
- _Accumulation/Distribution Oscillator_: **adosc**
- _Archer On-Balance Volume_: **aobv**
- _Chaikin Money Flow_: **cmf**
- _Elder's Force Index_: **efi**
- _Ease of Movement_: **eom**
- _Klinger Volume Oscillator_: **kvo**
- _Money Flow Index_: **mfi**
- _Negative Volume Index_: **nvi**
- _On-Balance Volume_: **obv**
- _Positive Volume Index_: **pvi**
- _Percentage Volume Oscillator_: **pvo**
- _Price-Volume_: **pvol**
- _Price Volume Rank_: **pvr**
- _Price Volume Trend_: **pvt**
- _Volume Heat Map_: **vhm**
- _Volume Profile_: **vp**
- _Volume Weighted Average Price_: **vwap**
  - **Requires** the DataFrame index to be a DatetimeIndex
- _Volume Weighted Moving Average_: **vwma**
- _Worden Brothers Time Segmented Value_: **wb_tsv**

<br/>

|      _On-Balance Volume_ (OBV)      |
| :---------------------------------: |
| ![Example OBV](/images/SPY_OBV.png) |

Back to [Contents](#contents)

<br/>

# **Backtesting**

While Pandas TA is not a backtesting application, it does provide _two_ trend methods that generate trading signals for backtesting purposes: **Trend Signals** (`ta.tsignals()`) and **Cross Signals** (`ta.xsignals()`). Both Signal methods return a DataFrame with columns for the signal's Trend, Trades, Entries and Exits.

A simple manual backtest using **Trend Signals** can be found in the [TA Analysis Notebook](https://github.com/twopirllc/pandas-ta/blob/development/examples/TA_Analysis.ipynb) starting at _Trend Creation_ cell.

<br/>

## Trend Signals

- Useful for signals based on trends or **states**.
- _Examples_
  - **Golden Cross**: `df.ta.sma(length=50) > df.ta.sma(length=200)`
  - **Positive MACD Histogram**: `df.ta.macd().iloc[:,1] > 0`

## Cross Signals

- Useful for Signal Crossings or **events**.
- _Examples_
  - RSI crosses above 30 and then below 70
  - ZSCORE crosses above -2 and then below 2.

<br/>

## Vector BT

_Ideally_ a backtesting application like [**vectorbt**](https://polakowo.io/vectorbt/) should be used. For an example comparing a _Buy and Hold Strategy_ versus a _TA Signal Strategy_, see: [VectorBT Backtest with Pandas TA Notebook](https://github.com/twopirllc/pandas-ta/blob/main/examples/VectorBT_Backtest_with_Pandas_TA.ipynb).

<br/>

## Trend Signal Example

```python
import pandas_ta as ta
import vectorbt as vbt

# requires 'yfinance' installed
df = ta.df.ta.ticker("AAPL", timed=True)

# Create the "Golden Cross"
df["GC"] = df.ta.sma(50, append=True) > df.ta.sma(200, append=True)

# Create Trend Signals
golden = df.ta.tsignals(df.GC, asbool=True, append=True)

# Create the Signals Portfolio
pf = vbt.Portfolio.from_signals(df.close, entries=golden.TS_Entries, exits=golden.TS_Exits, freq="D", init_cash=100_000, fees=0.0025, slippage=0.0025)

# Print Portfolio Stats and Return Stats
print(pf.stats())
print(pf.returns_stats())
```

<br/>

## Cross Signal Example

```python
import pandas_ta as ta
import vectorbt as vbt

# requires 'yfinance' installed
df = ta.df.ta.ticker("AAPL", timed=True)

# Signal when RSI crosses above 30 and later below 70
rsi = df.ta.rsi(append=True)

# Create Cross Signals
rsi_long = ta.xsignals(rsi, 20, 80, above=True)

# Create the Signals Portfolio
pf = vbt.Portfolio.from_signals(df.Close, entries=rsi_long.TS_Entries, exits=rsi_long.TS_Exits, freq="D", init_cash=100_000, fees=0.0025, slippage=0.0025)

# Print Portfolio Stats and Return Stats
print(pf.stats())
print(pf.returns_stats())
```

Back to [Contents](#contents)

<br/>

# BETA

Pandas TA also includes basic _Performance Metrics_.

- :chart_with_upwards_trend: Contributions are welcome to improve and stablize them.

<br/>

Back to [Contents](#contents)

<br/>

## **Performance Metrics**

_Performance Metrics_ are a **new** addition to the package.These metrics return a _float_ and are _not_ part of the _DataFrame_ Extension. They are called using the _Standard Convention_.

```python
import pandas_ta as ta
result = ta.cagr(df.close)

# Help
help(ta.cagr)
```

## Metrics

The current metrics include:

- _Compounded Annual Growth Rate_: **cagr**
- _Calmar Ratio_: **calmar_ratio**
- _Downside Deviation_: **downside_deviation**
- _Jensen's Alpha_: **jensens_alpha**
- _Log Max Drawdown_: **log_max_drawdown**
- _Max Drawdown_: **max_drawdown**
- _Pure Profit Score_: **pure_profit_score**
- _Sharpe Ratio_: **sharpe_ratio**
- _Sortino Ratio_: **sortino_ratio**
- _Volatility_: **volatility**

Back to [Contents](#contents)

<br/>

## TODO

| **Status** | **Remaining TA Lib Indicators**                                                                 |
| ---------- | ----------------------------------------------------------------------------------------------- |
| &#9744;    | Indicators: `ht_dcperiod`, `ht_dcphase`, `ht_phasor`, `ht_sine`, `ht_trendline`, `ht_trendmode` |
| &#9744;    | **Numpy**/**Numba**_-ify_ base indicators                                                       |

<br/>

| **Status** | **Config System**                      |
| ---------- | -------------------------------------- |
| &#9744;    | Candlesticks                           |
| &#9744;    | DataFrame Extension property: `config` |
| &#9744;    | JSON Config File                       |
|            | &#9744; JSON Config File Format        |

<br/>

| **Status** | **Stabilize**              |
| ---------- | -------------------------- |
| &#9744;    | Trading Signals            |
|            | &#9744; Trend Signals      |
|            | &#9744; Cross Signals      |
| &#9744;    | Performance Metrics        |
| &#10004;   | Better argument validation |

<br/>

Back to [Contents](#contents)

<br/>

# **Sources**

### Technical Analysis

[Original TA-LIB](https://ta-lib.org/) | [TradingView](http://www.tradingview.com) | [Sierra Chart](https://search.sierrachart.com/?Query=indicators&submitted=true) | [MQL5](https://www.mql5.com) | [FM Labs](https://www.fmlabs.com/reference/default.htm) | [Pro Real Code](https://www.prorealcode.com/prorealtime-indicators) | [User 42](https://user42.tuxfamily.org/chart/manual/index.html) | [Technical Traders](http://technical.traders.com/tradersonline/FeedTT-2014.html)

### Supplemental

[What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)

<br/>

# **Support**

Like the package, want more indicators and features? Continued Support?

- Donations help cover data and API costs so platform indicators (like [TradingView](https://github.com/tradingview/)) are accurate.
- I appreciate **ALL** of those that have bought me Coffee/Beer/Wine et al. I greatly appreciate it! 😎

<br/>

### Consider

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/twopirllc)

<br/>

Back to [Contents](#contents)
