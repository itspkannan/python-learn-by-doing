import logging

from service_management.core.service import Service

from observability.config import LoggingConfig


class LoggingService(Service):
    def __init__(self, logging_config: LoggingConfig = None) -> None:
        super().__init__("LoggingService")
        self.logging_config = logging_config or LoggingConfig.from_env()

    async def before_start(self):
        self.logger.info(f"{self.name} starting.")

    async def after_start(self):
        pass

    async def before_stop(self):
        self.logger.info(f"{self.name} stopping.")

    async def after_stop(self):
        pass

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
