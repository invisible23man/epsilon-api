import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_trends():
    response = client.get("/api/v1/trends/")
    assert response.status_code == 200
    assert response.json() == {"message": "Google Trends API data coming soon!"}
