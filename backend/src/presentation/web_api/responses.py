from dataclasses import dataclass
from typing import Generic, TypeVar

TError = TypeVar("TError")


@dataclass(frozen=True)
class Response:
    pass


@dataclass(frozen=True)
class ErrorData(Generic[TError]):
    title: str
    data: TError | None = None


@dataclass(frozen=True)
class ErrorResponse(Response, Generic[TError]):
    status: int
    error: ErrorData[TError]
