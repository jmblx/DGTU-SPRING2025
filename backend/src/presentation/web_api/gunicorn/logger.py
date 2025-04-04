from gunicorn.glogging import Logger


class GunicornLoggingConfig(Logger):
    def setup(self, cfg) -> None:
        super().setup(cfg)

        # Настройка ошибок Gunicorn
        self.error_log.setLevel("CRITICAL")
        self.error_log.propagate = False

        # Отключаем логи запросов Gunicorn
        self.access_log.propagate = False
