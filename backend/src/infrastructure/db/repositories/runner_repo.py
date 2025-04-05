from dataclasses import dataclass
from typing import TypedDict

from sqlalchemy import select

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

    async def get_all_runners(self) -> list[RunnerDTO]:
        runners = await self.session.execute(select(Runner))
        runners = runners.scalars().all()

        return [RunnerDTO(
            runner_id=r.id,
            reaction_time=round(r.reaction_time, 2) if r.reaction_time is not None else None,
            acceleration=round(r.acceleration, 2) if r.acceleration is not None else None,
            max_speed=round(r.max_speed, 2) if r.max_speed is not None else None,
            speed_decay=round(r.speed_decay, 2) if r.speed_decay is not None else None,
        ) for r in runners]

    async def save(self, runner: Runner) -> RunnerDTO:
        runner = await self.session.merge(runner)
        await self.session.flush()
        return RunnerDTO(
            runner_id=runner.id,
            reaction_time=round(runner.reaction_time, 2) if runner.reaction_time is not None else None,
            acceleration=round(runner.acceleration, 2) if runner.acceleration is not None else None,
            max_speed=round(runner.max_speed, 2) if runner.max_speed is not None else None,
            speed_decay=round(runner.speed_decay, 2) if runner.speed_decay is not None else None,
        )
