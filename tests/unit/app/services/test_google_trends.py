import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from fastapi import HTTPException
from app.services.google_trends import get_trends_data
from app.config import CONFIG

@pytest.fixture
def mock_pytrends():
    with patch('app.services.google_trends.pytrends') as mock:
        yield mock



@pytest.mark.skipif(not CONFIG.ENABLE_GOOGLE_TRENDS, reason="Google Trends disabled")
def test_get_trends_data_success(mock_pytrends):
    mock_trends_data = MagicMock()
    mock_trends_data.empty = False
    mock_trends_data.drop.return_value.to_dict.return_value = [
        {"date": "2023-05-01", "mental health": 75, "anxiety": 60, "depression": 50},
        {"date": "2023-05-02", "mental health": 80, "anxiety": 65, "depression": 55},
    ]
    mock_pytrends.interest_over_time.return_value = mock_trends_data

    result = get_trends_data()

    assert "timestamp" in result
    assert "trends" in result
    assert isinstance(result["timestamp"], str)
    assert isinstance(result["trends"], list)
    assert len(result["trends"]) == 2
    assert all(key in result["trends"][0] for key in ["date", "mental health", "anxiety", "depression"])
    mock_pytrends.build_payload.assert_called_once_with(
        kw_list=["mental health", "anxiety", "depression"],
        timeframe="now 7-d",
        geo="DK"
    )
    mock_pytrends.interest_over_time.assert_called_once()
