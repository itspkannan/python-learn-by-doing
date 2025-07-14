import logging

from observability.config import LoggingConfig


class LoggingService:
    def __init__(self, logging_config: LoggingConfig = None) -> None:
        self.logging_config = logging_config or LoggingConfig.from_env()

    def get_logger(self, name: str = None):
        logger_name = name or self.logging_config.service_name
        logger = logging.getLogger(logger_name)

        if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(self.logging_config.level)

        return logger
