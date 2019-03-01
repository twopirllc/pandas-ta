from pandas import read_csv

CORRELATION_THRESHOLD = 0.99  # Less than 0.99 is undesirable
ALERT = f"[!]"
INFO = f"[i]"
VERBOSE = True
sample_data = read_csv('data/sample.csv', index_col=0, parse_dates=True, infer_datetime_format=False, keep_date_col=True)

def error_analysis(df, kind, msg, icon=INFO):
    if VERBOSE: print(f"\n {icon} {df.name}['{kind}']: {msg}")