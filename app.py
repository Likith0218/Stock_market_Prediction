import streamlit as st
from Prediction import predict_end_of_day_price as predict_daily
from minute_prediction import predict_stock_price as predict_minute
from Hourly_stock_predictor import predict_hourly
from sentiment_analysis import fetch_news, analyze_sentiment, classify_sentiment
from live_chart import show_tradingview_chart

# Page configuration
st.set_page_config(page_title="Stock Market App", layout="wide")

# Helper function to format ticker symbol
def format_ticker(ticker):
    """Format ticker symbol for Indian/Global markets"""
    if any(char.isdigit() for char in ticker):  # Check if ticker contains numbers (like 500325)
        return f"{ticker}.BO"  # BSE stocks
    elif "." not in ticker and ticker.isalpha():  # If ticker doesn't have extension and is alphabetic
        return f"{ticker}.NS"  # NSE stocks
    return ticker  # Return as is for global markets

# Sidebar - Chart Parameters
st.sidebar.title("Chart Parameters")

# Market Selection
market = st.sidebar.selectbox(
    "Market",
    ["NSE (India)", "BSE (India)", "Global Markets"],
    index=0
)

# Ticker Input
ticker = st.sidebar.text_input("Ticker (e.g., RELIANCE for NSE, 500325 for BSE, AAPL for Global)")

# Time Period Dropdown
time_period = st.sidebar.selectbox(
    "Time Period",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
    index=0
)

# Chart Type Dropdown
chart_type = st.sidebar.selectbox(
    "Chart Type",
    ["Candlestick", "Line", "Area", "Bar"],
    index=0
)

# Technical Indicators Multi-select
technical_indicators = st.sidebar.multiselect(
    "Technical Indicators",
    ["Simple Moving Average (SMA)", "Exponential Moving Average (EMA)", "Bollinger Bands"],
    default=["Simple Moving Average (SMA)", "Exponential Moving Average (EMA)"]
)

# Initialize formatted_ticker as None
formatted_ticker = None

# Update Button
if st.sidebar.button("Update", key="update_chart"):
    if ticker:
        # Format ticker based on market selection
        if market == "NSE (India)":
            formatted_ticker = f"{ticker.upper()}.NS"
        elif market == "BSE (India)":
            formatted_ticker = f"{ticker}.BO"
        else:
            formatted_ticker = ticker.upper()
            
        with st.sidebar:
            with st.spinner('Fetching data...'):
                try:
                    # Get sentiment analysis results using company name without extension
                    company_name = ticker.split('.')[0]  # Remove extension for news search
                    news_articles = fetch_news(company_name)
                    
                    if news_articles:
                        sentiment_score = analyze_sentiment(news_articles)
                        sentiment_label = classify_sentiment(sentiment_score)
                        
                        # Display Price Predictions with formatted ticker
                        st.subheader("Price Predictions")
                        
                        # Daily Prediction
                        daily_result = predict_daily(formatted_ticker)
                        if daily_result:
                            current_price, predicted_price, last_date, _ = daily_result
                            st.markdown(f"""
                                **Current Price:** ₹{current_price:.2f}
                                **Daily Prediction:** ₹{predicted_price:.2f}
                                **Last Updated:** {last_date}
                            """)
                        
                        # Minute Prediction
                        minute_result = predict_minute(formatted_ticker)
                        if minute_result:
                            pred_price, pred_time = minute_result
                            st.markdown(f"""
                                **Minute Prediction:** ₹{pred_price:.2f}
                                **Predicted Time:** {pred_time.strftime('%Y-%m-%d %H:%M %p')}
                            """)
                        
                        # Hourly Prediction
                        hourly_result = predict_hourly(formatted_ticker)
                        if hourly_result:
                            st.markdown(f"**Hourly Prediction:** ₹{hourly_result:.2f}")
                        
                        # Display Sentiment Analysis
                        st.subheader("Sentiment Analysis")
                        st.markdown(f"""
                            **Sentiment Score:** {sentiment_score:.3f}
                            **Market Sentiment:** {sentiment_label}
                        """)
                        
                        # Display News Headlines
                        st.subheader("Latest News")
                        for headline in news_articles:
                            st.markdown(f"- {headline}")
                    
                except Exception as e:
                    st.error(f"Error fetching data: {str(e)}")
    else:
        st.sidebar.warning("Please enter a ticker symbol")

# Main Chart Section
st.title("📈 TradingView Chart")
if formatted_ticker:
    show_tradingview_chart(ticker=formatted_ticker, timeframe=time_period)
else:
    # Show default chart or message when no ticker is selected
    st.info("Enter a ticker symbol and click Update to view the chart")
    show_tradingview_chart(ticker="AAPL", timeframe=time_period)  # Default chart

# ...existing CSS styling code...
