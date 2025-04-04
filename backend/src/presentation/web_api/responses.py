from dataclasses import dataclass, field
from typing import Generic, TypeVar

TResult = TypeVar("TResult")
TError = TypeVar("TError")


@dataclass(frozen=True)
class Response:
    pass


@dataclass(frozen=True)
class OkResponse(Response, Generic[TResult]):
    status: int = 200
    result: TResult | None = None


@dataclass(frozen=True)
class ErrorData(Generic[TError]):
    title: str
    data: TError | None = None


@dataclass(frozen=True)
class ErrorResponse(Response, Generic[TError]):
    status: int
    error: ErrorData[TError]
