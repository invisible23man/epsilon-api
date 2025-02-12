import time
import random
from pytrends.request import TrendReq
from datetime import datetime
from fastapi import HTTPException
from app.config import CONFIG


# Initialize Google Trends API
pytrends = TrendReq(
    hl="da-DK",
    tz=360,
    # timeout=(10, 25),
    # proxies=[
    #     "https://34.203.233.13:80",
    # ],
    # retries=2,
    # backoff_factor=0.1,
    # requests_args={"verify": False},
)


def get_trends_data(search_terms=["mental health", "anxiety", "depression"]):
    """
    Fetches Google Trends data for given search terms in Denmark.
    """
    try:
        if not CONFIG.ENABLE_GOOGLE_TRENDS:
            return {"error": "Google Trends API is disabled in configuration."}

        # Set region-specific parameters (Denmark)
        pytrends.build_payload(kw_list=search_terms, timeframe="now 7-d", geo="DK")
        # Fetch interest over time
        trends_data = pytrends.interest_over_time()

        if trends_data.empty:
            raise HTTPException(status_code=404, detail="No trends data found")

        # Convert trends data to dictionary format
        response = {
            "timestamp": datetime.utcnow().isoformat(),
            "trends": trends_data.drop(columns=["isPartial"]).to_dict(orient="records"),
        }

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching trends data: {str(e)}"
        )
