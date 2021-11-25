from pandas import DataFrame
from pandas_ta import Imports, RATE, version
import datetime
import polygon
import pandas as pd
from typing import Union
import logging

LOGGER = logging.getLogger(__name__)


def polygon_api(ticker: str, **kwargs):
    r"""
    polygon_api - polygon.io API helper function.

    It returns OCHLV data from polygon (requires a valid subscription of course). To install the
    `polygon library <https://github.com/pssolanki111/polygon>`__ , use
    ``pip install polygon``.
    You can customize the range of data using kwargs ``from_date``, ``to_date````timespan`` and ``multiplier``. For a
    description of these arguments, see
    `Here <https://polygon.readthedocs.io/en/latest/Stocks.html#get-aggregate-bars-candles>`__

    To view additional information about the ticker symbols, you can use the **kwarg** ``kind``, defaulting to
    ``None`` which doesn't pull/display any additional info.

    **The function will always return the OCHLV dataframe no matter what additional info you ask it to pull.** The
    additional information is used for display only (yet?)

    Other options for kwarg ``kind`` are as described (in format: ``value_to_supply: description of that info type``):

    * ``all``: Everything below is displayed
    * ``company``: Company information
    * ````: pass

    :param ticker: The ticker symbols of the stock.
    :param \**kwargs:
        Described Below

    :Keyword Arguments:
        * ``verbose`` - Prints Company Information "info" and a Chart History
                        header to the screen. Default: False
        * ``show`` - How many last rows of Chart History to show. Default: None
        * ``api_key`` - REQUIRED. Your polygon API key. Visit your dashboard to get this key.
        * ``kind`` - options described above. Defaults to None
        * ``start_date`` - start date of time range to get data for. Defaults to roughly a year back. Can be supplied
                           as a ``datetime`` or ``date`` object or string ``YYYY-MM-DD``
        * ``to_date`` - end date of time range to get data for. Defaults to up to most recent data available. Can be
                        supplied as a ``datetime`` or ``date`` object or string ``YYYY-MM-DD``
        * ``limit`` - max number of base candles to aggregate from. Defaults to 50000 (also the maximum value).
        * ``timespan`` - Type of candles' granularity. Defaults to ``day`` which returns day candles.
        *  ``multiplier`` - multiplier of granularity. defaults to 1. so defaults candles are of `1Day` granularity.
    """
    LOGGER.info(f"[!] kwargs: {kwargs}")
    verbose = kwargs.pop("verbose", True)
    kind = kwargs.pop("kind", "nothing").lower()
    show = kwargs.pop("show", None)
    df = DataFrame()
    api_key = kwargs.pop('api_key', None)

    if api_key is None:
        raise ValueError('Please make sure you pass your polygon api key through kwarg api_key')
    if not Imports['polygon']:
        raise ValueError('Please install package polygon to use this function (pip install polygon)')

    if ticker is not None and isinstance(ticker, str):
        ticker = ticker.upper()
    else:
        raise ValueError('Ticker symbol name must be a valid name string. Eg: \'AMD\'')

    start_date = kwargs.pop('start_date', (datetime.date.today() - datetime.timedelta(days=525)))
    end_date = kwargs.pop('end_date', datetime.date.today())
    limit = kwargs.pop('limit', 50000)
    multiplier = kwargs.pop('multiplier', 1)
    timespan = kwargs.pop('timespan', 'day')

    LOGGER.info(f'start date: {start_date} || end date: {end_date} || limit: {limit} || '
                f'multiplier: {multiplier} || timespan: {timespan}')

    _all, div = ["all"], "=" * 53  # Max div width is 80

    if verbose:
        print("\n====  Chart History       " + div + f"\n[*] Pandas TA v{version} & polygon-api")
        print(f"[+] Downloading {ticker}[from {start_date} to {end_date}] from polygon ("
              f"https://www.polygon.io/)")

    with polygon.StocksClient(api_key) as polygon_client:
        resp = polygon_client.get_aggregate_bars(ticker, start_date, end_date, limit=limit,
                                                 multiplier=multiplier, timespan=timespan)

    if 'results' in resp.keys():
        df = pd.DataFrame.from_dict(resp['results'])
        if len(df) > 0:
            index = 't'
            df = df.set_index(pd.DatetimeIndex(unix_convert(df[index])))
            df = df[['v', 'o', 'c', 'h', 'l', 't']]
            df.columns = ['Volume', 'Open', 'Close', 'High', 'Low', 'Date']

        df.name = ticker
    else:
        return df  # no data received. empty dataframe returned

    if show is not None and isinstance(show, int) and show > 0:
        print(f"\n{df.name}\n{df.tail(show)}\n")

    if kind in ['nothing', None]:  # no additional data requested
        return df

    return df


def unix_convert(ts: Union[int, pd.Series]) -> Union[datetime.datetime, str]:
    """
    Converts timestamps from polygon to readable datetime strings.

    :param ts: The timestamp(s). An integer posix timestamp or a pd.Series of timestamps
    :return: The converted datetime string
    """
    return pd.to_datetime(ts, unit='ms')
