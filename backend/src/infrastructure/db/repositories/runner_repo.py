from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.models import Runner


class RunnerRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_runner(self, runner_id: int) -> Runner | None:
        return await self.session.get(Runner, runner_id)

    async def save(self, runner: Runner) -> None:
        runner = await self.session.merge(runner)
        await self.session.flush()
