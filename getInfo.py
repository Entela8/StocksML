from matplotlib import pyplot as plt
import requests
import yfinance as yf
import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

API_KEY = "PK7SZ5XKK9HFLRTQOXBK"
API_SECRET = "bPeyZwIPI8dDQYeJySMA6EcqjSzRQJ6eV3T1PlCy"
BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": API_SECRET,
}

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def get_stock_fluctuation(symbol, start_date, end_date):
    # Fetch historical market data from Yahoo Finance
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    
    # Check if data is empty
    if stock_data.empty:
        return f"No data found for {symbol} from {start_date} to {end_date}"
    
    # Calculate the price fluctuation
    start_price = stock_data['Close'].iloc[0]
    end_price = stock_data['Close'].iloc[-1]
    fluctuation = end_price - start_price
    fluctuation_percentage = (fluctuation / start_price) * 100
    
    return {
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date,
        "start_price": start_price,
        "end_price": end_price,
        "fluctuation": fluctuation,
        "fluctuation_percentage": fluctuation_percentage
    }

def get_stock_price_timeline(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)

    if stock_data.empty:
        return f"No data found for {symbol} from {start_date} to {end_date}"
    
    # Plotting the stock data
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data['Close'], label='Close Price')
    plt.title(f'{symbol} Stock Price from {start_date} to {end_date}')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return stock_data

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
    symbol = input("Enter stock symbol: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    get_stock_price_timeline(symbol, start_date, end_date)
    #fluctuation_data = get_stock_fluctuation(symbol, start_date, end_date)
    #print(fluctuation_data)

    fluctuation_data = get_stock_fluctuation(symbol, start_date, end_date)
    print(fluctuation_data)
      
    news_sentiment_df = get_news_sentiment(symbol)
    if isinstance(news_sentiment_df, str):
        print(news_sentiment_df)  # Print error message if news fetch failed
    else:
        print(news_sentiment_df)
