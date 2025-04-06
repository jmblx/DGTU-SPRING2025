from pydantic import BaseModel, Field


class RunnerParameters(BaseModel):
    reaction_time: float | None = Field(
        None, description="Reaction time in seconds (0.1 - 0.3 sec)"
    )
    acceleration: float | None = Field(
        None, description="Acceleration in m/s² (greater than or equal to 0)"
    )
    max_speed: float | None = Field(
        None, description="Maximum speed in m/s (greater than or equal to 0)"
    )
    speed_decay: float | None = Field(
        None, description="Speed decay factor (greater than or equal to 0)"
    )


class LastRacesResponse(BaseModel):
    """Pydantic модель для ответа API"""

    races: dict[int, dict[int, int]] = {
        "example": {123: {1: 3, 2: 1}, 124: {5: 1, 2: 2}},
        "description": "Словарь {race_id: {runner_id: position}}",
    }
