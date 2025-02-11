import redis
import json
from app.config import CONFIG

redis_client = redis.Redis(host=CONFIG.REDIS_HOST, port=CONFIG.REDIS_PORT, db=0, decode_responses=True)

def cache_set(key, data, expiry=1800):  # Cache expires in 30 min
    redis_client.setex(key, expiry, json.dumps(data))

def cache_get(key):
    data = redis_client.get(key)
    return json.loads(data) if data else None
