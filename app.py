import streamlit as st
import streamlit.components.v1 as components
from Prediction import predict_end_of_day_price
from Hourly_stock_predictor import predict_stock_price as predict_hourly
from minute_prediction import predict_stock_price as predict_minute
from sentiment_analysis import fetch_news, analyze_sentiment, classify_sentiment
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf

# External CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# External JS
with open("script.js") as f:
    js_code = f"<script>{f.read()}</script>"
components.html(js_code, height=0)

# Session state to track whether Analyze was clicked
if "analyze_clicked" not in st.session_state:
    st.session_state.analyze_clicked = False

# Header
st.markdown('<div class="sticky-header"><div class="title">📈 L&M Stock Dashboard</div></div>', unsafe_allow_html=True)
st.markdown('<div class="typing-text"></div>', unsafe_allow_html=True)

# Input
stock_symbol = st.text_input("🔍 Enter NSE Stock Symbol (e.g., TCS.NS)", "TCS.NS").upper()

# Handle Refresh from button below the chart
if st.session_state.get("do_refresh", False):
    st.experimental_rerun()

# Analyze button
if st.button("🔎 Analyze"):
    st.session_state.analyze_clicked = True

if st.session_state.analyze_clicked:
    with st.spinner("🔄 Generating your stock report..."):

        # DAILY PREDICTION
        try:
            current_price, predicted_price_eod, last_date, price_history = predict_end_of_day_price(stock_symbol)
            if predicted_price_eod:
                st.markdown('<div class="report-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">📅 End-of-Day Prediction</div>', unsafe_allow_html=True)
                st.markdown(f"**Last Trading Day:** {last_date}")
                st.markdown(f"**Current Price:** ₹{current_price:.2f}")
                st.markdown(f"**Predicted Closing Price (Next Day):** ₹{predicted_price_eod:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

                # INTERACTIVE CHART
                st.markdown('<div class="report-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">📊 Interactive Price Chart</div>', unsafe_allow_html=True)

                chart_type = st.selectbox("Chart Style", ["Line Chart", "Candlestick Chart"])

                fig = go.Figure()

                if chart_type == "Candlestick Chart":
                    ohlc_data = yf.download(stock_symbol, period="90d", interval="1d", progress=False)
                    fig.add_trace(go.Candlestick(
                        x=ohlc_data.index,
                        open=ohlc_data['Open'],
                        high=ohlc_data['High'],
                        low=ohlc_data['Low'],
                        close=ohlc_data['Close'],
                        name="Candlestick"
                    ))
                else:
                    fig.add_trace(go.Scatter(
                        x=price_history.index,
                        y=price_history.values,
                        mode='lines+markers',
                        name='Close Price',
                        line=dict(color='deepskyblue', width=2)
                    ))

                # Predicted point
                future_date = pd.to_datetime(price_history.index[-1]) + pd.Timedelta(days=1)
                fig.add_trace(go.Scatter(
                    x=[future_date],
                    y=[predicted_price_eod],
                    mode='markers+text',
                    name='Predicted EOD',
                    marker=dict(color='lime', size=12, symbol='star'),
                    text=["Predicted"],
                    textposition="top center"
                ))

                fig.update_layout(
                    template="plotly_dark",
                    title=f"{stock_symbol} Historical Prices with Prediction",
                    xaxis_title="Date",
                    yaxis_title="Price (₹)",
                    legend=dict(orientation="h", y=1.1),
                    hovermode="x unified",
                    dragmode="pan",
                    height=500
                )

                fig.update_xaxes(showgrid=False, rangeslider_visible=False)
                fig.update_yaxes(showgrid=True, gridcolor='#333')

                st.plotly_chart(fig, use_container_width=True)

                # REFRESH BUTTON — SHOWN ONLY NOW
                if st.button("🔄 Refresh Chart"):
                    st.session_state.do_refresh = True  # Trigger rerun

                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.warning("⚠️ Not enough data for daily prediction.")
        except Exception as e:
            st.error(f"❌ Daily prediction failed: {e}")

        # HOURLY PREDICTION
        try:
            price_hourly = predict_hourly(stock_symbol)
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">⏰ Hourly Prediction</div>', unsafe_allow_html=True)
            st.markdown(f"**Next Hour Price:** ₹{price_hourly:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Hourly prediction failed: {e}")

        # MINUTE PREDICTION
        try:
            price_minute, time_minute = predict_minute(stock_symbol)
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🕒 Minute-Level Prediction</div>', unsafe_allow_html=True)
            st.markdown(f"**Price:** ₹{price_minute:.2f} at {time_minute.strftime('%H:%M %p')}")
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Minute prediction failed: {e}")

        # SENTIMENT ANALYSIS
        try:
            news = fetch_news(stock_symbol)
            sentiment_score = analyze_sentiment(news)
            sentiment_label = classify_sentiment(sentiment_score)
            color = "🟢" if sentiment_score >= 0.05 else "🔴" if sentiment_score <= -0.05 else "🟡"

            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📰 Sentiment Analysis</div>', unsafe_allow_html=True)
            st.markdown(f"**Score:** `{sentiment_score:.3f}`")
            st.markdown(f"**Overall Sentiment:** {color} {sentiment_label}")
            if news:
                for i, headline in enumerate(news, 1):
                    st.markdown(f"**{i}.** {headline}")
            else:
                st.info("No news found.")
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Sentiment analysis failed: {e}")

# FOOTER
st.markdown('<div class="footer">© 2025 L&M Trading Desk | Built with ❤️ using Streamlit & Plotly</div>', unsafe_allow_html=True)
