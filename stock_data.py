"""
stock_data.py - Hardcoded Sample Stock Market Data Module
Part of Agile Assignment No. 1 (Semester V, Data Science) - LO2

This module provides hardcoded historical stock price data for demonstration
purposes without requiring live exchange connections or third-party API keys.
"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Seed for reproducible sample dataset generation
np.random.seed(42)

AVAILABLE_STOCKS = {
    "RELIANCE": {
        "name": "Reliance Industries Ltd.",
        "sector": "Energy & Telecommunications",
        "currency": "INR (₹)",
        "base_price": 2850.0,
        "daily_volatility": 0.015,
        "drift": 0.0008,
    },
    "TCS": {
        "name": "Tata Consultancy Services Ltd.",
        "sector": "Information Technology",
        "currency": "INR (₹)",
        "base_price": 3950.0,
        "daily_volatility": 0.012,
        "drift": 0.0006,
    },
    "INFY": {
        "name": "Infosys Ltd.",
        "sector": "Information Technology",
        "currency": "INR (₹)",
        "base_price": 1520.0,
        "daily_volatility": 0.018,
        "drift": 0.0005,
    },
    "HDFCBANK": {
        "name": "HDFC Bank Ltd.",
        "sector": "Banking & Financial Services",
        "currency": "INR (₹)",
        "base_price": 1640.0,
        "daily_volatility": 0.014,
        "drift": 0.0007,
    },
}


def _generate_hardcoded_series(base_price: float, volatility: float, drift: float, days: int = 50) -> pd.DataFrame:
    """Generates a deterministic 50-day trading series starting from a fixed past date."""
    # Fixed end date for reproducible academic demonstration
    end_date = datetime(2026, 10, 20)
    # Generate business days backwards
    dates = []
    curr = end_date
    while len(dates) < days:
        if curr.weekday() < 5:  # Monday to Friday
            dates.append(curr)
        curr -= timedelta(days=1)
    dates.reverse()

    # Pre-calculated deterministic noise vector to simulate authentic market oscillations
    returns = np.array([
        0.004, -0.008, 0.012, 0.005, -0.002, 0.015, -0.011, 0.008, -0.004, 0.006,
        0.018, -0.007, -0.003, 0.011, 0.002, -0.014, 0.009, 0.016, -0.005, 0.003,
        -0.012, 0.007, 0.014, -0.006, 0.008, -0.002, 0.019, -0.015, 0.004, 0.010,
        -0.009, 0.013, 0.001, -0.006, 0.021, -0.008, 0.005, 0.012, -0.004, -0.001,
        0.017, -0.010, 0.006, 0.008, -0.003, 0.014, -0.007, 0.009, 0.002, 0.011
    ])

    prices = []
    current_p = base_price
    for r in returns:
        step = r * (volatility / 0.015) + drift
        current_p = round(current_p * (1.0 + step), 2)
        prices.append(current_p)

    records = []
    for d, c in zip(dates, prices):
        # Derive realistic intraday Open, High, Low, Volume
        o = round(c * (1.0 - 0.003 * np.sin(len(records))), 2)
        h = round(max(o, c) * (1.0 + 0.006), 2)
        l = round(min(o, c) * (1.0 - 0.006), 2)
        v = int(1_200_000 + 400_000 * np.cos(len(records)))
        records.append({
            "Date": d.strftime("%Y-%m-%d"),
            "Open": o,
            "High": h,
            "Low": l,
            "Close": c,
            "Volume": v,
        })

    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


# Precompute cached tables for available stocks
_STOCKS_CACHE = {
    symbol: _generate_hardcoded_series(
        meta["base_price"],
        meta["daily_volatility"],
        meta["drift"]
    )
    for symbol, meta in AVAILABLE_STOCKS.items()
}


def get_available_tickers() -> list:
    """Returns the list of available stock ticker symbols."""
    return list(AVAILABLE_STOCKS.keys())


def get_stock_meta(ticker: str) -> dict:
    """Returns metadata for a given stock symbol."""
    return AVAILABLE_STOCKS.get(ticker, {})


def get_stock_data(ticker: str) -> pd.DataFrame:
    """Returns historical price dataframe for the requested ticker."""
    if ticker not in _STOCKS_CACHE:
        raise ValueError(f"Ticker '{ticker}' not found in hardcoded dataset.")
    return _STOCKS_CACHE[ticker].copy()


def get_stock_summary(ticker: str) -> dict:
    """Returns latest price, absolute change, percentage change, and 50-day range."""
    df = get_stock_data(ticker)
    latest_close = df.iloc[-1]["Close"]
    prev_close = df.iloc[-2]["Close"]
    abs_change = round(latest_close - prev_close, 2)
    pct_change = round((abs_change / prev_close) * 100, 2)
    period_high = df["High"].max()
    period_low = df["Low"].min()
    period_vol = int(df["Volume"].mean())

    return {
        "latest_close": latest_close,
        "prev_close": prev_close,
        "abs_change": abs_change,
        "pct_change": pct_change,
        "period_high": period_high,
        "period_low": period_low,
        "avg_volume": period_vol,
        "records_count": len(df),
    }
