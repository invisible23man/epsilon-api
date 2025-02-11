from fastapi import APIRouter
from app.services.trends import get_trends_data

router = APIRouter()

@router.get("/")
def fetch_trends():
    """
    Fetch Google Trends data for mental health topics in Denmark.
    """
    return get_trends_data()
