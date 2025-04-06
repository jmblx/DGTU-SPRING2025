from application.runner.get_all_runners_handler import GetAllRunnersHandler
from application.runner.update_parameters_handler import (
    UpdateRunnerParametersCommand,
    UpdateRunnerParametersHandler,
)
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from infrastructure.db.repositories.runner_repo import RunnerDTO
from presentation.web_api.routes.schemas import RunnerParameters

runner_router = APIRouter(route_class=DishkaRoute, tags=["runner"], prefix="/runners")


@runner_router.put("/{runner_id}")
async def update_runner(
    runner_id: int,
    handler: FromDishka[UpdateRunnerParametersHandler],
    data: RunnerParameters,
) -> RunnerDTO:
    return await handler.handle(
        UpdateRunnerParametersCommand(runner_id=runner_id, **data.model_dump())
    )


@runner_router.get("")
async def get_runners(
    handler: FromDishka[GetAllRunnersHandler],
):
    return await handler.handle()
