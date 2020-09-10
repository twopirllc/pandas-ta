name = "pandas_ta"
"""
.. moduleauthor:: Kevin Johnson
"""
from pkg_resources import get_distribution, DistributionNotFound
import os.path

try:
    _dist = get_distribution("pandas_ta")
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, "pandas_ta")):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = "Please install this project with setup.py"
else:
    __version__ = _dist.version

# Not ideal and not dynamic but it works.
# Will find a dynamic solution later.
Category = {
    # Candles
    "candles": ["cdl_doji", "cdl_inside", "ha"],

    # Momentum
    "momentum": ["ao", "apo", "bias", "bop", "brar", "cci", "cg", "cmo", "coppock", "er", "eri", "fisher", "inertia", "kdj", "kst", "macd", "mom", "pgo", "ppo", "psl", "pvo", "roc", "rsi", "rvgi", "slope", "smi", "squeeze", "stoch", "stochrsi", "trix", "tsi", "uo", "willr"],

    # Overlap
    "overlap": ["dema", "ema", "fwma", "hilo", "hl2", "hlc3", "hma", "ichimoku", "kama", "linreg", "midpoint", "midprice", "ohlc4", "pwma", "rma", "sinwma", "sma", "supertrend", "swma", "t3", "tema", "trima", "vwap", "vwma", "wcp", "wma", "zlma"],

    # Performance
    "performance": ["log_return", "percent_return", "trend_return"],

    # Statistics
    "statistics": ["entropy", "kurtosis", "mad", "median", "quantile", "skew", "stdev", "variance", "zscore"],

    # Trend
    "trend": ["adx", "amat", "aroon", "chop", "cksp", "decay", "decreasing", "dpo", "increasing", "long_run", "psar", "qstick", "short_run", "ttm_trend", "vortex"],

    # Volatility
    "volatility": ["aberration", "accbands", "atr", "bbands", "donchian", "kc", "massi", "natr", "pdist", "rvi", "true_range", "ui"],

    # Volume, "vp" or "Volume Profile" is unique
    "volume": ["ad", "adosc", "aobv", "cmf", "efi", "eom", "mfi", "nvi", "obv", "pvi", "pvol", "pvt"],
}

from pandas_ta.core import *