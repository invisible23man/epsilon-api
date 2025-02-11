import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.endpoints.auth import SECRET_KEY
import jwt
from datetime import datetime, timedelta, timezone

client = TestClient(app)


def test_login():
    response = client.post("/api/v1/auth/login")
    assert response.status_code == 200
    assert "access_token" in response.json()
    
    token = response.json()["access_token"]
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    
    assert "exp" in decoded_token
    # Convert timestamp to timezone-aware datetime
    expiration_time = datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)
    assert expiration_time > datetime.now(timezone.utc)
    # Allow 5-second execution margin to avoid precision issues
    assert expiration_time <= datetime.now(timezone.utc) + timedelta(days=1, seconds=5)

def test_protected_route_valid_token():
    # Generate a valid token
    expiration = datetime.now(timezone.utc) + timedelta(days=1)
    valid_token = jwt.encode({"exp": expiration}, SECRET_KEY, algorithm="HS256")

    # Make a request to the protected route with the valid token
    response = client.get("/api/v1/auth/protected", headers={"Authorization": f"Bearer {valid_token}"})

    # Assert the response
    assert response.status_code == 200
    assert response.json()["message"] == "Valid token!"
    assert "exp" in response.json()

def test_protected_route_expired_token():
    # Generate an expired token
    expiration = datetime.now(timezone.utc) - timedelta(days=1)
    expired_token = jwt.encode({"exp": expiration}, SECRET_KEY, algorithm="HS256")

    # Make a request to the protected route with the expired token
    response = client.get("/api/v1/auth/protected", headers={"Authorization": f"Bearer {expired_token}"})

    # Assert the response
    assert response.status_code == 401
    assert response.json()["detail"] == "Token expired"

def test_protected_route_invalid_token():
    # Generate an invalid token
    invalid_token = "invalid_token_string"

    # Make a request to the protected route with the invalid token
    response = client.get("/api/v1/auth/protected", headers={"Authorization": f"Bearer {invalid_token}"})

    # Assert the response
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"
