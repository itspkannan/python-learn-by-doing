from .config import ObservabilityConfig

from .logging.service import LoggingService
from .metrics.service import MetricsService
from .tracer.service import TracingService


class ObservabilityService:
    def __init__(self, observability: ObservabilityConfig):
        self.logging_service = LoggingService(observability.logging_config)
        self.tracing_service = TracingService(observability.tracing_config)
        self.metrics_service = MetricsService(observability.metric_config)
