from dataclasses import dataclass

from application.common.interfaces.uow import Uow
from application.runner.common.errors import (
    RunnerNotFoundByID,
    RunnerParameterValidationError,
)
from infrastructure.db.models import Runner
from infrastructure.db.repositories.runner_repo import RunnerRepo


@dataclass
class UpdateRunnerParametersCommand:
    runner_id: int
    reaction_time: float | None
    acceleration: float | None
    max_speed: float | None
    speed_decay: float | None


class UpdateRunnerParametersHandler:
    def __init__(self, runner_repo: RunnerRepo, uow: Uow):
        self.runner_repo = runner_repo
        self.uow = uow

    async def handle(self, command: UpdateRunnerParametersCommand) -> None:
        runner = await self.runner_repo.get_runner(command.runner_id)
        if runner is None:
            raise RunnerNotFoundByID

        if not (0.1 <= command.reaction_time <= 0.3) and not command.reaction_time == 0:
            raise RunnerParameterValidationError(
                f"Invalid reaction_time: {command.reaction_time}. Must be between 0.1 and 0.3 seconds."
            )
        if not (2 <= command.acceleration <= 10) and not command.acceleration == 0:
            raise RunnerParameterValidationError(
                f"Invalid acceleration: {command.acceleration}. Must be between 2 and 10 m/s^2."
            )
        if not (7 <= command.max_speed <= 12) and not command.max_speed == 0:
            raise RunnerParameterValidationError(
                f"Invalid max_speed: {command.max_speed}. Must be between 7 and 12 m/s."
            )
        if not (0.05 <= command.speed_decay <= 0.5) and not command.speed_decay == 0:
            raise RunnerParameterValidationError(
                f"Invalid speed_decay: {command.speed_decay}. Must be between 0.05 and 0.5."
            )

        for key, value in command.__dict__.items():
            if key not in ["runner_id"] and value not in (None, 0):
                setattr(runner, key, value)

        await self.uow.commit()
