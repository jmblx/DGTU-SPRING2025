from infrastructure.db.repositories.runner_repo import RunnerDTO, RunnerRepo


class GetAllRunnersHandler:
    def __init__(self, runner_repo: RunnerRepo):
        self.runner_repo = runner_repo

    async def handle(self) -> list[RunnerDTO]:
        return await self.runner_repo.get_all_runners()
