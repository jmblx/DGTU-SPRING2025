import logging
import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

import yaml

# from infrastructure.log.main import AppLoggingConfig
from presentation.web_api.gunicorn.config import GunicornConfig


if os.getenv("DEBUG", "true").lower() not in ("false", "0"):
    from dotenv import load_dotenv

    load_dotenv()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
# API_ADMIN_PWD = os.environ.get("API_ADMIN_PWD")
DEFAULT_TOML_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config"
    / "config.toml"
)
LOGGING_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "config"
    / "logging.yaml"
)


@dataclass
class PresentationConfig:
    gunicorn_config: GunicornConfig
    # app_logging_config: AppLoggingConfig
    app_logging_config: dict


def read_toml(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


data = read_toml(str(DEFAULT_TOML_CONFIG_PATH))

logger = logging.getLogger(__name__)


def load_config(path: str | None = None) -> PresentationConfig:
    if path is None:
        path = os.getenv("CONFIG_PATH", LOGGING_CONFIG_PATH)

    # data = read_toml(path)

    gunicorn_config = GunicornConfig(**data.get("gunicorn"))
    # app_logging_config = AppLoggingConfig(**data.get("logging"))

    try:
        with path.open("r") as f:
            app_logging_config = yaml.safe_load(f)
    except IOError:
        logging.basicConfig(level=logging.DEBUG)
        logger.warning("Logging config file not found, use basic config")
    return PresentationConfig(gunicorn_config, app_logging_config)
