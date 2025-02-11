import pytest
from app.config import CONFIG
from app.services.utils.analyse import analyze_sentiment

@pytest.mark.parametrize("text, expected_sentiment", [
    ("I'm feeling great today!", "positive"),
    ("The weather is nice.", "positive"),
    ("I don't have feelings about this.", "neutral"),
    ("This is just a regular day.", "neutral"),
    ("I'm feeling sad and upset.", "negative"),
    ("This situation is really frustrating.", "negative"),
])
@pytest.mark.skipif(not CONFIG.ENABLE_TWITTER_TRENDS, reason="Twitter API disabled")
def test_analyze_sentiment(text, expected_sentiment):
    result = analyze_sentiment(text)
    assert result == expected_sentiment