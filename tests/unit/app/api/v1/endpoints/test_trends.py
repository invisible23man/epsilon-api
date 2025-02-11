import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_google_trends():
    response = client.get("/api/v1/trends/google")
    assert response.status_code == 200
    assert "trends" in response.json().keys() 
