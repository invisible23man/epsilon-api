from urllib.parse import urlparse
import redis
import json
from app.config import CONFIG

parsed_redis_url = urlparse(CONFIG.REDIS_URL)

redis_client = redis.Redis(
    host=parsed_redis_url.hostname,
    port=parsed_redis_url.port,
    password=parsed_redis_url.password,
    decode_responses=True
)

def cache_set(key, data, expiry=1800):  # Cache expires in 30 min
    redis_client.setex(key, expiry, json.dumps(data))

def cache_get(key):
    data = redis_client.get(key)
    return json.loads(data) if data else None
