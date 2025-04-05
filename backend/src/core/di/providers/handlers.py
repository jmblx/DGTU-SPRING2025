from dishka import Provider, provide, Scope

from application.race.get_last_ten_races_handler import GetLastTenRacesHandler
from application.runner.get_all_runners_handler import GetAllRunnersHandler
from application.runner.update_parameters_handler import UpdateRunnerParametersHandler


class HandlerProvider(Provider):
    update_runner_parameters_handler = provide(
        UpdateRunnerParametersHandler, scope=Scope.REQUEST
    )
    get_all_runners_handler = provide(GetAllRunnersHandler, scope=Scope.REQUEST)
    get_last_ten_races_handler = provide(GetLastTenRacesHandler, scope=Scope.REQUEST)
