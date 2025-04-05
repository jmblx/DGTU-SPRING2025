from dishka import Provider, Scope, provide

from infrastructure.db.repositories.runner_repo import RunnerRepo


class RepositoriesProvider(Provider):
    runner_repo = provide(RunnerRepo, scope=Scope.REQUEST)
