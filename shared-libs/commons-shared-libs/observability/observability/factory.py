from service_management.core.registry import Registry

from observability import ObservabilityConfig, ObservabilityService
from observability.config import LoggingConfig, MetricsConfig, TracingConfig
from observability.logging.service import LoggingService
from observability.metrics.service import MetricsService
from observability.tracer.service import TracingService


@Registry.register(MetricsService)
def metrics_factory(config: MetricsConfig = None):
    return MetricsService(config or MetricsConfig.from_env())


@Registry.register(TracingService)
def trace_factory(config: TracingConfig = None):
    return TracingService(config or TracingConfig.from_env())


@Registry.register(LoggingService)
def logging_factory(config: LoggingConfig = None):
    return LoggingService(config or LoggingConfig.from_env())


@Registry.register(ObservabilityService)
def observability_factory(config: ObservabilityConfig = None):
    return ObservabilityService(config or ObservabilityConfig.from_env())
