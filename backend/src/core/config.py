from dataclasses import dataclass
from pathlib import Path
import tomllib
from typing import Any, Dict
import logging
import os


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


@dataclass
class RedisConfig:
    host: str
    port: int


@dataclass
class LoggingConfig:
    level: str
    render_json_logs: bool


@dataclass
class GlobalConfig:
    debug: bool


@dataclass
class AppConfig:
    gunicorn: GunicornConfig
    logging: LoggingConfig
    database: DatabaseConfig
    redis: RedisConfig
    global_: GlobalConfig


def load_config(path: str | None = None) -> AppConfig:
    if path is None:
        path = os.getenv("CONFIG_PATH", "config.toml")

    with open(path, "rb") as f:
        data = tomllib.load(f)

    return AppConfig(
        gunicorn=GunicornConfig(**data["gunicorn"]),
        logging=LoggingConfig(**data["logging"]),
        database=DatabaseConfig(**data["database"]),
        redis=RedisConfig(**data["redis"]),
        global_=GlobalConfig(**data["global"]),
    )


# Инициализация при старте
config = load_config()