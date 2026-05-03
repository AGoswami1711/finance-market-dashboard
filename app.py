import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

# 1. Page Configuration (Looks professional on GitHub demos)
st.set_page_config(page_title="Professional Finance Dashboard", layout="wide")

st.title("📈 Real-Time Finance Tracker & Data Exporter")
st.markdown("Developed for automated financial analysis and data extraction.")

# 2. Sidebar for Client Inputs
st.sidebar.header("Dashboard Controls")
ticker = st.sidebar.text_input("Stock/Crypto Symbol", value="BTC-USD")
period = st.sidebar.selectbox("Select Time Period", options=["1mo", "3mo", "6mo", "1y", "5y", "max"])

# 3. Data Extraction using yfinance
data = yf.download(ticker, period=period, interval="1d")

if not data.empty:
    # Get the latest price metrics
    last_price = data['Close'].iloc[-1]
    prev_price = data['Close'].iloc[-2]
    price_diff = last_price - prev_price

    # 4. Display KPI Metrics
    col1, col2 = st.columns(2)
    col1.metric(label=f"Current Price ({ticker})", value=f"${last_price:,.2f}", delta=f"{price_diff:,.2f}")
    
    # 5. Interactive Visualization
    fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Historical Trend")
    st.plotly_chart(fig, use_container_width=True)

    # 6. Data Export (Critical Freelance Skill)
    st.subheader("Data Export Center")
    csv = data.to_csv().encode('utf-8')
    st.download_button(
        label="Download Financial Data as CSV",
        data=csv,
        file_name=f"{ticker}_data.csv",
        mime="text/csv",
    )

    with st.expander("Preview Raw Data"):
        st.dataframe(data)

else:
    st.error("No data found. Please verify the ticker symbol.")