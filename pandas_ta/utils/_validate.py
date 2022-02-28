# -*- coding: utf-8 -*-
from functools import partial
from pandas import DataFrame, Series
from pandas.api.types import is_datetime64_any_dtype
from pandas_ta._typing import (
    Float, Int, IntFloat, List, MaybeSeriesFrame, Optional, SeriesFrame
)


def is_percent(x: IntFloat) -> bool:
    if isinstance(x, (int, float)):
        return x is not None and 0 <= x <= 100
    return False

def v_bool(var: bool, default: bool = True) -> bool:
    """Returns default=True if var is not a bool."""
    if isinstance(var, bool):
        return bool(var)
    return default

def v_dataframe(obj: MaybeSeriesFrame) -> None:
    if not isinstance(obj, (DataFrame, Series)):
        print("[X] Requires a Pandas Series or DataFrame.")

def v_float(
    var: IntFloat, default: IntFloat, ne: Optional[IntFloat] = 0.0
) -> Float:
    """Returns the default if var is not equal to the ne value."""
    is_ne, is_var = isinstance(ne, (float, int)), isinstance(var, (float, int))
    if is_ne and is_var and float(var) != float(ne):
        return float(var)
    return float(default)

def v_int(var: Int, default: Int, ne: Optional[Int] = 0) -> Int:
    """Returns the default if var is not equal to the ne value."""
    is_ne, is_var = isinstance(ne, int), isinstance(var, int)
    if is_ne and is_var and int(var) != int(ne):
        return int(var)
    return int(default)

def v_str(var: str, default: str) -> str:
    """"Returns the default value if var is not a empty str"""
    if isinstance(var, str) and len(var) > 0:
        return f"{var}"
    return f"{default}"

def v_ascending(var: bool) -> bool:
    """Returns True by default"""
    return partial(v_bool, default=True)(var=var)

def v_datetime_ordered(df: SeriesFrame) -> bool:
    if is_datetime64_any_dtype(df.index):
        np_dt_index = df.index.to_numpy()
        if np_dt_index[0] < np_dt_index[-1]:
            return True
    return False

def v_drift(var: Int) -> Int:
    """Defaults to 1"""
    return partial(v_int, default=1, ne=0)(var=var)

def v_list(var: List, default: List = []) -> List:
    """Returns [] if not a valid list"""
    if isinstance(var, list) and len(var) > 0:
        return var
    return default

def v_lowerbound(
    var: IntFloat, bound: IntFloat = 0,
    default: IntFloat = 0, strict: bool = True, complement: bool = False
) -> IntFloat:
    """Returns the default if var(iable) not greater(equal) than bound."""
    var_type = None
    if isinstance(var, float): var_type = float
    if isinstance(var, int): var_type = int

    if var_type is None:
        return default

    valid = False
    if strict:
        valid = var_type(var) > var_type(bound)
    else:
        valid = var_type(var) >= var_type(bound)

    if complement: valid = not valid

    if valid:
        return var_type(var)
    return default

def v_mamode(var: str, default: str) -> str: # Could be an alias.
    return v_str(var, default)

def v_offset(var: Int) -> Int:
    """Defaults to 0"""
    return partial(v_int, default=0, ne=0)(var=var)

def v_pos_default(
    var: IntFloat, default: IntFloat = 0, strict: bool = True, complement: bool = False
) -> IntFloat:
    return partial(v_lowerbound, bound=0)\
        (var=var, default=default, strict=strict, complement=complement)

def v_scalar(var: IntFloat, default: Optional[IntFloat] = 1) -> Float:
    """Returns the default if var is not a float."""
    if isinstance(var, (float, int)):
        return float(var)
    return float(default)

def v_series(series: Series, length: Optional[IntFloat] = 0) -> Optional[Series]:
    """Returns None if the Pandas Series does not meet the minimum length
    required for the indicator."""
    if isinstance(series, Series) and series.empty and series.size >= length:
        print("[X] Requires a Pandas Series or DataFrame.")
        return None
    return series

def v_talib(var: bool) -> bool:
    """Returns True by default"""
    return partial(v_bool, default=True)(var=var)

def v_tradingview(var: bool) -> bool:
    """Returns True by default"""
    return partial(v_bool, default=True)(var=var)

def v_upperbound(
    var: IntFloat, bound: IntFloat = 0,
    default: IntFloat = 0, strict: bool = True
) -> IntFloat:
    return partial(v_lowerbound, complement=True)\
        (var=var, bound=bound, default=default, strict=strict)
