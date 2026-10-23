"""
tests/test_app.py - Automated Unit & Integration Tests
Part of Agile Assignment No. 1 (Semester V, TE Data Science) - LO3 (CI/CD Pipeline)

Tests verify:
1. Basic module imports (app, stock_data, prediction).
2. Hardcoded stock dataset integrity, shapes, metadata, and summary calculations.
3. Moving average calculation (SMA-7 and SMA-14).
4. Prediction calculations using known hardcoded and synthetic inputs.
5. Invariant checks on prediction error bounds and trend signals.
6. Exception handling on empty, incomplete, or invalid input.
"""

from datetime import datetime, timedelta
import pytest
import pandas as pd
import numpy as np

# Core module imports
import stock_data
import prediction


# =====================================================================
# 1. Module Import Tests
# =====================================================================

def test_module_imports():
    """Verify core application modules import without error."""
    assert stock_data is not None
    assert prediction is not None


# =====================================================================
# 2. Stock Data Module Tests
# =====================================================================

def test_available_tickers():
    """Verify available tickers list is non-empty and contains expected equities."""
    tickers = stock_data.get_available_tickers()
    assert isinstance(tickers, list)
    assert len(tickers) == 4
    for expected in ["RELIANCE", "TCS", "INFY", "HDFCBANK"]:
        assert expected in tickers


def test_stock_metadata():
    """Verify stock metadata contains name, sector, and positive base price."""
    for ticker in stock_data.get_available_tickers():
        meta = stock_data.get_stock_meta(ticker)
        assert isinstance(meta, dict)
        assert "name" in meta
        assert "sector" in meta
        assert "currency" in meta
        assert meta["base_price"] > 0


def test_stock_data_shape_and_columns():
    """Verify stock historical DataFrame structure and required OHLCV columns."""
    df = stock_data.get_stock_data("RELIANCE")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 50
    expected_cols = {"Date", "Open", "High", "Low", "Close", "Volume"}
    assert expected_cols.issubset(set(df.columns))
    # Ensure High >= Low and Close is positive
    assert (df["High"] >= df["Low"]).all()
    assert (df["Close"] > 0).all()


def test_stock_data_invalid_ticker():
    """Verify requesting an invalid ticker raises ValueError."""
    with pytest.raises(ValueError, match="not found in hardcoded dataset"):
        stock_data.get_stock_data("UNKNOWN_TICKER")


def test_stock_summary():
    """Verify stock summary metrics calculation."""
    summary = stock_data.get_stock_summary("TCS")
    assert "latest_close" in summary
    assert "prev_close" in summary
    assert "abs_change" in summary
    assert "pct_change" in summary
    assert "period_high" in summary
    assert "period_low" in summary
    assert summary["period_high"] >= summary["period_low"]
    assert summary["records_count"] == 50


# =====================================================================
# 3. Technical Indicator Tests (Moving Averages)
# =====================================================================

def test_compute_moving_averages():
    """Verify SMA-7 and SMA-14 columns are computed correctly."""
    df = stock_data.get_stock_data("INFY").tail(20)
    df_sma = prediction.compute_moving_averages(df)
    assert "SMA_7" in df_sma.columns
    assert "SMA_14" in df_sma.columns
    # Check that tail has non-null float averages
    assert not df_sma["SMA_7"].isna().any()
    assert not df_sma["SMA_14"].isna().any()


# =====================================================================
# 4. Mathematical Prediction & Trend Forecast Tests
# =====================================================================

def test_prediction_output_structure_and_shape():
    """Verify forecast returns combined dataframe and metrics with expected length."""
    df = stock_data.get_stock_data("RELIANCE").tail(30)
    forecast_days = 7
    combined_df, metrics = prediction.forecast_linear_trend(df, forecast_days=forecast_days)
    
    # Combined length must be len(historical) + forecast_days
    assert len(combined_df) == len(df) + forecast_days
    
    # Required columns
    expected_cols = {"Date", "Type", "Price", "Lower_Bound", "Upper_Bound"}
    assert expected_cols.issubset(set(combined_df.columns))
    
    # Check split of Historical vs Forecast
    assert (combined_df["Type"] == "Historical").sum() == len(df)
    assert (combined_df["Type"] == "Forecast").sum() == forecast_days


def test_prediction_numerical_invariants():
    """Verify forecast error bounds: Upper_Bound >= Price >= Lower_Bound."""
    df = stock_data.get_stock_data("HDFCBANK").tail(25)
    combined_df, metrics = prediction.forecast_linear_trend(df, forecast_days=5)
    
    forecast_rows = combined_df[combined_df["Type"] == "Forecast"]
    assert (forecast_rows["Upper_Bound"] >= forecast_rows["Price"]).all()
    assert (forecast_rows["Price"] >= forecast_rows["Lower_Bound"]).all()
    
    # Metrics consistency
    assert metrics["forecast_days"] == 5
    assert metrics["target_price"] == forecast_rows["Price"].iloc[-1]
    expected_change = round(metrics["target_price"] - metrics["latest_close"], 2)
    assert metrics["expected_change"] == expected_change
    assert metrics["signal"] in [
        "Bullish Uptrend (↗)",
        "Bearish Downtrend (↘)",
        "Neutral / Sideways (↔)",
    ]


def test_prediction_known_linear_input():
    """Verify OLS model against known deterministic linear series y = 2x + 10."""
    dates = [datetime(2026, 10, 1) + timedelta(days=i) for i in range(10)]
    prices = [2.0 * i + 10.0 for i in range(10)]  # x in [0..9]
    df_synthetic = pd.DataFrame({"Date": dates, "Close": prices})
    
    combined_df, metrics = prediction.forecast_linear_trend(df_synthetic, forecast_days=3)
    
    # Slope must be exactly 2.0 and intercept 10.0
    assert pytest.approx(metrics["slope"], rel=1e-3) == 2.0
    assert pytest.approx(metrics["intercept"], rel=1e-3) == 10.0
    
    # Residual standard deviation must be ~0 since input is perfectly linear
    assert pytest.approx(metrics["residual_std"], abs=1e-2) == 0.0
    
    # Future x are 10, 11, 12 -> Price at x=12 must be 2*12 + 10 = 34.0
    forecast_rows = combined_df[combined_df["Type"] == "Forecast"]
    assert pytest.approx(forecast_rows["Price"].iloc[-1], rel=1e-3) == 34.0


# =====================================================================
# 5. Input Validation & Error Handling Tests
# =====================================================================

def test_prediction_empty_or_too_small_dataframe():
    """Verify ValueError is raised if DataFrame has fewer than 2 rows."""
    empty_df = pd.DataFrame(columns=["Date", "Close"])
    with pytest.raises(ValueError, match="at least 2 rows"):
        prediction.forecast_linear_trend(empty_df, forecast_days=5)

    single_row_df = pd.DataFrame({"Date": [datetime(2026, 10, 1)], "Close": [100.0]})
    with pytest.raises(ValueError, match="at least 2 rows"):
        prediction.forecast_linear_trend(single_row_df, forecast_days=5)


def test_prediction_missing_columns():
    """Verify ValueError is raised if 'Close' or 'Date' is missing."""
    invalid_df = pd.DataFrame({"Price": [100.0, 105.0], "Day": ["2026-10-01", "2026-10-02"]})
    with pytest.raises(ValueError, match="must contain 'Date' and 'Close'"):
        prediction.forecast_linear_trend(invalid_df, forecast_days=5)


def test_prediction_invalid_forecast_days():
    """Verify ValueError is raised if forecast_days is < 1."""
    df = stock_data.get_stock_data("RELIANCE").tail(10)
    with pytest.raises(ValueError, match="positive integer"):
        prediction.forecast_linear_trend(df, forecast_days=0)


# =====================================================================
# 6. Academic Disclaimer Text Test
# =====================================================================

def test_disclaimer_text():
    """Verify academic disclaimer is non-empty and includes key educational terms."""
    disclaimer = prediction.get_disclaimer_text()
    assert isinstance(disclaimer, str)
    assert len(disclaimer) > 50
    assert "Academic" in disclaimer or "Disclaimer" in disclaimer
    assert "financial advice" in disclaimer.lower()
