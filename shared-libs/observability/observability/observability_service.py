from .config import ObservabilityConfig
from .logging import LoggingService
from .metrics import MetricsService
from .tracer import TracingService


class ObservabilityService:
    def __init__(self, observability: ObservabilityConfig) -> None:
        self.logging_service = LoggingService(observability.logging_config)
        self.tracing_service = TracingService(observability.tracing_config)
        self.metrics_service = MetricsService(observability.metric_config)
