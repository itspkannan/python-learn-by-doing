from service_management.core import Service

from .config import ObservabilityConfig
from .logging import LoggingService
from .metrics import MetricsService
from .tracer import TracingService


class ObservabilityService(Service):
    def __init__(self, observability: ObservabilityConfig) -> None:
        super().__init__("ObservabilityService")
        self.logging_service = LoggingService(observability.logging_config)
        self.tracing_service = TracingService(observability.tracing_config)
        self.metrics_service = MetricsService(observability.metric_config)

    async def on_start(self):
        self.logger.info(f"{self.name} starting.")
        for service in [self.logging_service, self.tracing_service, self.metrics_service]:
            await service.start()
        self.logger.info(f"{self.name} started.")

    async def on_stop(self):
        self.logger.info(f"{self.name} stopped.")
