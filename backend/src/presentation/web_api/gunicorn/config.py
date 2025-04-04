from dataclasses import dataclass
from typing import Type

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# from presentation.web_api.gunicorn.logger import GunicornLoggingConfig

load_dotenv()


LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


@dataclass
class GunicornConfig:
    bind: str = "0.0.0.0:8000"
    workers: int = 2
    timeout: int = 30
    worker_class: str = "uvicorn.workers.UvicornWorker"
    proxy_protocol: bool = True
    proxy_allow_ips: str = "*"
    forwarded_allow_ips: str = "*"
