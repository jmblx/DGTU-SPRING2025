import logging
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class GunicornConfig:
    bind: str
    workers: int
    timeout: int
    worker_class: str


@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str
    db_uri: str = field(init=False)


@dataclass
class RedisConfig:
    host: str
    port: int
    uri: str = field(init=False)


@dataclass
class GlobalConfig:
    debug: bool


@dataclass
class AppConfig:
    gunicorn: GunicornConfig
    database: DatabaseConfig
    redis: RedisConfig
    global_: GlobalConfig


logger = logging.getLogger("core.config")


class ConfigLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_configs()
        return cls._instance

    @classmethod
    def _load_configs(cls):
        base_path = Path(__file__).parent.parent.parent.parent
        config_path = base_path / "backend" / "config" / "config.toml"
        logging_path = base_path / "backend" / "config" / "logging.yaml"

        with open(config_path, "rb") as f:
            toml_data = tomllib.load(f)

        try:
            with open(logging_path) as f:
                logging_config = yaml.safe_load(f)
        except FileNotFoundError:
            logging_config = {
                "version": 1,
                "disable_existing_loggers": False,
                "handlers": {
                    "console": {"class": "logging.StreamHandler", "formatter": "simple"}
                },
                "formatters": {
                    "simple": {
                        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                    }
                },
                "root": {"handlers": ["console"], "level": "INFO"},
            }
        redis = RedisConfig(**toml_data["redis"])
        redis.uri = f"redis://{toml_data['redis']['host']}:{toml_data['redis']['port']}"
        logger.info(toml_data['database'])
        cls._app_config = AppConfig(
            gunicorn=GunicornConfig(**toml_data["gunicorn"]),
            database=DatabaseConfig(**toml_data["database"]),
            redis=redis,
            global_=GlobalConfig(**toml_data["global"]),
        )
        cls._logging_config = logging_config

    @property
    def app_config(self) -> AppConfig:
        return self._app_config

    @property
    def logging_config(self) -> dict:
        return self._logging_config


config_loader = ConfigLoader()
