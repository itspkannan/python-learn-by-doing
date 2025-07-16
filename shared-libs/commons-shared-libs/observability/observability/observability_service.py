from service_management.core.service import Service

from .config import ObservabilityConfig
from .logging.service import LoggingService
from .metrics.service import MetricsService
from .tracer.service import TracingService


class ObservabilityService(Service):

    def __init__(self, observability_config: ObservabilityConfig = None) -> None:
        super().__init__("ObservabilityService")
        observability_config = observability_config or ObservabilityConfig.from_env()
        self.logging_service = LoggingService(observability_config.logging_config)
        self.tracing_service = TracingService(observability_config.tracing_config)
        self.metrics_service = MetricsService(observability_config.metric_config)

    async def before_start(self):
        for service in [self.logging_service, self.tracing_service, self.metrics_service]:
            await service.before_start()

    async def after_start(self):
        for service in [self.logging_service, self.tracing_service, self.metrics_service]:
            await service.after_start()

    async def before_stop(self):
        for service in [self.logging_service, self.tracing_service, self.metrics_service]:
            await service.before_stop()

    async def after_stop(self):
        for service in [self.logging_service, self.tracing_service, self.metrics_service]:
            await service.after_stop()
