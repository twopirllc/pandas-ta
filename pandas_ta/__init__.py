name = "pandas_ta"
"""
.. moduleauthor:: Kevin Johnson
"""
from pkg_resources import get_distribution, DistributionNotFound
import os.path

try:
    _dist = get_distribution('pandas_ta')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'pandas_ta')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version

# Momentum
from .momentum.ao import ao
from .momentum.apo import apo
from .momentum.bop import bop
from .momentum.cci import cci
from .momentum.cg import cg
from .momentum.cmo import cmo
from .momentum.coppock import coppock
from .momentum.fisher import fisher
from .momentum.kst import kst
from .momentum.macd import macd
from .momentum.mom import mom
from .momentum.ppo import ppo
from .momentum.roc import roc
from .momentum.rsi import rsi
from .momentum.slope import slope
from .momentum.stoch import stoch
from .momentum.trix import trix
from .momentum.tsi import tsi
from .momentum.uo import uo
from .momentum.willr import willr

# Overlap
from .overlap.dema import dema
from .overlap.ema import ema
from .overlap.fwma import fwma
from .overlap.hl2 import hl2
from .overlap.hlc3 import hlc3
from .overlap.hma import hma
from .overlap.ichimoku import ichimoku
from .overlap.linreg import linreg
from .overlap.midpoint import midpoint
from .overlap.midprice import midprice
from .overlap.ohlc4 import ohlc4
from .overlap.pwma import pwma
from .overlap.rma import rma
from .overlap.sma import sma
from .overlap.swma import swma
from .overlap.t3 import t3
from .overlap.tema import tema
from .overlap.trima import trima
from .overlap.vwap import vwap
from .overlap.vwma import vwma
from .overlap.wma import wma
from .overlap.zlma import zlma

# Performance
from .performance.log_return import log_return
from .performance.percent_return import percent_return
from .performance.trend_return import trend_return

# Statistics
from .statistics.kurtosis import kurtosis
from .statistics.mad import mad
from .statistics.median import median
from .statistics.quantile import quantile
from .statistics.skew import skew
from .statistics.stdev import stdev
from .statistics.variance import variance
from .statistics.zscore import zscore

# Trend
from .trend.adx import adx
from .trend.amat import amat
from .trend.aroon import aroon
from .trend.decreasing import decreasing
from .trend.dpo import dpo
from .trend.increasing import increasing
from .trend.linear_decay import linear_decay
from .trend.long_run import long_run
from .trend.qstick import qstick
from .trend.short_run import short_run
from .trend.vortex import vortex

# Volatility
from .volatility.accbands import accbands
from .volatility.atr import atr
from .volatility.bbands import bbands
from .volatility.donchian import donchian
from .volatility.kc import kc
from .volatility.massi import massi
from .volatility.natr import natr
from .volatility.true_range import true_range

# Volume
from .volume.ad import ad
from .volume.adosc import adosc
from .volume.aobv import aobv
from .volume.cmf import cmf
from .volume.efi import efi
from .volume.eom import eom
from .volume.mfi import mfi
from .volume.nvi import nvi
from .volume.obv import obv
from .volume.pvi import pvi
from .volume.pvol import pvol
from .volume.pvt import pvt
from .volume.vp import vp

# DataFrame Extension
from .core import *

