import logging
from typing import TypedDict

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from infrastructure.db.models import Race

logger = logging.getLogger(__name__)


class RacePositions(TypedDict):
    """Типизированный словарь позиций бегунов {runner_id: position}"""
    __annotations__: dict[int, int]


class RaceReader:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def read_last_10_races(self) -> dict[int, RacePositions]:
        result = await self.session.execute(
            select(Race)
            .order_by(desc(Race.start_time))
            .limit(10)
            .options(joinedload(Race.results))
        )

        last_races = result.scalars().all()

        races_data = {}
        for race in last_races:
            positions = {
                result.runner_id: result.position
                for result in race.results
            }
            races_data[race.id] = positions

        return races_data
