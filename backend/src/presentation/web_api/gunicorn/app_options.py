def get_app_options(
    host: str,
    port: int,
    timeout: int,
    workers: int,
) -> dict:
    return {
        "accesslog": "-",  # Поток вывода для логов доступа
        "errorlog": "-",  # Поток вывода для логов ошибок
        "bind": f"{host}:{port}",
        "logger_class": CustomGunicornLogger,  # Используем кастомный класс
        "timeout": timeout,
        "workers": workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
