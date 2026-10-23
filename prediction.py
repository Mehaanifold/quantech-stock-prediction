"""
prediction.py - Mathematical Prediction & Forecasting Engine
Part of Agile Assignment No. 1 (Semester V, Data Science) - LO2

This module provides basic, transparent mathematical methods for illustrative stock
forecasting:
1. Rolling Simple Moving Averages (SMA-7 and SMA-14).
2. Linear Trend Extrapolation using Ordinary Least Squares (OLS: y = mx + c).
3. Illustrative forecast error bands based on historical residual variance.

NOTE: All predictions are illustrative and strictly for academic demonstration.
"""

from datetime import timedelta
import pandas as pd
import numpy as np


def compute_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """Computes 7-day and 14-day rolling simple moving averages (SMA)."""
    df = df.copy()
    df["SMA_7"] = df["Close"].rolling(window=7, min_periods=1).mean().round(2)
    df["SMA_14"] = df["Close"].rolling(window=14, min_periods=1).mean().round(2)
    return df


def forecast_linear_trend(df: pd.DataFrame, forecast_days: int = 7) -> tuple[pd.DataFrame, dict]:
    """
    Fits an OLS Linear Trend (y = mx + c) over recent closing prices and projects
    the trend for the next `forecast_days` trading sessions.
    
    Returns:
        forecast_df: DataFrame with historical + projected points with upper/lower bounds.
        metrics: Dictionary containing slope, predicted price, expected change %, signal.
    """
    if df is None or len(df) < 2:
        raise ValueError("Historical DataFrame must contain at least 2 rows for trend analysis.")
    if "Close" not in df.columns or "Date" not in df.columns:
        raise ValueError("DataFrame must contain 'Date' and 'Close' columns.")
    if forecast_days < 1:
        raise ValueError("forecast_days must be a positive integer greater than or equal to 1.")

    df = df.copy().reset_index(drop=True)
    n = len(df)
    
    # Independent variable x = 0, 1, 2, ..., n-1
    x = np.arange(n)
    y = df["Close"].values
    
    # Fit linear regression line: y = m*x + c
    poly_fit = np.polyfit(x, y, deg=1)
    slope = float(poly_fit[0])
    intercept = float(poly_fit[1])
    
    # Calculate residuals and standard error for illustrative confidence band
    fitted_vals = slope * x + intercept
    residuals = y - fitted_vals
    residual_std = float(np.std(residuals))
    
    # Project into future
    last_date = df["Date"].iloc[-1]
    future_dates = []
    curr = last_date
    while len(future_dates) < forecast_days:
        curr += timedelta(days=1)
        if curr.weekday() < 5:  # Skip weekends
            future_dates.append(curr)
            
    future_x = np.arange(n, n + forecast_days)
    future_y = slope * future_x + intercept
    
    # Projected dataframe
    future_records = []
    for d, p in zip(future_dates, future_y):
        future_records.append({
            "Date": d,
            "Type": "Forecast",
            "Price": round(float(p), 2),
            "Lower_Bound": round(float(p - 1.96 * residual_std), 2),
            "Upper_Bound": round(float(p + 1.96 * residual_std), 2),
        })
    forecast_future_df = pd.DataFrame(future_records)
    
    # Historical series for plotting alignment
    hist_records = []
    for _, row in df.iterrows():
        hist_records.append({
            "Date": row["Date"],
            "Type": "Historical",
            "Price": round(float(row["Close"]), 2),
            "Lower_Bound": round(float(row["Close"]), 2),
            "Upper_Bound": round(float(row["Close"]), 2),
        })
    forecast_hist_df = pd.DataFrame(hist_records)
    
    combined_df = pd.concat([forecast_hist_df, forecast_future_df], ignore_index=True)
    
    latest_close = float(df.iloc[-1]["Close"])
    target_price = round(float(future_y[-1]), 2)
    expected_change = round(target_price - latest_close, 2)
    expected_change_pct = round((expected_change / latest_close) * 100, 2)
    
    # Trend signal determination
    if slope > 1.5:
        signal = "Bullish Uptrend (↗)"
        signal_color = "green"
    elif slope < -1.5:
        signal = "Bearish Downtrend (↘)"
        signal_color = "red"
    else:
        signal = "Neutral / Sideways (↔)"
        signal_color = "gray"
        
    metrics = {
        "slope": round(slope, 3),
        "intercept": round(intercept, 2),
        "residual_std": round(residual_std, 2),
        "latest_close": latest_close,
        "target_price": target_price,
        "expected_change": expected_change,
        "expected_change_pct": expected_change_pct,
        "forecast_days": forecast_days,
        "signal": signal,
        "signal_color": signal_color,
    }
    
    return combined_df, metrics


def get_disclaimer_text() -> str:
    """Returns the standardized academic disclaimer message."""
    return (
        "⚠️ **Academic & Illustrative Disclaimer:**\n\n"
        "This stock analytics and prediction module is created exclusively for **Agile Assignment No. 1 "
        "(Semester V, TE Data Science - LO2)**. All historical figures and linear trend extrapolations are "
        "hardcoded or generated using simplified mathematical formulas for demonstration purposes. "
        "This application does **not** connect to live stock exchanges, does **not** utilize real-time market data, "
        "and is **NOT financial advice**. Do not make investment or trading decisions based on this demo."
    )
