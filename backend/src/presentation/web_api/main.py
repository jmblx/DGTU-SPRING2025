import logging
from contextlib import asynccontextmanager
from dataclasses import asdict

from core.config import config_loader
from core.di.container import container
from dishka.integrations.fastapi import (
    setup_dishka,
)
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from infrastructure.log.main import configure_logging
from presentation.web_api.exceptions import setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    yield
    await app.state.dishka_container.close()


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        root_path="/api/v1",
        default_response_class=ORJSONResponse,
    )
    setup_exception_handlers(app)
    return app


def create_production_app():
    app = create_app()
    setup_dishka(container=container, app=app)
    return app


app = create_production_app()

global_config = config_loader.app_config.global_
logging_config = config_loader.logging_config
configure_logging(logging_config)


def main():
    if not global_config.debug:
        from presentation.web_api.gunicorn_application import Application

        gunicorn_config = config_loader.app_config.gunicorn
        gunicorn_app = Application(application=app, options=asdict(gunicorn_config))
        gunicorn_app.run()


if __name__ == "__main__":
    main()
