import json
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
        self.cache_key = "last_10_races_cache"

    async def read_last_10_races(self) -> dict[int, RacePositions]:
        cached_data = await self._get_from_cache()
        if cached_data is not None:
            return cached_data

        races_data = await self._load_from_db()

        await self._save_to_cache(races_data)

        return races_data

    async def _get_from_cache(self) -> dict[int, RacePositions] | None:
        """Пытается получить данные из Redis кэша"""
        try:
            cached_data = await self.redis.get(self.cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            logger.error(f"Error reading from cache: {e}")
        return None

    async def _save_to_cache(self, data: dict[int, RacePositions]):
        """Сохраняет данные в Redis кэш"""
        try:
            await self.redis.set(
                self.cache_key,
                json.dumps(data),
                ex=3600  # TTL 1 час
            )
        except Exception as e:
            logger.error(f"Error saving to cache: {e}")

    async def _load_from_db(self) -> dict[int, RacePositions]:
        """Загружает данные из базы данных"""
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

    async def invalidate_cache(self):
        """Сбрасывает кэш (вызывать при добавлении нового забега)"""
        try:
            await self.redis.delete(self.cache_key)
            logger.info("Race cache invalidated")
        except Exception as e:
            logger.error(f"Error invalidating cache: {e}")
