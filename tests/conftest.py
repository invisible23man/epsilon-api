import pytest
from unittest.mock import MagicMock
from app.services.cache import redis_client

@pytest.fixture(autouse=True)
def mock_redis_cache():
    redis_client.get = MagicMock(return_value=None)
    redis_client.setex = MagicMock(return_value=True)
