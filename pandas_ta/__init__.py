"""
.. moduleauthor:: Kevin Johnson
"""
name = "pandas_ta"

# Dictionaries and version
from pandas_ta.maps import EXCHANGE_TZ, RATE, Category, Imports, version
from pandas_ta.utils import *
from pandas_ta.utils import __all__ as utils_all

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
from pandas_ta.candles import __all__ as candles_all
from pandas_ta.cycles import __all__ as cycles_all
from pandas_ta.momentum import __all__ as momentum_all
from pandas_ta.overlap import __all__ as overlap_all
from pandas_ta.performance import __all__ as performance_all
from pandas_ta.statistics import __all__ as statistics_all
from pandas_ta.transform import __all__ as transform_all
from pandas_ta.trend import __all__ as trend_all
from pandas_ta.volatility import __all__ as volatility_all
from pandas_ta.volume import __all__ as volume_all

# Common Averages useful for Indicators with a mamode argument, like ta.adx()
from pandas_ta.ma import ma

# Custom External Directory Commands. See help(import_dir)
from pandas_ta.custom import create_dir, import_dir

# Enable "ta" DataFrame Extension
from pandas_ta.core import AnalysisIndicators

__all__ = [
    'name',
    'EXCHANGE_TZ',
    'RATE',
    'Category',
    'Imports',
    'version',
    'ma',
    'create_dir',
    'import_dir',
    'AnalysisIndicators',
]

__all__ += (
    utils_all
    + candles_all
    + cycles_all
    + momentum_all
    + overlap_all
    + performance_all
    + statistics_all
    + transform_all
    + trend_all
    + volatility_all
    + volume_all
)
