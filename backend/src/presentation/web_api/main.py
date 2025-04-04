import logging
import os
from contextlib import asynccontextmanager
from dataclasses import asdict

from dishka.integrations.fastapi import (
    setup_dishka,
)
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from core.di.container import container
from infrastructure.log.main import configure_logging
from presentation.web_api.config import load_config
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
    # setup_middlewares(app)
    return app


def create_production_app():
    app = create_app()
    setup_dishka(container=container, app=app)
    return app


if os.getenv("GUNICORN_MAIN", "false").lower() not in ("false", "0"):

    def main():
        from presentation.web_api.gunicorn.application import Application

        config = load_config()
        configure_logging(config.app_logging_config)
        gunicorn_app = Application(
            application=create_production_app(),
            options={
                **asdict(config.gunicorn_config),  # Опции Gunicorn
                "logconfig_dict": config.app_logging_config,  # Конфиг логирования
            },
        )
        gunicorn_app.run()

    if __name__ == "__main__":
        main()

else:
    config = load_config()
    configure_logging(config.app_logging_config)
    app = create_production_app()

    if __name__ == "__main__":
        uvicorn.run(
            app,
            port=8000,
            log_config=config.app_logging_config,
        )
