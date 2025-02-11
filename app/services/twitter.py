import os
import tweepy
import redis
import json
from dotenv import load_dotenv
from textblob import TextBlob

# Load API keys
load_dotenv()
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Set up Redis cache
# redis_client = redis.Redis(host="localhost", port=6379, db=0)

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
    """
    Fetch real-time tweets related to mental health topics.
    Implements caching to avoid API rate limits.
    """
    # cache_key = "mental_health_tweets"
    # cached_data = redis_client.get(cache_key)

    # if cached_data:
    #     return json.loads(cached_data)  # Return cached results

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

        # Store in Redis cache (expires in 30 mins)
        # redis_client.setex(cache_key, 1800, json.dumps(tweet_data))
        return tweet_data

    except tweepy.TweepyException as e:
        return {"error": f"Twitter API error: {str(e)}"}
