from infrastructure.db.models import Runner
from sqlalchemy.ext.asyncio import AsyncSession


class RunnerRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_runner(self, runner_id: int) -> Runner | None:
        return await self.session.get(Runner, runner_id)

    async def save(self, runner: Runner) -> int:
        runner = await self.session.merge(runner)
        await self.session.flush()
        return runner.id
