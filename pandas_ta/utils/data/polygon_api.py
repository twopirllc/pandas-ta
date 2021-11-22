from pandas import DataFrame
from pandas_ta import Imports, RATE, version
import datetime
import polygon
import pandas as pd
from typing import Union


def polygon_api(ticker: str, **kwargs):
    print(f"[!] kwargs: {kwargs}")
    verbose = kwargs.pop("verbose", True)
    kind = kwargs.pop("kind", "history")
    kind = kind.lower()
    show = kwargs.pop("show", None)
    df = DataFrame()
    api_key = kwargs.pop('api_key', None)

    if api_key is None:
        raise ValueError('Please make sure you pass your polygon api key through kwarg api_key')

    ticker = ticker.upper() if ticker is not None and isinstance(ticker, str) else None

    if Imports["polygon"] and ticker is not None:

        start_date = kwargs.pop('start_date', (datetime.date.today() - datetime.timedelta(days=525)))
        end_date = kwargs.pop('end_date', datetime.date.today())
        limit = kwargs.pop('limit', 50000)
        multiplier = kwargs.pop('multiplier', 1)
        timespan = kwargs.pop('timespan', 'day')

        print(f'{start_date} || {end_date} || {limit} || {multiplier} || {timespan}')

        _all, div = ["all"], "=" * 53  # Max div width is 80

        if kind in _all + ["history", "h"]:
            if verbose:
                print("\n====  Chart History       " + div + f"\n[*] Pandas TA v{version} & alphaVantage-api")
                print(f"[+] Downloading {ticker}[from {start_date} to {end_date}] from polygon ("
                      f"https://www.polygon.io/)")

            with polygon.StocksClient(api_key) as polygon_client:
                resp = polygon_client.get_aggregate_bars(ticker, start_date, end_date, limit=limit,
                                                         multiplier=multiplier, timespan=timespan)

            if 'results' in resp:
                df = pd.DataFrame.from_dict(resp['results'])
                if len(df) > 0:
                    index = 't'
                    df = df.set_index(pd.DatetimeIndex(unix_convert(df[index])))
                    df = df[['v', 'o', 'c', 'h', 'l', 't']]
                    df.columns = ['Volume', 'Open', 'Close', 'High', 'Low', 'Date']

                df.name = ticker
            else:
                return None

            if show is not None and isinstance(show, int) and show > 0:
                print(f"\n{df.name}\n{df.tail(show)}\n")

            return df

    return df


def unix_convert(ts: Union[int, pd.Series]) -> Union[datetime.datetime, str]:
    """
    Converts timestamps from polygon to readable datetime strings.

    :param ts: The timestamp(s). An integer posix timestamp or a pd.Series of timestamps
    :return: The converted datetime string
    """
    return pd.to_datetime(ts, unit='ms')
