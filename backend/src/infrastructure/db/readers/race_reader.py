import logging
from typing import TypedDict

from infrastructure.db.models import Race
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

logger = logging.getLogger(__name__)


class RacePositions(TypedDict):
    """Типизированный словарь позиций бегунов {runner_id: position}"""

    __annotations__: dict[int, int]


class RaceReader:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def read_last_10_races(self, last_race_id: int) -> dict[int, RacePositions]:
        """
        Возвращает данные в формате TypedDict:
        10 гонок, которые были до указанной, исключая её саму.
        """
        race_obj = await self.session.get(Race, last_race_id)
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
