from starlette.responses import HTMLResponse

from application.race.get_last_ten_races_handler import GetLastTenRacesHandler
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException

from infrastructure.db.readers.race_reader import RaceReader
from presentation.web_api.routes.schemas import LastRacesResponse

race_router = APIRouter(route_class=DishkaRoute, tags=["race"], prefix="/races")


@race_router.get("/last")
async def get_last_races(handler: FromDishka[GetLastTenRacesHandler]):
    return LastRacesResponse(races=await handler.handle())


@race_router.get("/races/{race_id}/chart", response_class=HTMLResponse)
async def get_race_chart(
    race_id: int,
    reader: FromDishka[RaceReader]
):
    img_data = await reader.get_race_chart(race_id)
    if not img_data:
        raise HTTPException(status_code=404, detail="Race not found")

    return f"""
    <html>
        <body>
            <img src="data:image/png;base64,{img_data}" />
        </body>
    </html>
    """
