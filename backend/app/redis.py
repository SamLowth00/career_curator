import os

from redis.asyncio import from_url

redis_client = None

async def init_redis():
    global redis_client
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_client = from_url(redis_url, decode_responses=True)

async def get_redis():
    global redis_client
    if redis_client is None:
        await init_redis()
    return redis_client


async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()


def get_redis():
    return redis_client