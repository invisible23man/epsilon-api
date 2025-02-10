import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_insights():
    response = client.get("/api/v1/insights/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI-driven mental health insights coming soon!"}
