from dishka import AsyncContainer, FromDishka
from dishka.integrations.fastapi import inject, DishkaRoute
from fastapi import APIRouter

from application.race.get_last_ten_races_handler import GetLastTenRacesHandler

race_router = APIRouter(route_class=DishkaRoute, tags=["race"], prefix="/races")


@race_router.get("/last")
async def get_last_races(handler: FromDishka[GetLastTenRacesHandler]):

