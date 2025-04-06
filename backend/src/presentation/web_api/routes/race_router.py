from application.race.get_last_ten_races_handler import GetLastTenRacesHandler
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from presentation.web_api.routes.schemas import LastRacesResponse

race_router = APIRouter(route_class=DishkaRoute, tags=["race"], prefix="/races")


@race_router.get("/last/{last_race_id}")
async def get_last_races(last_race_id: int, handler: FromDishka[GetLastTenRacesHandler]):
    return LastRacesResponse(races=await handler.handle(last_race_id))
