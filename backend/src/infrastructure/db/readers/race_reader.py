import logging
from typing import TypedDict

from infrastructure.db.models import Race
from redis.asyncio import Redis
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

logger = logging.getLogger(__name__)


class RacePositions(TypedDict):
    """Типизированный словарь позиций бегунов {runner_id: position}"""

    __annotations__: dict[int, int]


class RaceReader:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis

    async def read_last_10_races(self) -> dict[int, RacePositions]:
        current_id_raw = await self.redis.get("current_streaming_id")
        if not current_id_raw:
            return {}

        try:
            current_id = int(current_id_raw)
        except ValueError:
            return {}

        race_obj = await self.session.get(Race, current_id)
        if not race_obj:
            return {}

        result = await self.session.execute(
            select(Race)
            .where(Race.start_time < race_obj.start_time)
            .order_by(desc(Race.start_time))
            .limit(10)
            .options(joinedload(Race.results))
            .execution_options(populate_existing=True)
        )

        races = result.unique().scalars().all()

        races_data: dict[int, RacePositions] = {}
        for race in races:
            positions: RacePositions = {
                result.runner_id: result.position for result in race.results
            }
            races_data[race.id] = positions

        return races_data
