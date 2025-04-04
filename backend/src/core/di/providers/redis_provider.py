import os
from collections.abc import AsyncIterable
from dataclasses import dataclass

import redis.asyncio as aioredis
from dishka import Provider, Scope, provide

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")


@dataclass(frozen=True)
class RedisConfig:
    rd_uri: str

    @staticmethod
    def from_env() -> "RedisConfig":
        uri = os.environ.get("REDIS_URI", f"redis://{REDIS_HOST}:{REDIS_PORT}")

        if not uri:
            raise RuntimeError("Missing REDIS_URI environment variable")

        return RedisConfig(uri)


class RedisProvider(Provider):
    @provide(scope=Scope.APP, provides=RedisConfig)
    def provide_redis_config(self) -> RedisConfig:
        return RedisConfig.from_env()

    @provide(scope=Scope.REQUEST, provides=aioredis.Redis)
    async def provide_redis(
        self, config: RedisConfig
    ) -> AsyncIterable[aioredis.Redis]:
        redis = await aioredis.from_url(
            config.rd_uri, encoding="utf8", decode_responses=True
        )
        try:
            yield redis
        finally:
            await redis.close()
