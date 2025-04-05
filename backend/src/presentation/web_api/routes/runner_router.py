from dishka import AsyncContainer, FromDishka
from dishka.integrations.fastapi import inject, DishkaRoute
from fastapi import APIRouter

from application.runner.update_parameters_handler import (
    UpdateRunnerParametersHandler,
    UpdateRunnerParametersCommand,
)
from presentation.web_api.routes.schemas import RunnerParameters

runner_router = APIRouter(route_class=DishkaRoute, tags=["runner"], prefix="/runner")


@runner_router.put("/{runner_id}")
async def update_runner(
    runner_id: int,
    handler: FromDishka[UpdateRunnerParametersHandler],
    data: RunnerParameters,
):
    await handler.handle(
        UpdateRunnerParametersCommand(runner_id=runner_id, **data.model_dump())
    )
