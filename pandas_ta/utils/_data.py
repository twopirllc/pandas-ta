# -*- coding: utf-8 -*-
# from alphaVantageAPI import alphavantage
from pandas import DataFrame
from pandas_ta import Imports, RATE, version
from ._core import _camelCase2Title
from ._time import ytd_df


def av(ticker: str, **kwargs):
    print(f"[!] kwargs: {kwargs}")
    verbose = kwargs.pop("verbose", False)
    kind = kwargs.pop("kind", "history")
    kind = kind.lower()
    interval = kwargs.pop("interval", "D")
    show = kwargs.pop("show", None)
    # last = kwargs.pop("last", RATE["TRADING_DAYS_PER_YEAR"])

    ticker = ticker.upper() if ticker is not None and isinstance(ticker, str) else None

    if Imports["alphaVantage-api"] and ticker is not None:
        import alphaVantageAPI as AV
        AVC = {"api_key": "YOUR API KEY", "clean": True, "export": False, "output_size": "full", "premium": False}
        _config = kwargs.pop("av_kwargs", AVC)
        av = AV.AlphaVantage(**_config)

        period = kwargs.pop("period", av.output_size)

        _all, div = ["all"], "=" * 53 # Max div width is 80

        if kind in _all or verbose: pass

        if kind in _all + ["history", "h"]:
            if verbose:
                print("\n====  Chart History       " + div + f"\n[*] Pandas TA v{version} & alphaVantage-api")
                print(f"[+] Downloading {ticker}[{interval}:{period}] from {av.API_NAME} (https://www.alphavantage.co/)")
            df = av.data(ticker, interval)
            df.name = ticker
            if show is not None and isinstance(show, int) and show > 0:
                print(f"\n{df.name}\n{df.tail(show)}\n")
            return df

    return DataFrame()


def yf(ticker: str, **kwargs):
    """yf - yfinance wrapper

    It retrieves market data (ohlcv) from Yahoo Finance using yfinance.
    To install yfinance. (pip install yfinance) This method can also pull
    additional data using the 'kind' kwarg. By default kind=None and retrieves
    Historical Chart Data.

    Other options of 'kind' include:
    * All: "all"
        - Prints everything below but only returns Chart History to Pandas TA
    * Company Information: "info"
    * Institutional Holders: "institutional_holders" or "ih"
    * Major Holders: "major_holders" or "mh"
    * Mutual Fund Holders: "mutualfund_holders" or "mfh"
    * Recommendations (YTD): "recommendations" or "rec"
    * Earnings Calendar: "calendar" or "cal"
    * Earnings: "earnings" or "earn"
    * Sustainability/ESG Scores: "sustainability", "sus" or "esg"
    * Financials: "financials" or "fin"
        - Returns in order: Income Statement, Balance Sheet and Cash Flow
    * Option Chain: "option_chain" or "oc"
        - Uses the nearest expiration date by default
        - Change the expiration date using kwarg "exp"
        - Show ITM options, set kwarg "itm" to True. Or OTM options, set
        kwarg "itm" to False.
    * Chart History:
        - The only data returned to Pandas TA.

    Args:
        ticker (str): Any string for a ticker you would use with yfinance.
            Default: "SPY"
    Kwargs:
        desc (bool): Will print Company Description when printing Company
            Information. Default: False
        exp (str): Used to print other Option Chains for the given Expiration
            Date. Default: Nearest Expiration Date for the Option Chains
        interval (str): A yfinance argument. Default: "1d"
        itm (bool): When printing Option Chains, shows ITM Options when True.
            When False, it shows OTM Options: Default: None
        kind (str): Options see above. Default: None
        period (str): A yfinance argument. Default: "max"
        proxy (dict): Proxy for yfinance to use. Default: {}
        show (int > 0): How many last rows of Chart History to show.
            Default: None
        snd (int): How many recent Splits and Dividends to show in Company
            Information. Default: 5
        verbose (bool): Prints Company Information "info" and a Chart History
            header to the screen. Default: False

    Returns:
        Exits if the DataFrame is empty or None
        Otherwise it returns a DataFrame of the Chart History
    """
    verbose = kwargs.pop("verbose", False)
    if ticker is not None and isinstance(ticker, str) and len(ticker):
        ticker = ticker.upper()
    else:
        ticker = "SPY"

    kind = kwargs.pop("kind", None)
    if kind is not None and isinstance(kind, str) and len(kind):
        kind = kind.lower()
    else:
        print(f'[?] Available "kind" values: "" ')
        return

    period = kwargs.pop("period", "max")
    interval = kwargs.pop("interval", "1d")
    proxy = kwargs.pop("proxy", {})
    show = kwargs.pop("show", None)

    if not Imports["yfinance"]:
        print(f"[X] Please install yfinance to use this method. (pip install yfinance)")
        return
    if Imports["yfinance"] and ticker is not None:
        import yfinance as yfra
        yfra.pdr_override()

        # Ticker Info
        yfd = yfra.Ticker(ticker)

        try:
            ticker_info = yfd.info
        except KeyError as ke:
            print(f"[X] Ticker '{ticker}' not found.")
            return

        infodf = DataFrame.from_dict(ticker_info, orient="index")
        infodf.name, infodf.columns = ticker, [ticker]

        # Dividends and Splits
        dividends, splits = yfd.splits, yfd.dividends

        _all, div = ["all"], "=" * 53 # Max div width is 80
        if kind in _all + ["info"] or verbose:
            description = kwargs.pop("desc", False)
            snd_length = kwargs.pop("snd", 5)

            print("\n====  Company Information  " + div)
            print(f"{ticker_info['longName']} ({ticker_info['shortName']})")
            if description:
                print(f"{ticker_info['longBusinessSummary']}\n")
            if "address1" in ticker_info and len(ticker_info["address1"]):
                if "address2" in ticker_info and len(ticker_info["address2"]):
                    print(f"{ticker_info['address1']} {ticker_info['address2']}")
                else:
                    print(f"{ticker_info['address1']}")
                if "city" in ticker_info and len(ticker_info["city"]):
                    print(f"{ticker_info['city']}, {ticker_info['state']} {ticker_info['zip']}, {ticker_info['country']}")
                else:
                    print(f"{ticker_info['state']} {ticker_info['zip']}, {ticker_info['country']}")
                print(f"Phone (Fax): {ticker_info['phone']} ({ticker_info['fax'] if 'fax' in ticker_info else 'N/A'})")
            if "website" in ticker_info and "fullTimeEmployees" in ticker_info:
                print(f"Website: {ticker_info['website']}    FT Employees: {ticker_info['fullTimeEmployees']:,}")
            if "sector" in ticker_info and len(ticker_info["sector"]):
                print(f"Sector | Industry: {ticker_info['sector']} | {ticker_info['industry']}")

            print("\n====  Market Information   " + div)
            _category = f" | {ticker_info['category']}" if "category" in ticker_info and ticker_info["category"] is not None else ""
            print(f"Market | Exchange | Symbol{' | Category' if 'category' in ticker_info and ticker_info['category'] is not None else ''}: {ticker_info['market'].split('_')[0].upper()} | {ticker_info['exchange']} | {ticker_info['symbol']}{_category}")

            if "marketCap" in ticker_info and ticker_info["marketCap"] is not None:
                print(f"Market Cap.: {ticker_info['marketCap']:,} ({ticker_info['marketCap']/1000000:,.2f} MM)")

            print(f"\nShares Outstanding | Float: {ticker_info['sharesOutstanding']:,} | {ticker_info['floatShares']:,}")  if "sharesOutstanding" in ticker_info else None
            if "sharesShort" in ticker_info and "shortRatio" in ticker_info and ticker_info["sharesShort"] is not None and ticker_info["shortRatio"] is not None:
                print(f"Shares Short (Ratio): {ticker_info['sharesShort']:,} ({ticker_info['shortRatio']})")
            if "52WeekChange" in ticker_info and ticker_info['52WeekChange'] is not None:
                print(f"\n52Wk % Change:           {100 * ticker_info['52WeekChange']:.4f}%")
                if "SandP52WeekChange" in ticker_info and ticker_info['SandP52WeekChange'] is not None:
                    print(f"52Wk % Change vs S&P500: {100 *(ticker_info['52WeekChange'] - ticker_info['SandP52WeekChange']):.4f}%")
            if "fiftyTwoWeekHigh" in ticker_info and "fiftyTwoWeekLow" in ticker_info and "previousClose" in ticker_info: # or 'regularMarketPrice'
                print(f"52Wk Range (% from 52Wk Low): {ticker_info['fiftyTwoWeekLow']} - {ticker_info['fiftyTwoWeekHigh']} : {ticker_info['fiftyTwoWeekHigh'] - ticker_info['fiftyTwoWeekLow']:.4f} ({100 * (ticker_info['previousClose'] / ticker_info['fiftyTwoWeekLow'] - 1):.4f}%)")
            if "beta" in ticker_info and ticker_info['beta'] is not None:
                print(f"Beta (3Yr): {ticker_info['beta']} ({ticker_info['beta3Year']})")

            if not dividends.empty:
                dividends.name = "Value"
                total_dividends = dividends.size
                dividendsdf = DataFrame(dividends.tail(snd_length)[::-1]).T
                print(f"\nDividends (Last {snd_length} of {total_dividends}):\n{dividendsdf}")

            if not splits.empty:
                splits.name = "Ratio"
                total_splits = splits.size
                splitsdf = DataFrame(splits.tail(snd_length)[::-1]).T
                print(f"\nStock Splits (Last {snd_length} of {total_splits}):\n{splitsdf}")

            print("\n====  Price Information    " + div)
            print(f"OHLC: {ticker_info['open']:.4f}, {ticker_info['dayHigh']:.4f}, {ticker_info['dayLow']:.4f}, {ticker_info['previousClose']:.4f} ({100 * ((ticker_info['previousClose'] / ticker_info['open'] - 1)):.4f}%)")
            print(f"Volume: {ticker_info['volume']:,}        AvgVol (10Day): {ticker_info['averageVolume']:,} ({ticker_info['averageDailyVolume10Day']:,})")
            print(f"Bid | Ask | Spread:  {ticker_info['bid']} x {ticker_info['bidSize']} | {ticker_info['ask']} x {ticker_info['askSize']} | {ticker_info['ask'] - ticker_info['bid']:.4f}")

        if kind in _all + ["institutional_holders", "ih"]:
            ihdf = yfd.institutional_holders
            if ihdf is not None and "Date Reported" in ihdf.columns:
                ihdf.set_index("Date Reported", inplace=True)
                ihdf["Shares"] = ihdf.apply(lambda x: f"{x['Shares']:,}", axis=1)
                ihdf["Value"] = ihdf.apply(lambda x: f"{x['Value']:,}", axis=1)
                print("\n====  Instl Holders       " + div + f"\n{ihdf}")

        if kind in _all + ["major_holders", "mh"]:
            mhdf = yfd.major_holders
            if mhdf is not None and "Major Holders" in mhdf.columns:
                mhdf.columns = ["Percentage", "Major Holders"]
                mhdf.set_index("Major Holders", inplace=True)
                mhdf["Shares"] = mhdf.apply(lambda x: f"{x['Shares']:,}", axis=1)
                mhdf["Value"] = mhdf.apply(lambda x: f"{x['Value']:,}", axis=1)
                print("\n====  Major Holders       " + div + f"\n{mhdf}")

        if kind in _all + ["mutualfund_holders", "mfh"]:
            mfhdf = yfd.get_mutualfund_holders()
            if mfhdf is not None and "Holder" in mfhdf.columns:
                mfhdf.set_index("Date Reported", inplace=True)
                mfhdf["Shares"] = mfhdf.apply(lambda x: f"{x['Shares']:,}", axis=1)
                mfhdf["Value"] = mfhdf.apply(lambda x: f"{x['Value']:,}", axis=1)
                print("\n====  Mutual Fund Holders" + div + f"\n{mfhdf}")

        if kind in _all + ["recommendations", "rec"]:
            recdf = yfd.recommendations
            if recdf is not None:
                recdf = ytd_df(recdf)
                # recdf_grade = recdf["To Grade"].value_counts().T
                # recdf_grade.name = "Grades"
                print("\n====  Recommendations(YTD)" + div + f"\n{recdf}")

        if kind in _all + ["calendar", "cal"]:
            caldf = yfd.calendar
            if caldf is not None and "Earnings Date" in caldf.columns:
                    caldf.set_index("Earnings Date", inplace=True)
                    print("\n====  Earnings Calendar    " + div + f"\n{caldf}")

        if kind in _all + ["earnings", "earn"]:
            earndf = yfd.earnings
            if not earndf.empty:
                earndf["Revenue"] = earndf.apply(lambda x: f"{x['Revenue']:,}", axis=1)
                earndf["Earnings"] = earndf.apply(lambda x: f"{x['Earnings']:,}", axis=1)
                print("\n====  Earnings          " + div + f"\n{earndf}")

        if kind in _all + ["sustainability", "sus", "esg"]:
            susdf = yfd.sustainability
            if susdf is not None:
                susdf.replace({None: False}, inplace=True)
                susdf.columns = ["Score"]
                susdf.drop(susdf[susdf["Score"] == False].index, inplace=True)
                susdf.rename(index=_camelCase2Title, errors="ignore", inplace=True)
                susdf.index.name = "Source"
                print("\n====  Sustainability/ESG   " + div + f"\n{susdf}")

        if kind in _all + ["financials", "fin"]:
            print("\n====  Company Financials  " + div)
            icdf = yfd.financials
            bsdf = yfd.balance_sheet
            cfdf = yfd.cashflow
            if icdf.empty or bsdf.empty or cfdf.empty:
                if yfra.__version__ == "0.1.54":
                    print(f"[!] Ignore if aleady patched. Some tickers do not have financials.")
                    print(f"[!] Otherwise to enable Company Financials, see yfinance Issue #517 patch.")
                    print(f"[!] https://github.com/ranaroussi/yfinance/pull/517/files")
            else:
                if not icdf.empty: print(f"Income Statement:\n{icdf}\n")
                if not bsdf.empty: print(f"Balance Sheet:\n{bsdf}\n")
                if not cfdf.empty: print(f"Cash Flow:\n{cfdf}\n")

        if kind in _all + ["option_chain", "oc"]:
            try:
                yfd_options = yfd.options
            except IndexError as ie:
                yfd_options = None

            if yfd_options is not None:
                opt_expirations = list(yfd_options)
                itm = kwargs.pop("itm", None)
                opt_date = kwargs.pop("exp", opt_expirations[0])
                opt_expirations_str = f"{ticker} Option Expirations:\n\t{', '.join(opt_expirations)}\n"

                print("\n====  Option Chains       " + div)
                print(opt_expirations_str)
                if opt_date not in opt_expirations:
                    print(f"[X] No Options for {ticker_info['quoteType']} {ticker_info['symbol']}")
                else:
                    option_columns = ["Contract", "Last Trade", "Strike", "Price", "Bid", "Ask", "Change", "Percent Change", "Volume", "OI", "IV", "ITM", "Size", "Currency"]
                    cp_chain = yfd.option_chain(proxy=proxy)
                    calls, puts = cp_chain.calls, cp_chain.puts
                    calls.columns = puts.columns = option_columns
                    calls.set_index("Contract", inplace=True)
                    puts.set_index("Contract", inplace=True)

                    calls.name = f"{ticker} Calls for {opt_date}"
                    puts.name = f"{ticker} Puts for {opt_date}"

                    if itm is not None:
                        calls.name, puts.name = f"{calls.name} ITM: {itm}", f"{puts.name}  ITM: {itm}"
                        print(f"{calls.name}\n{calls[calls['ITM'] == itm]}\n\n{puts.name}\n{puts[puts['ITM'] == itm]}")
                    else:
                        print(f"{calls.name}\n{calls}\n\n{puts.name}\n{puts}")

        df = yfd.history(period=period, interval=interval, proxy=proxy, **kwargs)
        df.name = ticker
        if verbose:
            print("\n====  Chart History       " + div + f"\n[*] Pandas TA v{version} & yfinance v{yfra.__version__}")
            print(f"[+] Downloading {ticker}[{interval}:{period}] from Yahoo Finance")
        if show is not None and isinstance(show, int) and show > 0:
            print(f"\n{df.name}\n{df.tail(show)}\n")
        if verbose: print("=" * 80 + "\n")
        else: print()
        return df

    else:
        return DataFrame()
