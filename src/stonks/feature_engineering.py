from __future__ import annotations

import pandas as pd
import numpy as np


def compute_indicators(
    df: pd.DataFrame,
    price_col: str = "vw",
    window_short: int = 10,
    window_long: int = 50,
    sharpe_windows: list[int] = [20, 60, 120]
) -> pd.DataFrame:
    df = df.copy()
    price = df[price_col]

    # Returns & moving averages
    df["ret_1"] = price.pct_change()
    df["sma_short"] = price.rolling(window_short, min_periods=1).mean()
    df["sma_long"] = price.rolling(window_long, min_periods=1).mean()
    df["ema_short"] = price.ewm(span=window_short, adjust=False).mean()
    df["ema_long"] = price.ewm(span=window_long, adjust=False).mean()

    # Momentum
    df["momentum"] = (df["sma_short"] - df["sma_long"]) / df["sma_long"]

    # Volatility (annualized)
    df["vol_20"] = df["ret_1"].rolling(20, min_periods=1).std() * np.sqrt(252)

    # RSI (14-day)
    delta = price.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(14, min_periods=1).mean()
    roll_down = down.rolling(14, min_periods=1).mean()
    rs = roll_up / (roll_down + 1e-12)
    df["rsi"] = 100 - (100 / (1 + rs))

    # MACD
    ema_12 = price.ewm(span=12, adjust=False).mean()
    ema_26 = price.ewm(span=26, adjust=False).mean()
    df["macd"] = ema_12 - ema_26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

    # Z-score (20-day)
    rolling_mean = price.rolling(20, min_periods=1).mean()
    rolling_std = price.rolling(20, min_periods=1).std(ddof=0)
    df["zscore_20"] = (price - rolling_mean) / (rolling_std + 1e-12)

    # Skewness & kurtosis
    df["skew_20"] = price.rolling(20, min_periods=1).apply(lambda x: pd.Series(x).skew(), raw=False)
    df["kurt_20"] = price.rolling(20, min_periods=1).apply(lambda x: pd.Series(x).kurt(), raw=False)

    # Bollinger Bands
    bb_mid = price.rolling(20, min_periods=1).mean()
    bb_std = price.rolling(20, min_periods=1).std(ddof=0)
    df["bb_mid"] = bb_mid
    df["bb_upper"] = bb_mid + 2 * bb_std
    df["bb_lower"] = bb_mid - 2 * bb_std

    # Rolling Sharpe Ratios
    for w in sharpe_windows:
        roll_ret = df["ret_1"].rolling(w, min_periods=1)
        mean_ret = roll_ret.mean()
        std_ret = roll_ret.std(ddof=0)
        df[f"sharpe_{w}"] = (mean_ret / (std_ret + 1e-12)) * np.sqrt(252)

    return df.dropna()







