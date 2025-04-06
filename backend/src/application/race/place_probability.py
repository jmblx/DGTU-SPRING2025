import random
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.race_simulate import MIN_SPEED_VARIATION, MAX_SPEED_VARIATION, RANDOMNESS_FACTOR, DISTANCE
from infrastructure.db.models import Runner


class RaceProbabilityCalculator:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def calculate_win_probabilities(self, num_simulations: int = 1000) -> Dict[int, Dict[int, float]]:
        """
        Рассчитывает вероятности занятых мест для каждого бегуна
        Возвращает словарь: {runner_id: {position: probability}}
        """
        result = await self.session.execute(select(Runner))
        runners = result.scalars().all()

        if not runners:
            return {}

        position_counts = {runner.id: [0] * len(runners) for runner in runners}

        for _ in range(num_simulations):
            simulated_race = self._simulate_single_race(runners)

            for position, (runner, _, _) in enumerate(simulated_race, start=1):
                position_counts[runner.id][position - 1] += 1

        probabilities = {}
        for runner_id, counts in position_counts.items():
            total = sum(counts)
            probabilities[runner_id] = {
                pos + 1: count / total for pos, count in enumerate(counts)
            }

        return probabilities

    def _simulate_single_race(self, runners: List[Runner]) -> List[tuple[Runner, float, list[float]]]:
        """Упрощенная симуляция одной гонки без прогресса"""
        times = {}

        for runner in runners:
            reaction_time = runner.reaction_time

            acceleration_time = runner.max_speed / runner.acceleration

            remaining_distance = DISTANCE - (0.5 * runner.acceleration * acceleration_time ** 2)
            if remaining_distance > 0:
                decay_time = remaining_distance / runner.max_speed
            else:
                decay_time = 0

            random_factor = random.uniform(MIN_SPEED_VARIATION, MAX_SPEED_VARIATION)
            total_time = (reaction_time + acceleration_time + decay_time) * random_factor

            times[runner.id] = total_time * (1 + (random.random() - 0.5) * RANDOMNESS_FACTOR)

        sorted_runners = sorted(runners, key=lambda r: times[r.id])

        return [(runner, times[runner.id], []) for runner in sorted_runners]