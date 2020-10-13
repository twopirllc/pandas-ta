import os
from pandas import DatetimeIndex, read_csv

VERBOSE = True

ALERT = f"[!]"
INFO = f"[i]"

CORRELATION = "corr"  # "sem"
CORRELATION_THRESHOLD = 0.99  # Less than 0.99 is undesirable

sample_data = read_csv(
    f"data/SPY_D.csv",
    index_col=0,
    parse_dates=True,
    infer_datetime_format=True,
    keep_date_col=True,
)
sample_data.set_index(DatetimeIndex(sample_data["date"]), inplace=True, drop=True)
sample_data.drop("date", axis=1, inplace=True)


def error_analysis(df, kind, msg, icon=INFO, newline=True):
    if VERBOSE:
        s = f"{icon} {df.name}['{kind}']: {msg}"
        if newline:
            s = f"\n{s}"
        print(s)
