import logging
from collections.abc import Awaitable, Callable
from functools import partial

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from application.common.errors.base import AppError
# from presentation.web_api.config import TRACING
# from presentation.web_api.middlewares.metrics import APP_NAME
# from presentation.web_api.middlewares.metrics.labels import EXCEPTIONS
from presentation.web_api.responses import ErrorData, ErrorResponse

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppError, error_handler(500))
    # app.add_exception_handler(
    #     InvalidRedirectURLError, error_handler(status.HTTP_400_BAD_REQUEST)
    # )
    app.add_exception_handler(Exception, unknown_exception_handler)



def error_handler(
    status_code: int,
) -> Callable[..., Awaitable[ORJSONResponse]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(
    request: Request, err: AppError, status_code: int
) -> ORJSONResponse:
    method = request.method
    path = request.url.path

    logger.error("Handle error", exc_info=err, extra={"error": err})

    # if TRACING:
    #     EXCEPTIONS.labels(
    #         method=method,
    #         path=path,
    #         exception_type=type(err).__name__,
    #         app_name=APP_NAME,
    #     ).inc()

    return await handle_error(
        request=request,
        err=err,
        err_data=ErrorData(title=err.title, data=err.title),
        status=err.status,
        status_code=status_code,
    )


async def unknown_exception_handler(
    request: Request, err: Exception
) -> ORJSONResponse:
    method = request.method
    path = request.url.path

    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception(
        "Unknown error occurred", exc_info=err, extra={"error": err}
    )

    # if TRACING:
    #     EXCEPTIONS.labels(
    #         method=method,
    #         path=path,
    #         exception_type=type(err).__name__,
    #         app_name=APP_NAME,
    #     ).inc()

    return ORJSONResponse(
        ErrorResponse(
            error=ErrorData(data=str(err), title="Unknown error"),
            status=HTTP_500_INTERNAL_SERVER_ERROR,
        ),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(
    request: Request,
    err: Exception,
    err_data: ErrorData,
    status: int,
    status_code: int,
) -> ORJSONResponse:
    return ORJSONResponse(
        ErrorResponse(error=err_data, status=status_code),
        status_code=status_code,
    )
