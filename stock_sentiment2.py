from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(articles):
    sentiments = []
    for article in articles:
        text = article['title'] + ". " + article['description']
        sentiment = sentiment_analyzer(text)
        sentiments.append({
            'title': article['title'],
            'description': article['description'],
            'sentiment': sentiment[0]['label'],
            'score': sentiment[0]['score']
        })
    return sentiments