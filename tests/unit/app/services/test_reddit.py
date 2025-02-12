
import pytest
from unittest.mock import patch, MagicMock
from app.services.reddit import get_mental_health_posts
from app.config import CONFIG

@pytest.fixture
def mock_dependencies():
    with patch('app.services.reddit.reddit.subreddit') as mock_subreddit, \
         patch('app.services.reddit.cache_get') as mock_cache_get, \
         patch('app.services.reddit.cache_set') as mock_cache_set, \
         patch('app.services.reddit.analyze_sentiment') as mock_analyze_sentiment:
        
        mock_cache_get.return_value = None
        mock_analyze_sentiment.return_value = 'Neutral'
        
        mock_post = MagicMock()
        mock_post.title = 'Test Title'
        mock_post.selftext = 'Test Text'
        mock_post.score = 100
        mock_post.num_comments = 50
        mock_post.url = 'https://reddit.com/test'
        
        mock_subreddit.return_value.hot.return_value = [mock_post]
        
        yield {
            'mock_subreddit': mock_subreddit,
            'mock_cache_get': mock_cache_get,
            'mock_cache_set': mock_cache_set,
            'mock_analyze_sentiment': mock_analyze_sentiment
        }
@pytest.mark.skipif(not CONFIG.ENABLE_REDDIT_TRENDS, reason="Reddit API disabled")
def test_get_mental_health_posts_details(mock_dependencies):
    result = get_mental_health_posts()
    
    assert len(result) == 1
    post = result[0]
    assert post['title'] == 'Test Title'
    assert post['text'] == 'Test Text'
    assert post['upvotes'] == 100
    assert post['sentiment'] == 'Neutral'
    assert post['comments'] == 50
    assert post['url'] == 'https://reddit.com/test'
    
    mock_dependencies['mock_cache_set'].assert_called_once()
