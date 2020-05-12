import os
from pandas import read_csv

VERBOSE = True

ALERT = f"[!]"
INFO = f"[i]"

CORRELATION = 'corr'  #'sem'
CORRELATION_THRESHOLD = 0.99  # Less than 0.99 is undesirable

sample_data = read_csv(
        f"data/SPY_D.csv",
        index_col=0,
        parse_dates=True,
        infer_datetime_format=False,
        keep_date_col=True
    )

def error_analysis(df, kind, msg, icon=INFO, newline=True):
    if VERBOSE:
        s = f" {icon} {df.name}['{kind}']: {msg}"
        if newline: s = f"\n{s}"
        print(s)