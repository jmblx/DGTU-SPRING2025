import json

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from redis.asyncio import Redis

from presentation.web_api.routes.schemas import PositionProbability, ProbabilityResponse, RunnerPairProbability

probability_router = APIRouter(route_class=DishkaRoute, tags=["probability"], prefix="/probabilities")


@probability_router.get("", response_model=ProbabilityResponse)
async def get_probabilities(redis: FromDishka[Redis]):
    # Получаем данные из Redis
    position_data = await redis.get("position_probability_cache")
    top2_data = await redis.get("top2_probability_cache")
    top3_data = await redis.get("top3_probability_cache")
    pair_data = await redis.get("pair_matrix_cache")

    # Парсим JSON
    position_probs = json.loads(position_data) if position_data else {}
    top2_probs = json.loads(top2_data) if top2_data else {}
    top3_probs = json.loads(top3_data) if top3_data else {}
    pair_probs = json.loads(pair_data) if pair_data else {}

    # Преобразуем данные в структуру Pydantic
    response = ProbabilityResponse(
        position_probabilities={
            int(runner_id): PositionProbability(
                position_1=positions.get("1", 0),
                position_2=positions.get("2", 0),
                position_3=positions.get("3", 0),
                position_4=positions.get("4", 0),
                position_5=positions.get("5", 0),
                position_6=positions.get("6", 0)
            )
            for runner_id, positions in position_probs.items()
        },
        top2_probabilities={int(k): v for k, v in top2_probs.items()},
        top3_probabilities={int(k): v for k, v in top3_probs.items()},
        pair_matrix={
            int(first): RunnerPairProbability(
                runner_1=pairs.get("1"),
                runner_2=pairs.get("2"),
                runner_3=pairs.get("3"),
                runner_4=pairs.get("4"),
                runner_5=pairs.get("5"),
                runner_6=pairs.get("6")
            )
            for first, pairs in pair_probs.items()
        }
    )

    return response