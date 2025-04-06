import asyncio
import logging

from application.calculate_probabilities import ProbabilityCalculatorService
from core.di.container import container
from dishka import Scope
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def calc_probabilities():
    async with container(scope=Scope.REQUEST) as ioc:
        session = await ioc.get(AsyncSession)
        redis = await ioc.get(Redis)
        race_manager = ProbabilityCalculatorService(session, redis)
        await race_manager.start()


if __name__ == "__main__":
    asyncio.run(calc_probabilities())
