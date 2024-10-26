import languagemodels as lm
from stock_data import get_stock_data, get_news
from stock_sentiment2 import analyze_sentiment
from Speak2 import Speak
import warnings
from LIST import List
from stock_prediction2 import predict_stock_price

warnings.filterwarnings("ignore", category=FutureWarning)

def ReplyBrain(input2,):
    lm.config["max_ram"] = "4gb"
    if "predict" in input2:
        while True:
            Speak("Enter the name of the company:")
            ticker = input()
            FF=List()
            try:
                ticker=ticker.lower()
                ticker=FF[ticker]
            except:
                pass
            try:
                predictions = predict_stock_price(ticker)
                return f"The predicted stock price of {ticker} is {predictions[-1][-1][0]:.2f} USD."
            except:
                Speak("Market doesn't exist.")

    elif "price" in input2:
        while True:
            Speak("Enter the name of company:")
            #ticker = input.split("price of")[-1].strip()
            ticker=input()
            FF=List()
            try:
                ticker=ticker.lower()
                ticker=FF[ticker]
            except:
                pass
            try:
                stock_info = get_stock_data(ticker)
                return f"The stock price of {ticker} is {stock_info['Close'][-1]} USD."
            except:
                Speak("Market doesn't exist.")

    elif "news" in input2:
        Speak("Enter the name of the company:")
        ticker = input()
        news_data = get_news(ticker)
        return f"Here is the latest market news: {news_data['articles'][0]['title']}"
    
    elif "analysis" in input2:
        while True:
            Speak("Enter the name of the company:")
            ticker = input()
            
            articles = get_news(ticker)
            if not articles:
                return "No news articles found."
            else:
                news=articles['articles']
            
            sentiments = analyze_sentiment(news)
            Positive=0
            Negative=0
            for i in sentiments:
                if i['sentiment']=='POSITIVE':
                    Positive=Positive+1
                if i['sentiment']=='NEGATIVE':
                    Negative=Negative+1
            if Positive > Negative:
                overall_sentiment = 'positive'
            elif Negative > Positive:
                overall_sentiment = 'negative'
            else:
                overall_sentiment = 'neutral'
            
            if overall_sentiment == 'positive':
                prediction = "Shares are likely to go up."
            elif overall_sentiment == 'negative':
                prediction = "Shares are likely to go down."
            else:
                prediction = "Shares are likely to remain stable."

            return(f"Here is the latest news for {ticker}: {articles['articles'][0]['title']}. "
                    f"The overall sentiment is {overall_sentiment}. {prediction}")
    else:
        output = lm.do(input2)
        return output
''' Market history and reports
    redirect'''