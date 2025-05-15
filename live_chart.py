import streamlit.components.v1 as components

def show_tradingview_chart(ticker=None, timeframe='1d', chart_type='Candlestick'):
    # Map chart types to TradingView values
    chart_styles = {
        'Candlestick': '1',
        'Line': '2',
        'Area': '3',
        'Bar': '0'
    }
    
    # Format exchange prefix for Indian markets
    if ticker:
        if '.NS' in ticker:
            # NSE stocks use NSEI prefix
            symbol = ticker.replace('.NS', '')
            ticker = f"NSEI:{symbol}"
        elif '.BO' in ticker:
            # BSE stocks use BSE prefix
            symbol = ticker.replace('.BO', '')
            ticker = f"BSE:{symbol}"
        else:
            # Global markets
            ticker = f"{ticker}"
    else:
        # Default to NIFTY 50 index
        ticker = "NSEI:NIFTY50"

    components.html(
        f"""
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
            <div id="tradingview_chart"></div>
            <div class="tradingview-widget-copyright">
                <a href="https://www.tradingview.com/symbols/{ticker}/" rel="noopener" target="_blank">
                    <span class="blue-text">{ticker} Chart</span>
                </a>
            </div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
            new TradingView.widget(
            {{
                "width": "100%",
                "height": 600,
                "symbol": "{ticker}",
                "interval": "D",
                "timezone": "Asia/Kolkata",
                "theme": "dark",
                "style": "{chart_styles.get(chart_type, '1')}",
                "locale": "in",
                "toolbar_bg": "#f1f3f6",
                "enable_publishing": false,
                "hide_side_toolbar": false,
                "allow_symbol_change": true,
                "details": true,
                "calendar": true,
                "studies": [
                    "MASimple@tv-basicstudies",
                    "MAExp@tv-basicstudies",
                    "BB@tv-basicstudies"
                ],
                "container_id": "tradingview_chart",
                "show_popup_button": false,
                "range": "{timeframe}",
                "save_image": true,
                "referral_id": "10107"
            }});
            </script>
        </div>
        <!-- TradingView Widget END -->
        """,
        height=650,
    )
