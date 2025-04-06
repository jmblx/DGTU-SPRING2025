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

    async def read_last_10_races(self) -> dict[int, RacePositions]:
        """Возвращает данные в формате TypedDict"""
        result = await self.session.execute(
            select(Race)
            .order_by(desc(Race.start_time))
            .limit(10)
            .options(joinedload(Race.results))
            .execution_options(populate_existing=True)
        )

        # Добавляем .unique() для корректной обработки joinedload
        last_races = result.unique().scalars().all()

        races_data: Dict[int, RacePositions] = {}
        for race in last_races:
            positions: RacePositions = {
                result.runner_id: result.position for result in race.results
            }
            races_data[race.id] = positions

        return races_data
