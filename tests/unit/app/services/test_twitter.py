import pytest
from unittest.mock import call, patch, MagicMock
from app.services.twitter import analyze_sentiment, get_mental_health_tweets
from app.config import CONFIG


@patch('app.services.twitter.cache_get')
@patch('app.services.twitter.CONFIG')
@pytest.mark.skipif(not CONFIG.ENABLE_TWITTER_TRENDS, reason="Twitter API disabled")
def test_get_mental_health_tweets_returns_cached_data(mock_config, mock_cache_get):
    mock_config.ENABLE_TWITTER_TRENDS = True
    cached_data = [{"username": "@user_123", "tweet": "Test tweet", "sentiment": "positive", "timestamp": "2023-05-01 12:00:00"}]
    mock_cache_get.return_value = cached_data

    result = get_mental_health_tweets()

    assert result == cached_data
    mock_cache_get.assert_called_once_with("mental_health_tweets")

@patch('app.services.twitter.client')
@patch('app.services.twitter.analyze_sentiment')
@patch('app.services.twitter.cache_set')
@patch('app.services.twitter.cache_get')
@patch('app.services.twitter.CONFIG')
@pytest.mark.skipif(not CONFIG.ENABLE_TWITTER_TRENDS, reason="Twitter API disabled")
def test_get_mental_health_tweets_formats_data_correctly(mock_config, mock_cache_get, mock_cache_set, mock_analyze_sentiment, mock_client):
    mock_config.ENABLE_TWITTER_TRENDS = True
    mock_cache_get.return_value = None
    mock_analyze_sentiment.return_value = "positive"

    mock_tweet = MagicMock()
    mock_tweet.author_id = "123456"
    mock_tweet.text = "Test tweet about #mentalhealth"
    mock_tweet.created_at.strftime.return_value = "2023-05-01 12:00:00"

    mock_client.search_recent_tweets.return_value.data = [mock_tweet]

    result = get_mental_health_tweets()

    assert len(result) == 1
    assert result[0] == {
        "username": "@user_123456",
        "tweet": "Test tweet about #mentalhealth",
        "sentiment": "positive",
        "timestamp": "2023-05-01 12:00:00"
    }
    mock_cache_set.assert_called_once_with("mental_health_tweets", result)

@patch('app.services.twitter.client')
@patch('app.services.twitter.analyze_sentiment')
@patch('app.services.twitter.cache_get')
@patch('app.services.twitter.CONFIG')
@pytest.mark.skipif(not CONFIG.ENABLE_TWITTER_TRENDS, reason="Twitter API disabled")
def test_get_mental_health_tweets_analyzes_sentiment_correctly(mock_config, mock_cache_get, mock_analyze_sentiment, mock_client):
    mock_config.ENABLE_TWITTER_TRENDS = True
    mock_cache_get.return_value = None

    mock_tweet1 = MagicMock()
    mock_tweet1.author_id = "123"
    mock_tweet1.text = "Feeling happy today!"
    mock_tweet1.created_at.strftime.return_value = "2023-05-01 12:00:00"

    mock_tweet2 = MagicMock()
    mock_tweet2.author_id = "456"
    mock_tweet2.text = "Feeling sad today."
    mock_tweet2.created_at.strftime.return_value = "2023-05-01 13:00:00"

    mock_client.search_recent_tweets.return_value.data = [mock_tweet1, mock_tweet2]

    mock_analyze_sentiment.side_effect = ["positive", "negative"]

    result = get_mental_health_tweets()

    assert len(result) == 2
    assert result[0]["sentiment"] == "positive"
    assert result[1]["sentiment"] == "negative"
    mock_analyze_sentiment.assert_has_calls([
        call("Feeling happy today!"),
        call("Feeling sad today.")
    ])

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
