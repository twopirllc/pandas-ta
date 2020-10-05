# -*- coding: utf-8 -*-
from numpy import arange as npArange
from numpy import log as npLog
from numpy import sqrt as npSqrt
from pandas import DataFrame, Series, Timedelta

from ._core import verify_series
from ._time import total_time
from ._math import linear_regression
from pandas_ta.performance import drawdown, log_return, percent_return


def cagr(close: Series) -> float:
    """Compounded Annual Growth Rate"""
    close = verify_series(close)
    start, end = close.iloc[0], close.iloc[-1]
    return ((end / start) ** (1 / total_time(close))) - 1


def calmar_ratio(close: Series, method: str = "percent", years: int = 3, log: bool = False) -> float:
    """The Calmar Ratio is the percent Max Drawdown Ratio 'typically' over
    the past three years."""
    close = verify_series(close)

    n_years_ago = close.index[-1] - Timedelta(days=365.25 * years)
    close = close[close.index > n_years_ago]

    return cagr(close) / max_drawdown(close, method=method)


def downside_deviation(returns: Series, benchmark_rate: float = 0.0, log: bool = False, tf: str = "years") -> float:
    """Downside Deviation for the Sortino ratio.
    Benchmark rate is assumed to be annualized. Adjusted according for the
    number of periods per year seen in the data."""
    # For both de-annualizing the benchmark rate and annualizing result
    returns = verify_series(returns)
    days_per_year = returns.shape[0] / total_time(returns, tf)

    adjusted_benchmark_rate = ((1 + benchmark_rate) ** (1 / days_per_year)) - 1

    downside = adjusted_benchmark_rate - returns
    downside_sum_of_squares = (downside[downside > 0] ** 2).sum()
    downside_deviation = npSqrt(downside_sum_of_squares / (returns.shape[0] - 1))
    return downside_deviation * npSqrt(days_per_year)


def jensens_alpha(returns:Series, benchmark_returns:Series) -> float:
    """Jensen's 'Alpha' of a series and a benchmark."""
    returns = verify_series(returns)
    benchmark_returns = verify_series(benchmark_returns)

    benchmark_returns.interpolate(inplace=True)
    return linear_regression(benchmark_returns, returns)["a"]


def log_max_drawdown(close:Series):
    """Log Max Drawdown of a series."""
    close = verify_series(close)
    log_return = npLog(close.iloc[-1]) - npLog(close.iloc[0])
    return log_return - max_drawdown(close, method="log")


def max_drawdown(close: Series, method:str = None, all:bool = False) -> float:
    """Maximum Drawdown from close. Defaults to 'dollar'. """
    close = verify_series(close)
    max_dd = drawdown(close).max()

    max_dd_ = {
        "dollar": max_dd.iloc[0],
        "percent": max_dd.iloc[1],
        "log": max_dd.iloc[2]
    }
    if all: return max_dd_

    if isinstance(method, str) and method in max_dd_.keys():
        return max_dd_[method]
    return max_dd_["dollar"]


def pure_profit_score(close:Series) -> float:
    """Pure Profit Score of a series."""
    from sklearn.linear_model import LinearRegression
    close = verify_series(close)
    close_index = Series(0, index=close.reset_index().index)

    r = linear_regression(close_index, close)["r"]
    return r * cagr(close)


def sharpe_ratio(close:Series, benchmark_rate:float = 0.0, log:bool = False) -> float:
    """Sharpe Ratio of a series."""
    close = verify_series(close)
    returns = percent_return(close=close) if not log else log_return(close=close)

    result  = cagr(close) - benchmark_rate
    result /= volatility(close, returns, log=log)
    return result


def sortino_ratio(close:Series, benchmark_rate:float = 0.0, log:bool = False) -> float:
    """Sortino Ratio of a series."""
    close = verify_series(close)
    returns = percent_return(close=close) if not log else log_return(close=close)

    result  = cagr(close) - benchmark_rate
    result /= downside_deviation(returns)
    return result


def volatility(close: Series, tf:str = "years", returns:bool = False, log: bool = False, **kwargs) -> float:
    """Volatility of a series. Default: 'years'"""
    close = verify_series(close)
    
    if not returns:
        returns = percent_return(close=close) if not log else log_return(close=close)

    factor = returns.shape[0] / total_time(returns, tf)
    if kwargs.pop("nearest_day", False) and tf.lower() == "years":
        factor = int(factor + 1)

    return returns.std() * npSqrt(factor)