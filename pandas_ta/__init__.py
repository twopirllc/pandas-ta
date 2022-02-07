"""
.. moduleauthor:: Kevin Johnson
"""
name = "pandas_ta"

# Dictionaries and version
from pandas_ta.maps import EXCHANGE_TZ, RATE, Category, Imports, version
from pandas_ta.utils import *

# Flat Structure. Supports ta.ema() or ta.overlap.ema() calls.
from pandas_ta.candles import *
from pandas_ta.cycles import *
from pandas_ta.momentum import *
from pandas_ta.overlap import *
from pandas_ta.performance import *
from pandas_ta.statistics import *
from pandas_ta.transform import *
from pandas_ta.trend import *
from pandas_ta.volatility import *
from pandas_ta.volume import *

# Common Averages useful for Indicators with a mamode argument, like ta.adx()
from pandas_ta.ma import ma

# Custom External Directory Commands. See help(import_dir)
from pandas_ta.custom import create_dir, import_dir

# Enable "ta" DataFrame Extension
from pandas_ta.core import AnalysisIndicators

# Empty DataFrame Alias. Example: df = ta.df  vs.  df = pd.DataFrame()
df = DataFrame()
