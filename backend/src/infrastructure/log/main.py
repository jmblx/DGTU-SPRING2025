# import logging
# import time
# from dataclasses import dataclass
# from sqlalchemy import log as sa_log
# from pathlib import Path
#
# from sqlalchemy import Engine, event
# import structlog
# from typing import Callable
#
# from structlog import BoundLogger
# from structlog._log_levels import add_log_level
# from structlog.contextvars import merge_contextvars
# from structlog.processors import CallsiteParameterAdder, CallsiteParameter, JSONRenderer, TimeStamper
# from structlog.stdlib import ProcessorFormatter, ExtraAdder, add_logger_name
#
#
# @dataclass
# class AppLoggingConfig:
#     render_json_logs: bool = False
#     path: Path | None = None
#     level: str = "DEBUG"
#
#
# def setup_sqlalchemy_logging():
#     """Подключает обработчики SQLAlchemy."""
#     @event.listens_for(Engine, "before_cursor_execute")
#     def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#         conn.info.setdefault("query_start_time", []).append(time.time())
#         logging.getLogger("sqlalchemy").debug(f"Start Query: {statement} | Parameters: {parameters}")
#
#     @event.listens_for(Engine, "after_cursor_execute")
#     def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#         total = time.time() - conn.info["query_start_time"].pop(-1)
#         logging.getLogger("sqlalchemy").debug(f"Query Complete! Time: {total:.3f} sec")
#
#     @event.listens_for(Engine, "handle_error")
#     def handle_error(context):
#         logging.getLogger("sqlalchemy").error(f"Error: {context.original_exception}")
#
#
# def configure_logging(cfg: AppLoggingConfig):
#     """Настраивает логирование в зависимости от переданного конфигурационного объекта."""
#
#     def add_callsite_for_warning_and_above(logger, method_name, event_dict):
#         """
#         Добавляет информацию о строке и функции вызова, если уровень лога WARNING и выше.
#         """
#         level = event_dict.get("level", "INFO").upper()
#         if level in ("WARNING", "ERROR", "CRITICAL"):
#             # Добавляем информацию о вызове только для WARNING и выше
#             event_dict["pathname"] = event_dict.get("pathname", "")
#             event_dict["func_name"] = event_dict.get("func_name", "")
#             event_dict["lineno"] = event_dict.get("lineno", "")
#         return event_dict
#
#     # Процессоры для structlog
#     common_processors = [
#         add_log_level,  # Добавляет уровень логирования
#         add_logger_name,  # Добавляет имя логгера
#         ExtraAdder(),  # Обрабатывает данные из `extra`
#         TimeStamper(fmt="iso"),  # Добавляет timestamp
#         add_callsite_for_warning_and_above,  # Добавляем обработчик вызова только для WARNING и выше
#     ]
#
#     # Рендеринг: JSON или человекочитаемый
#     if cfg.render_json_logs:
#         renderer = JSONRenderer()
#     else:
#         renderer = structlog.dev.ConsoleRenderer()
#
#     # Настройка structlog
#     structlog.configure(
#         processors=common_processors + [renderer],
#         context_class=dict,
#         wrapper_class=structlog.stdlib.BoundLogger,
#         logger_factory=structlog.stdlib.LoggerFactory(),
#     )
#
#     # Настройка обработчиков
#     handlers = []
#
#     # Консольный вывод
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(cfg.level.upper())
#     console_formatter = structlog.stdlib.ProcessorFormatter(
#         processor=renderer,  # Используем выбранный рендерер
#         foreign_pre_chain=common_processors,  # Предобработка
#     )
#     console_handler.setFormatter(console_formatter)
#     handlers.append(console_handler)
#
#     # Логи в файл, если указан путь
#     if cfg.path:
#         cfg.path.parent.mkdir(parents=True, exist_ok=True)
#         file_handler = logging.FileHandler(cfg.path, mode="a")
#         file_handler.setLevel(cfg.level.upper())
#         file_formatter = structlog.stdlib.ProcessorFormatter(
#             processor=renderer,  # Используем тот же рендерер
#             foreign_pre_chain=common_processors,
#         )
#         file_handler.setFormatter(file_formatter)
#         handlers.append(file_handler)
#
#     # Установка обработчиков в root logger
#     logging.basicConfig(
#         level=cfg.level.upper(),
#         handlers=handlers,
#         force=True,  # Убирает старые обработчики
#     )


import logging.config

logger = logging.getLogger(__name__)


def configure_logging(logging_config: dict):

    logging.config.dictConfig(logging_config)
    logger.info("Logging configured successfully")
