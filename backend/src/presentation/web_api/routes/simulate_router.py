# from fastapi import APIRouter, HTTPException
# from dishka.integrations.fastapi import DishkaRoute
# from dishka import FromDishka
# from typing import List
# import logging
#
# logger = logging.getLogger(__name__)
#
# simulate_router = APIRouter(
#     route_class=DishkaRoute,
#     tags=["Race Simulation"],
#     prefix="/api/simulate"
# )
#
#
# @simulate_router.get("/race", summary="Симуляция забега")
# async def simulate_race_endpoint(
#     calc: FromDishka[Calculate]
# ) -> List[dict]:
#     formatted_results = await calc.calculate_race()
#     return formatted_results
