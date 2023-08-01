from redis import asyncio as aioredis

from src.config import settings


class RedisCache:
    __redis_connect = aioredis.from_url(settings.REDIS_URL)

    @classmethod
    def get_key(cls, key: str):
        return cls.__redis_connect.get(key)

    @classmethod
    def set_key(cls, key: str, value):
        return cls.__redis_connect.set(key, value)


cache = RedisCache()
