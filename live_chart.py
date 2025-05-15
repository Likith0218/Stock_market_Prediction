# tradingview_chart.py

import streamlit as st
import streamlit.components.v1 as components

def show_tradingview_chart(ticker=None, timeframe='1d'):
    st.subheader("📈 TradingView Chart Integration")

    ticker = st.text_input("Enter Stock Ticker (e.g., NSE:TCS, NASDAQ:AAPL)", value="NSE:TCS")

    components.html(
        f"""
        <div class="tradingview-widget-container">
            <div id="tradingview_chart"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
            new TradingView.widget(
            {{
                "width": "100%",
                "height": 610,
                "symbol": "{ticker if ticker else 'AAPL'}",
                "interval": "D",
                "timezone": "Asia/Kolkata",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "#f1f3f6",
                "enable_publishing": false,
                "range": "{timeframe}",
                "allow_symbol_change": true,
                "container_id": "tradingview_chart"
            }});
            </script>
        </div>
        """,
        height=610,
    )
