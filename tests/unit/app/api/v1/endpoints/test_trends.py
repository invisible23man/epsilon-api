import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import CONFIG

client = TestClient(app)


@pytest.mark.skipif(not CONFIG.ENABLE_GOOGLE_TRENDS, reason="Google Trends disabled")
def test_get_google_trends():
    response = client.get("/api/v1/trends/google")
    assert response.status_code == 200
    assert "trends" in response.json().keys() 

@pytest.mark.skipif(not CONFIG.ENABLE_TWITTER_TRENDS, reason="Twitter Trends disabled")
def test_get_twitter_trends():
    response = client.get("/api/v1/trends/twitter")
    assert response.status_code == 200
    assert "tweet" in response.json()[0].keys() if response.json()[0].keys() else None
