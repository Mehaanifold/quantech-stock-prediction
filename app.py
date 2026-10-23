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

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Quantech Stock Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-box {
        background-color: #F3F4F6;
        border-radius: 8px;
        padding: 12px;
        border-left: 4px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Header Section
# ---------------------------------------------------------
st.markdown('<div class="main-title">📈 Quantech: Stock Analytics & Forecasting</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Agile Assignment No. 1 — LO2: Source Code Management with Git & GitHub '
    '| Semester V, TE Data Science</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.header("🎯 Stock Selection")
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

# ---------------------------------------------------------
# Load and Filter Data
# ---------------------------------------------------------
full_df = get_stock_data(selected_ticker)
df = full_df.tail(days_filter).copy()
summary = get_stock_summary(selected_ticker)

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
        label=f"{days_filter}D Low",
        value=f"₹{df['Low'].min():,.2f}",
    )

with col5:
    st.metric(
        label="Avg Daily Volume",
        value=f"{summary['avg_volume']:,}",
    )

st.markdown("---")

# ---------------------------------------------------------
# Historical Price Interactive Chart
# ---------------------------------------------------------
st.subheader(f"📊 Historical Price Chart — {selected_ticker} ({days_filter} Trading Days)")

chart = (
    alt.Chart(df)
    .mark_line(point=True, color="#2563EB", strokeWidth=2)
    .encode(
        x=alt.X("Date:T", title="Trading Date", axis=alt.Axis(format="%d %b %Y")),
        y=alt.Y(
            "Close:Q",
            title="Closing Price (INR)",
            scale=alt.Scale(domain=[df["Low"].min() * 0.98, df["High"].max() * 1.02]),
        ),
        tooltip=[
            alt.Tooltip("Date:T", title="Date", format="%Y-%m-%d"),
            alt.Tooltip("Open:Q", title="Open (₹)", format=",.2f"),
            alt.Tooltip("High:Q", title="High (₹)", format=",.2f"),
            alt.Tooltip("Low:Q", title="Low (₹)", format=",.2f"),
            alt.Tooltip("Close:Q", title="Close (₹)", format=",.2f"),
            alt.Tooltip("Volume:Q", title="Volume", format=","),
        ],
    )
    .properties(height=380)
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

# ---------------------------------------------------------
# Raw Data Table Preview
# ---------------------------------------------------------
with st.expander("📁 View Historical OHLCV Data Table"):
    display_df = df.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(
        display_df.sort_values(by="Date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
