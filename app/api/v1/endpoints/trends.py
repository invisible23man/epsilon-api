from fastapi import APIRouter
from app.services.google_trends import get_trends_data
from app.services.twitter import get_mental_health_tweets
from app.config import CONFIG

router = APIRouter()

if CONFIG.ENABLE_GOOGLE_TRENDS:
    @router.get("/google")
    def fetch_trends():
        """Fetch Google Trends data (if enabled)."""
        return get_trends_data()

if CONFIG.ENABLE_TWITTER_TRENDS:
    @router.get("/twitter")
    def fetch_twitter_trends():
        """Fetch Twitter mental health trends (if enabled)."""
        return get_mental_health_tweets()
