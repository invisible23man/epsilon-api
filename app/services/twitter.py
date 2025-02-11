import os
import tweepy
import redis
import json
from dotenv import load_dotenv
from textblob import TextBlob
from app.services.cache import cache_get, cache_set

# Load API keys
load_dotenv()
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Initialize Twitter API client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def analyze_sentiment(text):
    """
    Perform sentiment analysis on the tweet text.
    Returns 'positive', 'neutral', or 'negative'.
    """
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"


def get_mental_health_tweets():
    cache_key = "mental_health_tweets"
    cached_data = cache_get(cache_key)

    if cached_data:
        return cached_data  # ✅ Return cached data if available

    try:
        query = "#mentalhealth OR #anxiety OR #depression lang:en -is:retweet"
        tweets = client.search_recent_tweets(query=query, max_results=10, tweet_fields=["created_at", "text", "author_id"])

        if not tweets.data:
            return {"error": "No tweets found"}

        tweet_data = []
        for tweet in tweets.data:
            tweet_data.append({
                "username": f"@user_{tweet.author_id}",
                "tweet": tweet.text,
                "sentiment": analyze_sentiment(tweet.text),
                "timestamp": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        cache_set(cache_key, tweet_data)  # ✅ Cache results for 30 min
        return tweet_data

    except tweepy.TweepyException as e:
        return {"error": f"Twitter API error: {str(e)}"}

