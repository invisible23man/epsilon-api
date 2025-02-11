from fastapi import APIRouter
from app.services.google_trends import get_trends_data
from app.services.twitter import get_mental_health_tweets

router = APIRouter()

@router.get("/google")
def fetch_trends():
    """
    Fetch Google Trends data for mental health topics in Denmark.
    """
    return get_trends_data()


@router.get("/twitter")
def fetch_twitter_trends():
    """
    Fetch real-time Twitter mental health trends with sentiment analysis.
    """
    return {"tweets": get_mental_health_tweets()}
