import yfinance as yf
import requests
import numpy as np
from stock_sentiment2 import analyze_sentiment
from sklearn.preprocessing import MinMaxScaler
from Speak2 import Speak

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period='5y')
    return hist

def get_news(query):
    try:
        api_key = 'bf61697e90eeab1eec4489b3213f7ead'
        url = f'https://gnews.io/api/v4/search?q={query}&token={api_key}&lang=en'
        response = requests.get(url , timeout=10)
        return response.json()
    except:
        Speak("Can't Connect , Bad network!!")

def preprocess_data(stock_data, sentiments):
    stock_data = stock_data[['Close']]
    scaler = MinMaxScaler(feature_range=(0, 1))
    stock_data_scaled = scaler.fit_transform(stock_data)
    sentiment_scores = np.array([sent['score'] for sent in sentiments])
    sentiment_scores = sentiment_scores.reshape(-1, 1)
    dataset = np.hstack((stock_data_scaled, sentiment_scores))
    X, y = [], []
    for i in range(60, len(dataset)):
        X.append(dataset[i-60:i])
        y.append(dataset[i, 0])   
    return np.array(X), np.array(y), scaler

def get_news_sentiment(company):
    news_data = get_news(company)
    return analyze_sentiment(news_data['articles'])