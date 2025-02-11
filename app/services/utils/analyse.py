from textblob import TextBlob
def analyze_sentiment(text):
    """
    Perform sentiment analysis on post text.
    Returns 'positive', 'neutral', or 'negative'.
    """
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"