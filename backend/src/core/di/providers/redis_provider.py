import os
from collections.abc import AsyncIterable

import redis.asyncio as aioredis
from dishka import Provider, Scope, provide

from core.config import RedisConfig

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")


class RedisProvider(Provider):
    @provide(scope=Scope.SESSION, provides=aioredis.Redis)
    async def provide_redis(self, config: RedisConfig) -> AsyncIterable[aioredis.Redis]:
        redis = await aioredis.from_url(
            config.uri, encoding="utf8", decode_responses=True
        )
        try:
            yield redis
        finally:
            await redis.close()
