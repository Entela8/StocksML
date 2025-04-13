from matplotlib import pyplot as plt
import requests
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import date
import json
import sys

API_KEY = "PK7SZ5XKK9HFLRTQOXBK"
API_SECRET = "bPeyZwIPI8dDQYeJySMA6EcqjSzRQJ6eV3T1PlCy"
BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": API_SECRET,
}

def fetch_stock_news(symbol):
    url = f'https://data.alpaca.markets/v1beta1/news?symbols={symbol}'
    headers = {
        "APCA-API-KEY-ID": ALPACA_CREDS["APCA-API-KEY-ID"],
        "APCA-API-SECRET-KEY": ALPACA_CREDS["APCA-API-SECRET-KEY"]
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Failed to fetch news: {response.status_code}"
    
    news_data = response.json()
    return news_data['news']

def analyze_sentiment_textblob(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def analyze_sentiment_vader(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    return score['compound']

def get_news_sentiment(symbol):
    news_articles = fetch_stock_news(symbol)
    if isinstance(news_articles, str):
        return news_articles  # Return error message if news fetch failed
    
    news_df = pd.DataFrame(news_articles)
    if news_df.empty:
        return f"No news found for {symbol}"
    
    # Ensure content is available and not just headlines
    news_df['content'] = news_df['summary']
    
    # Analyze sentiment
    news_df['textblob_sentiment'] = news_df['content'].apply(analyze_sentiment_textblob)
    news_df['vader_sentiment'] = news_df['content'].apply(analyze_sentiment_vader)
    
    return news_df[['headline', 'content', 'textblob_sentiment', 'vader_sentiment']]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
        symbol = data.get("stockName")
        if not symbol:
            raise ValueError("Missing 'stockName' in input")

        result = get_news_sentiment(symbol)
        # ⚠️ NE PAS METTRE DE PRINT NON JSON
        if isinstance(result, str):
            print(result)  # Print error message if news fetch failed
        else:
            print(json.dumps(result.to_dict(orient="records")))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

