import numpy as np
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Fetch recent news articles for a given company
def fetch_news(company):
    try:
        newsapi = NewsApiClient(api_key='24f63e7ed5f2419dad3349ed302267f4')
        articles = newsapi.get_everything(
            q=company,
            language='en',
            sort_by='publishedAt',
            page_size=5
        )
        return [article['title'] for article in articles['articles']]
    except Exception as e:
        print(f"❌ Failed to fetch news: {e}")
        return []

# Analyze sentiment using VADER
def analyze_sentiment(news_articles):
    if not news_articles:
        return 0.0  # Neutral if no news
    analyzer = SentimentIntensityAnalyzer()
    sentiments = [analyzer.polarity_scores(article)['compound'] for article in news_articles]
    return np.mean(sentiments)

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

if __name__ == "__main__":
    # Test the functionality
    test_symbols = ["AAPL"]
    results = run_sector_ticker(test_symbols)
    print(results)
