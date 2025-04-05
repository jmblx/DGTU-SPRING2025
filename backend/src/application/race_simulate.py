import asyncio
import json
import logging
import random
from datetime import UTC, datetime
from time import perf_counter

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.models import Runner, Race, RaceResult

DISTANCE = 100

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RaceManager:
    """Класс для управления гонками с доступом к БД и Redis"""

    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis

    def simulate_race(
        self, runners: list[Runner], time_step: float = 0.10
    ) -> list[tuple[Runner, float, list[float]]]:
        """Симуляция гонки (чистая функция, не требует доступа к БД/Redis)"""
        start_time = perf_counter()

        progress = {runner.id: [] for runner in runners}
        finished = {runner.id: False for runner in runners}
        times = {runner.id: 0.0 for runner in runners}
        distances = {runner.id: 0.0 for runner in runners}

        t = 0.0
        while not all(finished.values()):
            for runner in runners:
                if finished[runner.id]:
                    continue

                t_effective = max(0.0, t - runner.reaction_time)

                if t_effective < runner.max_speed / runner.acceleration:
                    speed = runner.acceleration * t_effective
                else:
                    time_after_accel = t_effective - (
                        runner.max_speed / runner.acceleration
                    )
                    speed = runner.max_speed * (
                        1 - runner.speed_decay * time_after_accel
                    )
                    speed = max(speed, 3.5)

                distances[runner.id] += speed * time_step

                if distances[runner.id] >= DISTANCE:
                    finished[runner.id] = True
                    distances[runner.id] = DISTANCE
                    times[runner.id] = t + random.uniform(0.001, 0.009)

                progress[runner.id].append(round(distances[runner.id], 2))

            t += time_step

        elapsed = perf_counter() - start_time
        if elapsed < 25:
            time_step = (25 - elapsed) / len(runners)
            for runner in runners:
                progress[runner.id].extend([DISTANCE] * int(time_step / 0.1))

        results = [(runner, times[runner.id], progress[runner.id]) for runner in runners]
        results.sort(key=lambda x: x[1])
        return results

    async def create_race(self, runners: list[Runner]) -> Race:
        """Создает новую гонку в БД"""
        race = Race(
            start_time=datetime.now(UTC),
        )
        self.session.add(race)
        await self.session.commit()
        logger.info(f"Created race with ID {race.id}")
        return race

    async def store_race_results(
        self, race_id: int, results: list[tuple[Runner, float, list[float]]]
    ):
        """Сохраняет результаты гонки в БД"""
        race_results = []
        for position, (runner, finish_time, progress) in enumerate(results, start=1):
            race_results.append(
                RaceResult(
                    race_id=race_id,
                    runner_id=runner.id,
                    position=position,
                    finish_time=finish_time,
                )
            )

        self.session.add_all(race_results)
        await self.session.commit()

        race = await self.session.get(Race, race_id)
        if race:
            race.end_time = datetime.now(UTC)
            await self.session.commit()
            logger.info(f"Race {race_id} results saved and end time updated")

    async def _store_race_metadata(self, race_info: dict):
        """Сохраняет метаданные гонки в Redis"""
        try:
            await self.redis.set(f"race:{race_info['id']}:meta", json.dumps(race_info))
            await self.redis.lpush("recent_races", race_info["id"])
            await self.redis.ltrim("recent_races", 0, 9)
            logger.info(f"Stored race metadata for race {race_info['id']}")
        except Exception as e:
            logger.error(f"Error storing race metadata: {e}")

    async def _store_race_results(self, race_id: int, results_data: list[dict]):
        """Сохраняет результаты гонки в Redis"""
        try:
            if results_data:
                await self.redis.set(f"race:{race_id}:results", json.dumps(results_data))
                logger.info(f"Stored results for race {race_id}")
            else:
                logger.warning(f"Attempted to store empty results for race {race_id}")
        except Exception as e:
            logger.error(f"Error storing race results: {e}")

    async def start_race_loop(self):
        """Основной цикл генерации гонок с проверкой наличия бегунов"""
        while True:
            try:
                start_loop_time = perf_counter()

                result = await self.session.execute(select(Runner))
                runners = result.scalars().all()

                if not runners:
                    logger.warning("No runners available, waiting...")
                    await asyncio.sleep(10)
                    continue

                race = await self.create_race(runners)
                await self.redis.set("current_race_id", str(race.id))

                race_info = {
                    "id": race.id,
                    "start_time": race.start_time.isoformat(),
                    "status": "running",
                    "runners": [
                        {"id": r.id, "color": r.colour, "name": f"Runner {r.id}"}
                        for r in runners
                    ],
                }

                await self._store_race_metadata(race_info)

                results = self.simulate_race(runners)
                await self.store_race_results(race.id, results)

                results_data = [
                    {"runner_id": runner.id, "time": time, "progress": progress}
                    for runner, time, progress in results
                ]
                await self._store_race_results(race.id, results_data)

                elapsed = perf_counter() - start_loop_time
                if elapsed < 25:
                    await asyncio.sleep(25 - elapsed)

            except Exception as e:
                logger.error(f"Error in race loop: {e}")
