import praw
import json
from app.config import CONFIG
from app.services.cache import cache_get, cache_set
from app.services.utils.analyse import analyze_sentiment


# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=CONFIG.REDDIT_CLIENT_ID,
    client_secret=CONFIG.REDDIT_CLIENT_SECRET,
    user_agent=CONFIG.REDDIT_USER_AGENT
)

def get_mental_health_posts():
    """
    Fetch top posts from r/mentalhealth & r/depression.
    Implements caching to avoid API rate limits.
    """
    cache_key = "reddit_mental_health_posts"
    cached_data = cache_get(cache_key)

    if cached_data:
        return json.loads(cached_data)  # Return cached results

    try:
        subreddit = reddit.subreddit("mentalhealth+depression")
        posts = subreddit.hot(limit=10)  # Fetch top 10 trending posts

        post_data = []
        for post in posts:
            post_data.append({
                "title": post.title,
                "text": post.selftext,
                "upvotes": post.score,
                "sentiment": analyze_sentiment(post.selftext),
                "comments": post.num_comments,
                "url": post.url
            })

        # Store in Redis cache (expires in 30 mins)
        cache_set(cache_key, post_data)
        return post_data

    except Exception as e:
        return {"error": f"Reddit API error: {str(e)}"}
