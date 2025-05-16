import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date, timedelta
import plotly.graph_objects as go
import time
from requests.exceptions import RequestException

# Page config must be the first Streamlit command
st.set_page_config(page_title="Stock Trend Analysis", layout="wide")

# Move sidebar warning after page config
st.sidebar.warning("""
    ⚠️ Note: Yahoo Finance has rate limits.
    If you encounter errors, please wait a few seconds before trying again.
""")

# Add CSS for better styling
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="big-font">Stock Trend Analysis & Prediction</p>', unsafe_allow_html=True)

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    # Stock symbol input with validation
    ticker = st.text_input('Enter Stock Symbol (e.g., AAPL, MSFT, GOOGL):', 'AAPL').upper()
    
    # Add period selector
    time_period = st.selectbox(
        "Select Time Period",
        ["1 Month", "3 Months", "6 Months", "1 Year", "2 Years", "5 Years"]
    )

with col2:
    # Add technical indicator selection
    moving_average = st.multiselect(
        'Select Moving Averages',
        ['20 MA', '50 MA', '100 MA', '200 MA'],
        default=['50 MA', '200 MA']
    )

# Calculate start date based on selected period
period_dict = {
    "1 Month": 30,
    "3 Months": 90,
    "6 Months": 180,
    "1 Year": 365,
    "2 Years": 730,
    "5 Years": 1825
}
start_date = date.today() - timedelta(days=period_dict[time_period])
end_date = date.today()

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def load_data(ticker, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            # Get stock info
            stock = yf.Ticker(ticker)
            
            # Fetch historical data with specific interval
            data = stock.history(
                start=start_date,
                end=end_date,
                interval='1d',
                actions=False,
                prepost=False
            )
            
            if data.empty:
                if attempt == max_retries - 1:
                    st.error(f"No data found for {ticker}. Please verify the stock symbol.")
                    return None, None
                time.sleep(delay)
                continue
            
            # Add delay before fetching info
            time.sleep(delay)
            
            try:
                info = stock.info
            except Exception as e:
                st.warning(f"Could not fetch complete info for {ticker}. Using basic data.")
                info = {
                    'marketCap': stock.fast_info.get('marketCap', 0),
                    'longName': ticker,
                    'sector': 'N/A'
                }
            
            data.reset_index(inplace=True)
            return data, info
            
        except Exception as e:
            if attempt == max_retries - 1:
                st.error(f"Error fetching data: {str(e)}")
                return None, None
            st.warning(f"Attempt {attempt + 1} failed, retrying in {delay} seconds...")
            time.sleep(delay * 2)
    
    return None, None

# Show loading state
with st.spinner(f'Fetching data for {ticker}... This may take a few seconds'):
    data, info = load_data(ticker)

if data is not None and not data.empty:
    # Display company info
    st.subheader('Company Information')
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Price", f"{data['Close'].iloc[-1]:.2f}")
    with col2:
        st.metric("Market Cap", f"{info.get('marketCap', 0)/1e9:.2f}B")
    with col3:
        price_change = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
        st.metric("Period Change", f"{price_change:.2f}%")

    # Create interactive chart using Plotly
    fig = go.Figure()
    
    # Add candlestick
    fig.add_trace(go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='OHLC'
    ))
    
    # Add selected moving averages
    ma_dict = {'20 MA': 20, '50 MA': 50, '100 MA': 100, '200 MA': 200}
    colors = ['rgba(13, 205, 255, 0.8)', 'rgba(255, 207, 102, 0.8)', 
              'rgba(255, 102, 102, 0.8)', 'rgba(102, 255, 102, 0.8)']
    
    for ma, color in zip(moving_average, colors):
        period = ma_dict[ma]
        data[f'MA_{period}'] = data['Close'].rolling(window=period).mean()
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=data[f'MA_{period}'],
            name=ma,
            line=dict(color=color, width=2)
        ))

    # Update layout
    fig.update_layout(
        title=f'{ticker} Stock Price Chart',
        yaxis_title='Stock Price (USD)',
        xaxis_title='Date',
        template='plotly_dark',
        height=800
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display trading volume
    volume_fig = go.Figure()
    volume_fig.add_trace(go.Bar(
        x=data['Date'],
        y=data['Volume'],
        name='Volume'
    ))
    volume_fig.update_layout(
        title='Trading Volume',
        yaxis_title='Volume',
        xaxis_title='Date',
        template='plotly_dark',
        height=400
    )
    st.plotly_chart(volume_fig, use_container_width=True)

else:
    st.error("Please enter a valid stock symbol")

# Add footer with disclaimer
st.markdown("""
---
**Disclaimer:** This tool is for educational purposes only. Do not use it as financial advice.
Stock data is provided by Yahoo Finance.
""")
