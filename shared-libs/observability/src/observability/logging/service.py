import logging

from observability.config import LoggingConfig


class LoggingService:
    def __init__(self, logging_config: LoggingConfig):
        self.logging_config = logging_config or LoggingConfig.from_env()
        self.logging_config = logging_config
        self.logger = logging.getLogger(logging_config.service_name)
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging_config.level)

    def get_logger(self):
        return self.logger
