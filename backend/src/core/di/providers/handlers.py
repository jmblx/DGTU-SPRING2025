from dishka import Provider, provide, Scope

from application.runner.update_parameters_handler import UpdateRunnerParametersHandler


class HandlerProvider(Provider):
    update_runner_parameters_handler = provide(
        UpdateRunnerParametersHandler, scope=Scope.REQUEST
    )
