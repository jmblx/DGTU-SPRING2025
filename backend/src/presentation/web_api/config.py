import logging
import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

import yaml

DEBUG = os.getenv("DEBUG", "true").lower() not in ("false", "0")

if DEBUG:
    from dotenv import load_dotenv

    load_dotenv()

TOML_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent / "config" / "config.toml"
)
LOGGING_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent / "config" / "logging.yaml"
)


@dataclass
class GunicornConfig:
    bind: str = "0.0.0.0:8000"
    workers: int = 2
    timeout: int = 30
    worker_class: str = "uvicorn.workers.UvicornWorker"


@dataclass
class PresentationConfig:
    gunicorn_config: GunicornConfig
    app_logging_config: dict


def read_toml(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


data = read_toml(str(TOML_CONFIG_PATH))

logger = logging.getLogger(__name__)


def load_config(path: str | None = None) -> PresentationConfig:
    if path is None:
        path = os.getenv("CONFIG_PATH", LOGGING_CONFIG_PATH)

    gunicorn_config = GunicornConfig(**data.get("gunicorn"))

    try:
        with path.open("r") as f:
            app_logging_config = yaml.safe_load(f)
    except OSError:
        logging.basicConfig(level=logging.DEBUG)
        logger.warning("Logging config file not found, use basic config")
    return PresentationConfig(gunicorn_config, app_logging_config)
