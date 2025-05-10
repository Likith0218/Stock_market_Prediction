import numpy as np
from sentiment_analysis import fetch_news, analyze_sentiment  # Your existing functions

# Classify sentiment
def classify_sentiment(score):
    if score >= 0.05:
        return "Bullish 📈"
    elif score <= -0.05:
        return "Bearish 📉"
    else:
        return "Neutral ➖"

# Predict stock price (dummy function for sector analysis)
def predict_stock_price(symbol):
    # Replace this with your actual prediction logic if needed
    return 1000.0, 1020.0  # Example: current price and predicted price

# Main function to analyze user-selected stocks
def run_sector_ticker(stock_symbols):
    results = []

    for company in stock_symbols:
        # Stock price prediction
        current_price, predicted_price = predict_stock_price(company)

        # News sentiment
        news_articles = fetch_news(company)
        sentiment_score = analyze_sentiment(news_articles)
        sentiment_label = classify_sentiment(sentiment_score)

        # Append results for each company
        results.append({
            "company": company,
            "current_price": current_price,
            "predicted_price": predicted_price,
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label,
            "news": news_articles
        })

    return results