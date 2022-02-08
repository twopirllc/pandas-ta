import datetime

from pandas import DataFrame, DatetimeIndex, merge
from pandas_ta.maps import Imports, RATE, version
from pandas_ta.utils import unix_convert


def polygon_api(ticker: str, **kwargs) -> DataFrame:
    r"""
    polygon_api - polygon.io API helper function.

    It returns OCHLV data from polygon (A valid subscription is required).
    To install the `polygon library <https://github.com/pssolanki111/polygon>`__ ,
    use ``pip install polygon``.
    You can customize the range of data using kwargs ``from_date``,
    ``to_date``, ``timespan`` and ``multiplier``. For a description of
    these arguments, see
    `Here <https://polygon.readthedocs.io/en/latest/Stocks.html#get-aggregate-bars-candles>`__

    To view additional information about the ticker symbols, you can use
    the **kwarg** ``kind``, defaulting to ``None`` which doesn't
    pull/display any additional info.

    **The function will always return the OCHLV dataframe no matter what
    additional info you ask it to pull.** The additional information is
    used for display only (yet?)

    Other options for kwarg ``kind`` are as described
    in format: ``value_to_supply: description of that info type``):

    * ``all`` OR ``info``: Everything below is displayed
    * ``option_chains`` OR ``oc``: Option chains information

    :param ticker: The ticker symbols of the stock.
    :param \**kwargs:
        Described Below

    :Keyword Arguments:
        * ``api_key`` - REQUIRED. Your polygon API key.
            Visit your dashboard to get this key.
        * ``show`` - How many last rows of Chart History to show.
            Default: None
        * ``kind`` - Options described above. Default: None
        * ``desc`` - Company description. Default: False
        * ``start_date`` - Start Date for the time range.
            Defaults to roughly a year back. Can be supplied as a
            ``datetime`` or ``date`` object or string ``YYYY-MM-DD``
        * ``to_date`` - End date for the time range.
            Defaults to up to most recent data available. Can be supplied as
            a ``datetime`` or ``date`` object or string ``YYYY-MM-DD``
        * ``limit`` - Max number of candles to aggregate.
            Default: 50000 (also the maximum value).
        * ``timespan`` - Type of candles' granularity.
            Default: ``day`` (Daily Candles)
        * ``multiplier`` - Multiplier of granularity. Default: 1.
            Defaults candles are of `1Day` granularity.
        * ``contract_type`` - Can be changed to ``call`` OR ``put``.
            Only applicable when displaying option chains data.
            Default: both
        * ``contract_limit`` - Max number of Contracts to display from
            Option Chains. Default: 10
        * ``verbose`` - Prints Company Information "info" and a Chart History
                        header to the screen. Default: False
    """
    verbose = kwargs.pop("verbose", False)
    kind = kwargs.pop("kind", "nothing").lower()
    api_key = kwargs.pop("api_key", None)
    show = kwargs.pop("show", None)
    # desc = kwargs.pop("desc", False)

    if api_key is None:
        raise ValueError(
            "Please make sure you pass your polygon api key through kwarg api_key")
    if not Imports["polygon"]:
        raise ValueError(
            "Please install package polygon to use this function (pip install polygon)")

    if ticker is not None and isinstance(ticker, str):
        ticker = ticker.upper()
    else:
        raise ValueError(
            f"Ticker symbol name must be a valid name string. Eg: \'AMD\'")

    start_date = kwargs.pop(
        "start_date", (datetime.date.today() - datetime.timedelta(days=525))
    )
    end_date = kwargs.pop("end_date", datetime.date.today())
    limit = kwargs.pop("limit", 50000)
    multiplier = kwargs.pop("multiplier", 1)
    timespan = kwargs.pop("timespan", "day")

    if not Imports["polygon"]:
        print(f"[X] Please install yfinance to use this method. (pip install yfinance)")
        return
    if Imports["polygon"] and ticker is not None:
        import polygon as polyapi

        with polyapi.StocksClient(api_key) as polygon_client:
            resp = polygon_client.get_aggregate_bars(
                ticker, start_date, end_date, limit=limit,
                multiplier=multiplier, timespan=timespan
            )

        df = DataFrame()
        if "results" in resp.keys():
            df = DataFrame.from_dict(resp["results"])
            df = df.set_index(DatetimeIndex(unix_convert(df["t"])))
            df.index.name = "DateTime"
            # reorder then rename
            df = df[["o", "h", "l", "c", "v", "vw", "n"]]
            _columns = {
                "o": "Open", "h": "High", "l": "Low", "c": "Close",
                "v": "Volume", "vw": "VWAP", "n": "Trades"
            }
            df.rename(columns=_columns, errors="ignore", inplace=True)

        if df.empty:
            print(f"[X] Could not find: {ticker} with 'get_aggregate_bars()'.")
            return
        df.name = ticker

        # ADDITIONAL DATA FLOW
        ref_client, stock_client = polyapi.ReferenceClient(
            api_key), polyapi.StocksClient(api_key)

        div = "=" * 53  # Max div width is 80
        # ALL THE INFORMATION
        if kind in ["all", "info"] or verbose:
            print("\n====  Company Information  " + div)
            details = ref_client.get_ticker_details(ticker)
            details_vx = ref_client.get_ticker_details_vx(ticker)["results"]

            has_name = "name" in details_vx and len(details_vx['name'])
            has_ticker = "ticker" in details_vx and len(details_vx['ticker'])
            if not has_ticker:
                details_vx['ticker'] = ticker
            if has_name and has_ticker:
                print(f"{details_vx['name']} [{details_vx['ticker']}]")
            else:
                print(f"{details_vx['ticker']}")

            # TODO: polygon returns a lot of data for market info across a few endpoints. I don't know which ones to
            #  include here lol. I wrote the ones i felt were important. Feel free to suggest more.
            #  Yeah. It needs some additional modifications since details and details_vx are
            #    not equal and sparse depending on asset of ticker

            # Common Information
            # print(f"{details['hq_address']}. {details['hq_country']}\nPhone: {details_vx['phone_number']}\n"
            #       f"Website: {details['url']} || Employees: {details['employees']}\nSector: {details['sector']} || "
            #       f"Industry: {details['industry']}\n\n====  Market Information {div}\n"
            #       f"Market: {details_vx['market'].upper()} || locale: {details_vx['locale'].upper()} || "
            #       f"Exchange: {details['exchange']} || Symbol: {details['symbol']}\nMarket Shares: "
            # f"{details_vx['market_cap']} || Outstanding Shares:
            # {details_vx['outstanding_shares']}\n")
            has_hq_address = "hq_address" in details and len(
                details['hq_address'])
            has_vx_address = "address" in details_vx and len(
                details_vx["address"])
            if has_hq_address:
                print(
                    f"{details['hq_address']}\n{details['hq_state']}, {details['hq_country']}")
            elif has_vx_address:
                has_vx_address1 = "address1" in details_vx['address'] and len(
                    details_vx['address']['address1'])
                has_vx_address2 = "address2" in details_vx['address'] and len(
                    details_vx['address']['address2'])
                if has_vx_address1 and has_vx_address2:
                    print(
                        f"{details_vx['address']['address1']}\n{details_vx['address']['address2']}\n{details_vx['address']['city']}, {details_vx['address']['state']} {details_vx['address']['postal_code']}")
                elif has_vx_address1:
                    print(
                        f"{details_vx['address']['address1']}\n{details_vx['address']['city']}, {details_vx['address']['state']} {details_vx['address']['postal_code']}")

            has_phone = "phone" in details and len(details['phone'])
            has_vx_phone = "phone_number" in details_vx and len(
                details_vx['phone_number'])
            if has_phone or has_vx_phone:
                _phone = details_vx['phone_number'] or details['phone']
                if len(_phone):
                    print(f"Phone: {_phone}")

            # Market Information
            has_market = "locale" in details_vx and len(details_vx["locale"])
            has_exchange = "primary_exchange" in details_vx and len(
                details_vx["primary_exchange"])
            print("\n====  Market Information   " + div)
            if has_market and has_exchange and has_ticker:
                print(
                    f"Market | Exchange | Symbol".ljust(39),
                    f"{details_vx['locale'].upper()} | {details_vx['primary_exchange']} | {details_vx['ticker']}".rjust(40))

            print()
            if "market_cap" in details_vx:
                print(
                    f"Market Cap.".ljust(39),
                    f"{details_vx['market_cap']:,} ({details_vx['market_cap']/1000000:,.2f} MM)".rjust(40))
            if "outstanding_shares" in details_vx:
                print(f"Shares Outstanding".ljust(39),
                      f"{details_vx['outstanding_shares']:,}".rjust(40))

            # Price Info
            snap_res = stock_client.get_snapshot(ticker)
            print(f"\n====  Price Information ==={div}")
            try:
                snap = snap_res["ticker"]

                # TODO: Convert to DF and print similar to YF
                print(f"\nCurrent Price: {snap['lastTrade']['p']} || Today\'s Change: ${snap_res['todaysChange']} - "
                      f"{snap_res['todaysChangePerc']}%\nBid: {snap['lastQuote']['p']} x {snap['lastQuote']['s']} || Ask: "
                      f"{snap['lastQuote']['P']} x {snap['lastQuote']['S']} || Spread: "
                      f"{round(snap['lastQuote']['P'] - snap['lastQuote']['p'], 4)}\nOpen: {snap['day']['o']} || High: "
                      f"{snap['day']['h']} || Low: {snap['day']['l']} || Close: {snap['day']['c']} || Volume: "
                      f"{snap['day']['v']} || VWA: {snap['day']['vw']}")
            except KeyError:
                print(f"* Snapshot not found for {ticker}. Can not print price information.\n"
                      f"* Note: Snapshot data is cleared at 12am EST and gets populated as data is\n"
                      f"    received from the exchanges. This can happen as early as 4am EST.\n"
                      f'* Requires a "Stocks Starter" subscription')

            # Splits and Dividends
            # divs, splits = ref_client.get_stock_dividends(ticker), ref_client.get_stock_splits(ticker)
            # # TODO: spits and dividends endpoints from polygon return a huge list. not sure if that entire list is useful
            # print(f"\nNumber of dividends: {divs['count']} || Number of splits: {splits['count']}\n")

            # TODO: financials endpoint on polygon returns a huge response. I
            # doubt if that's useful to be displayed.

        # Option Chains
        if kind in ["option_chains", "oc"]:
            _contract_type = kwargs.pop("contract_type", "all").lower()
            contract_type = None if _contract_type == "all" else _contract_type
            contract_limit = kwargs.pop("contract_limit", 10)

            call_chain = put_chain = None
            if contract_type is None:
                call_chain = ref_client.get_option_contracts(
                    ticker, limit=contract_limit,
                    contract_type="call"
                )

                put_chain = ref_client.get_option_contracts(
                    ticker, limit=contract_limit,
                    contract_type="put"
                )
            else:
                if contract_type == "call":
                    call_chain = ref_client.get_option_contracts(
                        ticker, limit=contract_limit,
                        contract_type="call"
                    )
                if contract_type == "put":
                    put_chain = ref_client.get_option_contracts(
                        ticker, limit=contract_limit,
                        contract_type="put"
                    )

            if call_chain is not None or put_chain is not None:
                print(f"\n====  Option Chains {div}")

            def _cleandf(chain: dict):
                exp_dates = [x["expiration_date"] for x in chain]
                df = DataFrame().from_records(chain)
                df = df[["ticker", "strike_price",
                         "expiration_date", "exercise_style"]]
                df.columns = ["Contract", "Strike", "Exp. Date", "Style"]
                df.set_index("Exp. Date", inplace=True)
                return exp_dates, df

            if call_chain is not None and len(call_chain["results"]):
                exp_dates, calldf = _cleandf(call_chain["results"])
                if contract_type == "call":
                    print(f"\n{ticker} Calls for {exp_dates[0]}\n{calldf}")

            if put_chain is not None and len(put_chain["results"]):
                exp_dates, putdf = _cleandf(put_chain["results"])
                if contract_type == "put":
                    print(f"\n{ticker} Puts for {exp_dates[0]}\n{putdf}")

            if contract_type is None:
                alldf = merge(
                    calldf.reset_index(), putdf.reset_index(), on="Strike"
                )
                alldf.rename(
                    columns={
                        "Contract_x": "Calls",
                        "Contract_y": "Puts",
                        "Exp. Date_x": "Exp. Date"
                    }, inplace=True
                )
                alldf.set_index("Exp. Date", inplace=True)
                alldf = alldf[["Calls", "Strike", "Puts"]]
                print(f"\n{ticker} Calls & Puts for {exp_dates[0]}\n{alldf}")
            else:
                print(f"\nNo option chains data found for {ticker}.")

        if verbose:
            _chart_history = \
                f"\n====  Chart History       " + div + \
                f"\n[*] Pandas TA v{version} & polygon API" + \
                f"\n[+] Downloading {ticker} [{start_date} : {end_date}] from Polygon (www.polygon.io/)\n{'='*80}\n"
            print(_chart_history)

        if show is not None and isinstance(show, int) and show > 0:
            print(f"\n{df.name}\n{df.tail(show)}\n")

        return df
    else:
        return DataFrame()
