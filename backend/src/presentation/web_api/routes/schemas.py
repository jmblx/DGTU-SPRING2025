from typing import Optional

from pydantic import BaseModel, Field


class RunnerParameters(BaseModel):
    reaction_time: Optional[float] = Field(
        None, description="Reaction time in seconds (0.1 - 0.3 sec)"
    )
    acceleration: Optional[float] = Field(
        None, description="Acceleration in m/s² (greater than or equal to 0)"
    )
    max_speed: Optional[float] = Field(
        None, description="Maximum speed in m/s (greater than or equal to 0)"
    )
    speed_decay: Optional[float] = Field(
        None, description="Speed decay factor (greater than or equal to 0)"
    )
