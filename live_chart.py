# tradingview_chart.py

import streamlit as st
import streamlit.components.v1 as components

def show_tradingview_chart():
    st.subheader("📈 TradingView Chart Integration")

    ticker = st.text_input("Enter Stock Ticker (e.g., NSE:TCS, NASDAQ:AAPL)", value="NSE:TCS")

    chart_html = f"""
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "width": "100%",
        "height": 600,
        "symbol": "{ticker}",
        "interval": "1",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_chart"
      }});
      </script>
    </div>
    """

    components.html(chart_html, height=620)
