import json
from app.redis import get_redis

def cache_key(prefix, user_id):
    return f"{prefix}:{user_id}"

async def get_cached(key):
    redis = get_redis()
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None

async def set_cached(key, data, ttl=3600):
    redis = get_redis()
    await redis.set(key, json.dumps(data), ex=ttl)


async def invalidate(*keys):
    redis = get_redis()
    for key in keys:
        await redis.delete(key)