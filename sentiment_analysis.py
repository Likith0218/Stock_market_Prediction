from newsapi import NewsApiClient
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Fetch recent news articles for a given company
def fetch_news(company):
    try:
        newsapi = NewsApiClient(api_key='24f63e7ed5f2419dad3349ed302267f4')  # Replace with your own key
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

# Classify sentiment score into labels
def classify_sentiment(score):
    if score >= 0.05:
        return "Bullish 📈"
    elif score <= -0.05:
        return "Bearish 📉"
    else:
        return "Neutral ➖"

# Example usage
if __name__ == "__main__":
    company = "TCS"
    news_articles = fetch_news(company)

    print(f"\n📰 Latest headlines for {company}:\n")
    for i, headline in enumerate(news_articles, 1):
        print(f"{i}. {headline}")

    sentiment_score = analyze_sentiment(news_articles)
    sentiment_label = classify_sentiment(sentiment_score)

    print(f"\n📊 Sentiment score: {sentiment_score:.3f}")
    print(f"🔎 Sentiment label: {sentiment_label}")
