import os
import redis
import json
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")  # Default to localhost if not set
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

def cache_set(key, data, expiry=1800):  # Cache expires in 30 min
    redis_client.setex(key, expiry, json.dumps(data))

def cache_get(key):
    data = redis_client.get(key)
    return json.loads(data) if data else None
