import streamlit as st
from Prediction import predict_next_price
from Hourly_stock_predictor import predict_stock_price as predict_hourly
from minute_prediction import predict_stock_price as predict_minute
from sentiment_analysis import fetch_news, analyze_sentiment, classify_sentiment
from datetime import datetime

st.set_page_config(page_title="📈 Full Stock Report", layout="centered")
st.title("📊 L&M's Automated Stock Report Generator")

stock_symbol = st.text_input("Enter NSE Stock Symbol (e.g., TCS.NS)", "TCS.NS").upper()

if st.button("Analyze"):
    with st.spinner("Generating report..."):

        # 1. Real-Time Prediction
        try:
            current_price, predicted_price_rt, time_rt = predict_next_price(stock_symbol)
            if predicted_price_rt:
                st.subheader("📈 Real-Time Prediction")
                st.markdown(f"**Current Price:** ₹{current_price:.2f}")
                st.markdown(f"**Predicted Price (next min):** ₹{predicted_price_rt:.2f}")
                st.markdown(f"**Prediction Time (IST):** {time_rt.strftime('%Y-%m-%d %H:%M %p')}")
            else:
                st.warning("Real-time prediction not available. Possibly due to market closure or insufficient data.")
        except Exception as e:
            st.error(f"Real-time prediction failed: {e}")

        # 2. Hourly Prediction
        try:
            price_hourly = predict_hourly(stock_symbol)
            st.subheader("⏰ Hourly Prediction")
            st.markdown(f"**Predicted Next Hour Price:** ₹{price_hourly:.2f}")
        except Exception as e:
            st.error(f"Hourly prediction failed: {e}")

        # 3. Minute-Level Prediction
        try:
            price_minute, time_minute = predict_minute(stock_symbol)
            st.subheader("🕒 Minute-Level Prediction")
            st.markdown(f"**Predicted Price:** ₹{price_minute:.2f} at {time_minute.strftime('%H:%M %p')}")
        except Exception as e:
            st.error(f"Minute prediction failed: {e}")

        # 4. Sentiment Analysis
        try:
            news = fetch_news(stock_symbol)
            sentiment_score = analyze_sentiment(news)
            sentiment_label = classify_sentiment(sentiment_score)

            st.subheader("📰 News & Sentiment Analysis")
            if news:
                st.markdown("**Latest Headlines:**")
                for i, headline in enumerate(news, 1):
                    st.markdown(f"{i}. {headline}")
            else:
                st.info("No recent news found.")

            st.markdown(f"**Sentiment Score:** `{sentiment_score:.3f}`")
            st.markdown(f"**Overall Sentiment:** {sentiment_label}")
        except Exception as e:
            st.error(f"Sentiment analysis failed: {e}")
