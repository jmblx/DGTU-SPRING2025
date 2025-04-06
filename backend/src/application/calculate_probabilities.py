import asyncio
import json
import logging
import random
from typing import Dict, Tuple, List
from collections import defaultdict

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.race_simulate import MIN_SPEED_VARIATION, MAX_SPEED_VARIATION, RANDOMNESS_FACTOR, DISTANCE
from infrastructure.db.models import Runner

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

                if need_recalculate in ("1", "true", "True", 1):
                    await self.redis.set("recalculate_place_probability", "0")

                    runners = await self._get_current_runners()
                    if not runners:
                        continue

                    probabilities = await self._calculate_all_probabilities(runners)

                    await self._store_probabilities(probabilities)
                    logger.info("All probabilities updated in cache")

                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error(f"Error in calculator service: {e}")
                await asyncio.sleep(1)

    async def _calculate_all_probabilities(self, runners: List[Runner], n_simulations: int = 5000) -> Dict[str, Dict]:
        """Вычисляет все типы вероятностей, включая матрицу пар 1-2 мест"""
        runner_ids = [runner.id for runner in runners]

        position_counts = {runner_id: [0] * len(runners) for runner_id in runner_ids}
        top2_counts = {runner_id: 0 for runner_id in runner_ids}
        top3_counts = {runner_id: 0 for runner_id in runner_ids}
        pair_matrix = {i: {j: 0 for j in runner_ids if j != i} for i in runner_ids}  # Матрица без диагонали

        for _ in range(n_simulations):
            results = self._simulate_race(runners)

            for pos, (runner, _) in enumerate(results, start=1):
                position_counts[runner.id][pos - 1] += 1

                if pos <= 2:
                    top2_counts[runner.id] += 1
                if pos <= 3:
                    top3_counts[runner.id] += 1

            # Заполняем матрицу пар
            if len(results) >= 2:
                first, second = results[0][0].id, results[1][0].id
                pair_matrix[first][second] += 1

        return {
            "position_probabilities": {
                runner_id: {
                    pos + 1: count / n_simulations
                    for pos, count in enumerate(counts)
                }
                for runner_id, counts in position_counts.items()
            },
            "top2_probabilities": {
                runner_id: count / n_simulations
                for runner_id, count in top2_counts.items()
            },
            "top3_probabilities": {
                runner_id: count / n_simulations
                for runner_id, count in top3_counts.items()
            },
            "pair_matrix": {
                first: {
                    second: count / n_simulations
                    for second, count in seconds.items()
                }
                for first, seconds in pair_matrix.items()
            }
        }

    async def _store_probabilities(self, probabilities: Dict[str, Dict]):
        """Сохраняет все данные в Redis"""
        await asyncio.gather(
            self.redis.set("position_probability_cache", json.dumps(probabilities["position_probabilities"]), ex=3600),
            self.redis.set("top2_probability_cache", json.dumps(probabilities["top2_probabilities"]), ex=3600),
            self.redis.set("top3_probability_cache", json.dumps(probabilities["top3_probabilities"]), ex=3600),
            self.redis.set("pair_matrix_cache", json.dumps(probabilities["pair_matrix"]), ex=3600)
        )

    async def stop(self):
        self.is_running = False

    async def _get_current_runners(self) -> List[Runner]:
        self.session.expire_all()
        result = await self.session.execute(select(Runner))
        return result.scalars().all()

    def _simulate_race(self, runners: List[Runner]) -> List[Tuple[Runner, float]]:
        times = []
        for runner in runners:
            accel_time = runner.max_speed / runner.acceleration
            accel_dist = 0.5 * runner.acceleration * accel_time ** 2
            remaining_dist = max(0, DISTANCE - accel_dist)
            decay_time = remaining_dist / runner.max_speed

            total_time = (runner.reaction_time + accel_time + decay_time) * \
                         random.uniform(MIN_SPEED_VARIATION, MAX_SPEED_VARIATION) * \
                         (1 + (random.random() - 0.5) * RANDOMNESS_FACTOR)

            times.append((runner, total_time))

        return sorted(times, key=lambda x: x[1])