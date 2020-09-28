# -*- coding: utf-8 -*-
from datetime import datetime
from time import perf_counter

from pandas_ta import EXCHANGE_TZ



def final_time(stime):
    time_diff = perf_counter() - stime
    return f"{time_diff * 1000:2.4f} ms ({time_diff:2.4f} s)"


def get_time(exchange: str = "NYSE", to_string:bool = False) -> (None, str):
    tz = EXCHANGE_TZ["NYSE"] # Default is NYSE (Eastern Time Zone)
    if isinstance(exchange, str):
        exchange = exchange.upper()
        tz = EXCHANGE_TZ[exchange]

    day_of_year = datetime.utcnow().timetuple().tm_yday
    today = datetime.utcnow()
    s  = f"Today: {today}, "
    s += f"Day {day_of_year}/365 ({100 * round(day_of_year/365, 2)}%), "
    s += f"{exchange} Time: {(today.timetuple().tm_hour + tz) % 12}:{today.timetuple().tm_min}:{today.timetuple().tm_sec}"
    return s if to_string else print(s)
