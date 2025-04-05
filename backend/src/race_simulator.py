import asyncio

from dishka import Scope
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from application.race_simulate import RaceManager
from core.di.container import container


async def start_race():
    async with container(scope=Scope.REQUEST) as ioc:
        session = await ioc.get(AsyncSession)
        redis = await ioc.get(Redis)
        race_manager = RaceManager(session, redis)
        await race_manager.start_race_loop()


if __name__ == "__main__":
    asyncio.run(start_race())
