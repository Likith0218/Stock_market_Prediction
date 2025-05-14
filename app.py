import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

# Function to fetch live data and plot the chart
def display_live_stock_chart(stock_symbol):
    st.subheader(f"📈 Live Stock Price for {stock_symbol}")
    try:
        stock_data = yf.download(stock_symbol, period="1d", interval="1m", progress=False)
        if stock_data.empty:
            st.warning("No data available for the given stock symbol.")
            return

        # Plot the live stock data
        fig = go.Figure(data=[go.Scatter(
            x=stock_data.index,
            y=stock_data['Close'],
            mode='lines+markers',
            name='Close Price'
        )])
        fig.update_layout(
            title=f"Live Stock Prices for {stock_symbol}",
            xaxis_title="Time",
            yaxis_title="Price",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")

# Sidebar for stock selection
st.sidebar.header("Stock Market Dashboard")
selected_stock = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", value="AAPL")

# Call the live chart function
display_live_stock_chart(selected_stock)
