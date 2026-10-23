"""
app.py - Quantech Stock Analytics & Prediction Web Application
Built with Streamlit and Python
Part of Agile Assignment No. 1 (Semester V, TE Data Science)
"""

import streamlit as st
import pandas as pd
import altair as alt
from stock_data import (
    get_available_tickers,
    get_stock_meta,
    get_stock_data,
    get_stock_summary,
)
from prediction import (
    compute_moving_averages,
    forecast_linear_trend,
    get_disclaimer_text,
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Quantech Stock Analytics & Forecasting",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 0.98rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Header Section
# ---------------------------------------------------------
st.markdown('<div class="main-title">📈 Quantech: Stock Analytics & Forecasting Platform</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Agile Assignment No. 1 — LO2: Source Code Management with Git & GitHub '
    '| Semester V, TE Data Science</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.header("🎯 Stock & Model Controls")
tickers = get_available_tickers()
selected_ticker = st.sidebar.selectbox("Choose a Stock Symbol:", tickers, index=0)

meta = get_stock_meta(selected_ticker)
st.sidebar.markdown(f"**Company:** {meta.get('name', selected_ticker)}")
st.sidebar.markdown(f"**Sector:** {meta.get('sector', 'N/A')}")
st.sidebar.markdown(f"**Currency:** {meta.get('currency', 'INR')}")
st.sidebar.markdown("---")

days_filter = st.sidebar.slider(
    "Historical Window (Days):",
    min_value=15,
    max_value=50,
    value=30,
    step=5,
)

forecast_days = st.sidebar.slider(
    "Prediction Horizon (Days):",
    min_value=3,
    max_value=14,
    value=7,
    step=1,
)

show_sma = st.sidebar.checkbox("Overlay Moving Averages (SMA-7 & SMA-14)", value=True)

st.sidebar.markdown("---")
st.sidebar.info("💡 Hardcoded sample data for demonstration. No live API connectivity.")

# ---------------------------------------------------------
# Load Data & Run Models
# ---------------------------------------------------------
full_df = get_stock_data(selected_ticker)
df = full_df.tail(days_filter).copy()
df_with_sma = compute_moving_averages(df)
summary = get_stock_summary(selected_ticker)
forecast_df, pred_metrics = forecast_linear_trend(df, forecast_days=forecast_days)

# ---------------------------------------------------------
# Key Performance Metrics
# ---------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label=f"Current Price ({meta.get('currency', 'INR')})",
        value=f"₹{summary['latest_close']:,.2f}",
        delta=f"{summary['abs_change']:+,.2f} ({summary['pct_change']:+.2f}%)",
    )

with col2:
    st.metric(
        label="Previous Close",
        value=f"₹{summary['prev_close']:,.2f}",
    )

with col3:
    st.metric(
        label=f"{days_filter}D High",
        value=f"₹{df['High'].max():,.2f}",
    )

with col4:
    st.metric(
        label=f"{forecast_days}D Projected Target",
        value=f"₹{pred_metrics['target_price']:,.2f}",
        delta=f"{pred_metrics['expected_change']:+,.2f} ({pred_metrics['expected_change_pct']:+.2f}%)",
    )

with col5:
    st.metric(
        label="Trend Signal",
        value=pred_metrics["signal"],
    )

st.markdown("---")

# ---------------------------------------------------------
# Main Tabs: Dashboard & Forecast
# ---------------------------------------------------------
tab_chart, tab_forecast, tab_data = st.tabs([
    "📈 Historical Dashboard",
    "🔮 Illustrative Prediction Model",
    "📁 Raw OHLCV Dataset",
])

with tab_chart:
    st.subheader(f"Historical Price Analysis — {selected_ticker} ({days_filter} Trading Days)")
    
    # Base chart: Close price
    base = alt.Chart(df_with_sma).encode(
        x=alt.X("Date:T", title="Trading Date", axis=alt.Axis(format="%d %b %Y"))
    )
    
    line_close = base.mark_line(color="#2563EB", strokeWidth=2.5).encode(
        y=alt.Y("Close:Q", title="Price (INR)", scale=alt.Scale(domain=[df["Low"].min() * 0.98, df["High"].max() * 1.02])),
        tooltip=[
            alt.Tooltip("Date:T", format="%Y-%m-%d"),
            alt.Tooltip("Close:Q", format=",.2f", title="Close (₹)"),
        ],
    )
    
    chart_layers = [line_close]
    
    if show_sma:
        line_sma7 = base.mark_line(color="#10B981", strokeDash=[4, 3], strokeWidth=1.8).encode(
            y="SMA_7:Q",
            tooltip=[alt.Tooltip("SMA_7:Q", format=",.2f", title="SMA-7 (₹)")],
        )
        line_sma14 = base.mark_line(color="#F59E0B", strokeDash=[6, 4], strokeWidth=1.8).encode(
            y="SMA_14:Q",
            tooltip=[alt.Tooltip("SMA_14:Q", format=",.2f", title="SMA-14 (₹)")],
        )
        chart_layers.extend([line_sma7, line_sma14])
        st.caption("🟢 Green Dashed: SMA-7 | 🟠 Orange Dashed: SMA-14 | 🔵 Solid Blue: Close Price")

    final_chart = alt.layer(*chart_layers).properties(height=380).interactive()
    st.altair_chart(final_chart, use_container_width=True)

with tab_forecast:
    st.subheader(f"Illustrative Mathematical Forecast (OLS Trend: {forecast_days}-Day Horizon)")
    
    c_left, c_right = st.columns([3, 1])
    
    with c_right:
        st.markdown("#### 📐 Model Parameters")
        st.write(f"- **Method:** Ordinary Least Squares ($y = mx + c$)")
        st.write(f"- **Trend Slope ($m$):** `₹{pred_metrics['slope']}/day`")
        st.write(f"- **Intercept ($c$):** `₹{pred_metrics['intercept']}`")
        st.write(f"- **Residual Std ($\sigma$):** `₹{pred_metrics['residual_std']}`")
        st.write(f"- **Target Price:** `₹{pred_metrics['target_price']}`")
        st.write(f"- **Expected Return:** `{pred_metrics['expected_change_pct']}%`")
        
    with c_left:
        # Forecast chart with band
        band = alt.Chart(forecast_df).mark_area(opacity=0.18, color="#8B5CF6").encode(
            x=alt.X("Date:T", title="Date", axis=alt.Axis(format="%d %b")),
            y="Lower_Bound:Q",
            y2="Upper_Bound:Q",
        )
        
        lines = alt.Chart(forecast_df).mark_line(point=True).encode(
            x=alt.X("Date:T"),
            y=alt.Y("Price:Q", title="Price (INR)", scale=alt.Scale(zero=False)),
            color=alt.Color("Type:N", scale=alt.Scale(
                domain=["Historical", "Forecast"],
                range=["#2563EB", "#7C3AED"]
            )),
            strokeDash=alt.condition(
                alt.datum.Type == "Forecast",
                alt.value([5, 5]),
                alt.value([0])
            ),
            tooltip=[
                alt.Tooltip("Date:T", format="%Y-%m-%d"),
                alt.Tooltip("Type:N"),
                alt.Tooltip("Price:Q", format=",.2f"),
                alt.Tooltip("Lower_Bound:Q", format=",.2f"),
                alt.Tooltip("Upper_Bound:Q", format=",.2f"),
            ],
        )
        
        forecast_chart = (band + lines).properties(height=380).interactive()
        st.altair_chart(forecast_chart, use_container_width=True)

with tab_data:
    st.subheader(f"Historical OHLCV Data Table — {selected_ticker}")
    display_df = df_with_sma.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(
        display_df.sort_values(by="Date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
    
    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv_data,
        file_name=f"{selected_ticker}_historical_data.csv",
        mime="text/csv",
    )

# ---------------------------------------------------------
# Educational & Regulatory Disclaimer
# ---------------------------------------------------------
st.markdown("---")
st.warning(get_disclaimer_text())
