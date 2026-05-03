import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Professional Finance Dashboard", layout="wide")

st.title("📈 Real-Time Finance Tracker & Data Exporter")
st.markdown("Developed for automated financial analysis and data extraction.")

# 2. Sidebar for Client Inputs
st.sidebar.header("Dashboard Controls")
ticker = st.sidebar.text_input("Stock/Crypto Symbol", value="BTC-USD")
period = st.sidebar.selectbox("Select Time Period", options=["1mo", "3mo", "6mo", "1y", "5y", "max"])

# 3. Data Extraction (Ultra-Reliable Mode)
data = yf.download(ticker, period=period, interval="1d")

if not data.empty:
    # This part is updated to be "Bulletproof"
    try:
        # Flatten the data in case it's a multi-index
        df = data.copy()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        close_series = df['Close']
        
        # Get the latest values
        last_price = float(close_series.iloc[-1])
        prev_price = float(close_series.iloc[-2])
        price_diff = last_price - prev_price

        # 4. Display KPI Metrics
        col1, col2 = st.columns(2)
        col1.metric(label=f"Current Price ({ticker})", value=f"${last_price:,.2f}", delta=f"{price_diff:,.2f}")
        
        # 5. Interactive Visualization
        fig = px.line(df, x=df.index, y='Close', title=f"{ticker} Historical Trend")
        st.plotly_chart(fig, use_container_width=True)

        # 6. Data Export
        st.subheader("Data Export Center")
        csv = df.to_csv().encode('utf-8')
        st.download_button(
            label="Download Financial Data as CSV",
            data=csv,
            file_name=f"{ticker}_data.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"Data Processing Error: {e}")

    with st.expander("Preview Raw Data"):
        st.dataframe(data)
else:
    st.error("No data found. Please verify the ticker symbol.")   
