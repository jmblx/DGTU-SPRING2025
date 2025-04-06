import asyncio
import json
import logging
import random

from application.race_simulate import (
    DISTANCE,
    MAX_SPEED_VARIATION,
    MIN_SPEED_VARIATION,
    RANDOMNESS_FACTOR,
)
from infrastructure.db.models import Runner
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class ProbabilityCalculatorService:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis
        self.is_running = False

    async def start(self):
        """Запускает фоновый процесс пересчета"""
        self.is_running = True
        while self.is_running:
            try:
                need_recalculate = await self.redis.get("recalculate_place_probability")
                logger.info(f"Need to recalculate probabilities: {need_recalculate}")

                if need_recalculate in ("1", "true", "True", 1):
                    logger.info("Starting probability recalculation...")

                    await self.redis.set("recalculate_place_probability", "0")

                    runners = await self._get_current_runners()

                    if runners:
                        probabilities = await self._calculate_probabilities(runners)

                        await self.redis.set(
                            "place_probability_cache", json.dumps(probabilities), ex=3600
                        )
                        logger.info("Probabilities updated in cache")

                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error(f"Error in calculator service: {e}")
                await asyncio.sleep(1)

    async def stop(self):
        """Останавливает сервис"""
        self.is_running = False

    async def _get_current_runners(self) -> list[Runner]:
        """Получает актуальный список бегунов"""
        self.session.expire_all()
        result = await self.session.execute(select(Runner))
        return result.scalars().all()

    async def _calculate_probabilities(
        self, runners: list[Runner], n_simulations: int = 5000
    ) -> dict[int, dict[int, float]]:
        """Вычисляет вероятности занятых мест"""
        position_counts = {runner.id: [0] * len(runners) for runner in runners}

        for _ in range(n_simulations):
            results = self._simulate_race(runners)
            for pos, (runner, _) in enumerate(results, start=1):
                position_counts[runner.id][pos - 1] += 1

        return {
            runner_id: {
                pos + 1: count / n_simulations for pos, count in enumerate(counts)
            }
            for runner_id, counts in position_counts.items()
        }

    def _simulate_race(self, runners: list[Runner]) -> list[tuple[Runner, float]]:
        """Быстрая симуляция одной гонки"""
        times = []
        for runner in runners:
            accel_time = runner.max_speed / runner.acceleration
            accel_dist = 0.5 * runner.acceleration * accel_time**2
            remaining_dist = max(0, DISTANCE - accel_dist)
            decay_time = remaining_dist / runner.max_speed

            # Добавляем случайность
            total_time = (
                (runner.reaction_time + accel_time + decay_time)
                * random.uniform(MIN_SPEED_VARIATION, MAX_SPEED_VARIATION)
                * (1 + (random.random() - 0.5) * RANDOMNESS_FACTOR)
            )

            times.append((runner, total_time))

        return sorted(times, key=lambda x: x[1])
