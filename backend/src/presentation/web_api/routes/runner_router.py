import asyncio
import json

from dishka import AsyncContainer, FromDishka
from dishka.integrations.fastapi import inject, DishkaRoute
from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from application.runner.update_parameters_handler import UpdateRunnerParametersHandler

runner_router = APIRouter(route_class=DishkaRoute, tags=["runner"], prefix="/runner")


@runner_router.put("/")
async def update_runner(handler: FromDishka[UpdateRunnerParametersHandler], command: ):
    await handler.handle(command)
