from dataclasses import dataclass
from typing import TypedDict

from infrastructure.db.models import Runner
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class RunnerDTO:
    runner_id: int
    reaction_time: float
    acceleration: float
    max_speed: float
    speed_decay: float


class RunnerRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_runner(self, runner_id: int) -> Runner | None:
        return await self.session.get(Runner, runner_id)

    async def save(self, runner: Runner) -> RunnerDTO:
        runner = await self.session.merge(runner)
        await self.session.flush()
        return RunnerDTO(
            runner_id=runner.id,
            reaction_time=runner.reaction_time,
            acceleration=runner.acceleration,
            max_speed=runner.max_speed,
            speed_decay=runner.speed_decay,
        )
