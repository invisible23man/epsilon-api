import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

class Config:
    """Central configuration for environment variables"""

    # Twitter API
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

    # Reddit API credentials
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

    # Redis Cache
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    # Feature Flags
    ENABLE_GOOGLE_TRENDS = os.getenv("ENABLE_GOOGLE_TRENDS", "false").lower() == "true"
    ENABLE_TWITTER_TRENDS = os.getenv("ENABLE_TWITTER_TRENDS", "false").lower() == "true"
    ENABLE_REDDIT_TRENDS = os.getenv("ENABLE_REDDIT_TRENDS", "true").lower() == "true"

CONFIG = Config()
