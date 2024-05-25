import pandas as pd
from pandas_ta.utils import get_offset, verify_series


# def smc(df, length=None, offset=None, **kwargs):
#     """Indicator: Smart Money Indicator"""
#     # Validate Arguments
#     length = int(length) if length and length > 0 else 14

#     offset = get_offset(offset)

#     if df is None:
#         return

#     # Calculate Result
#     df["up"] = df["open"] < df["close"]
#     df["down"] = df["open"] > df["close"]
#     df["doji"] = df["open"] == df["close"]
#     df["body_hi"] = df[["open", "close"]].max(axis=1)
#     df["body_lo"] = df[["open", "close"]].min(axis=1)
#     df["body"] = df["body_hi"] - df["body_lo"]
#     df["body_avg"] = df["body"].rolling(window=length).mean()
#     df["has_up_shadow"] = (df["high"] - df["body_hi"]) > 0.05 * df["body"]
#     df["has_dn_shadow"] = (df["body_lo"] - df["low"]) > 0.05 * df["body"]
#     df["down_trend"] = df["close"] < df["close"].rolling(window=50).mean()

#     # Imbalance calculations
#     df["top_imbalance_size"] = df["low"].shift(2) - df["high"]
#     df["bottom_imbalance_size"] = df["low"] - df["high"].shift(2)
#     day_adr = (
#         df["high"].rolling(window=length).max() - df["low"].rolling(window=length).min()
#     )
#     df["top_imbalance_percentage"] = (df["top_imbalance_size"] / day_adr) * 100
#     df["bottom_imbalance_percentage"] = (df["bottom_imbalance_size"] / day_adr) * 100

#     # Adding flags for significant imbalances
#     df["top_imbalance_flag"] = (df["top_imbalance_size"] > 0) & (
#         df["top_imbalance_percentage"] > 1
#     )
#     df["bottom_imbalance_flag"] = (df["bottom_imbalance_size"] > 0) & (
#         df["bottom_imbalance_percentage"] > 1
#     )

#     # Offset
#     if offset != 0:
#         df = df.shift(offset)

#     # Handle fills
#     if "fillna" in kwargs:
#         df.fillna(kwargs["fillna"], inplace=True)
#     if "fill_method" in kwargs:
#         df.fillna(method=kwargs["fill_method"], inplace=True)

#     # Name and Categorize it
#     df.name = f"SMI_{length}"
#     df.category = "momentum"



def smc(df):
    # Temporarily rename columns for compatibility
    # df = df.rename(
    #     columns={"bid_o": "open", "bid_c": "close", "bid_h": "high", "bid_l": "low"}
    # )

    df["up"] = df["open"] < df["close"]
    df["down"] = df["open"] > df["close"]
    df["doji"] = df["open"] == df["close"]
    df["body_hi"] = df[["open", "close"]].max(axis=1)
    df["body_lo"] = df[["open", "close"]].min(axis=1)
    df["body"] = df["body_hi"] - df["body_lo"]
    df["body_avg"] = df["body"].rolling(window=14).mean()
    df["small_body"] = df["body"] < df["body_avg"]
    df["long_body"] = df["body"] > df["body_avg"]
    df["white_body"] = df["open"] < df["close"]
    df["black_body"] = df["open"] > df["close"]
    df["up_shadow"] = df["high"] - df["body_hi"]
    df["dn_shadow"] = df["body_lo"] - df["low"]
    df["has_up_shadow"] = df["up_shadow"] > 0.05 * df["body"]
    df["has_dn_shadow"] = df["dn_shadow"] > 0.05 * df["body"]
    df["down_trend"] = df["close"] < df["close"].rolling(window=50).mean()

    # Calculate imbalance sizes and percentages based on day average range
    df["top_imbalance_size"] = df["low"].shift(2) - df["high"]
    df["bottom_imbalance_size"] = df["low"] - df["high"].shift(2)
    day_adr = df["high"].rolling(window=14).max() - df["low"].rolling(window=14).min()
    df["top_imbalance_percentage"] = (df["top_imbalance_size"] / day_adr) * 100
    df["bottom_imbalance_percentage"] = (df["bottom_imbalance_size"] / day_adr) * 100
    df["volatility"] = df["high"] - df["low"]
    df["vol_avg"] = df["volatility"].rolling(window=20).mean()
    df["high_volatility"] = df["volatility"] > 1.5 * df["vol_avg"]
    
    # Adding flags for significant imbalances
    df["top_imbalance_flag"] = (df["top_imbalance_size"] > 0) & (
        df["top_imbalance_percentage"] > 1
    )
    df["bottom_imbalance_flag"] = (df["bottom_imbalance_size"] > 0) & (
        df["bottom_imbalance_percentage"] > 1
    )
    
    # Correct way to fill NaN values
    df.ffill(inplace=True)  # Forward fill
    df.bfill(inplace=True)  # Backward fill if any NaN at the start

    return df


smc.__doc__ = """Smart Money Comcept (SMC)

The Smart Money concept combines several techniques to identify significant
price movements that might indicate 'smart money' actions. It uses candlestick
patterns, moving averages, and imbalance calculations.

Sources:
    None (custom method)

Calculation:
    Default Inputs:
        length=14

Args:
    df (pd.DataFrame): DataFrame containing 'open', 'high', 'low', 'close' data
    length (int): The length of the period for rolling calculations. Default: 14
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: Original DataFrame with new columns for the indicator.
"""
