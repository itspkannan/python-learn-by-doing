from contextlib import asynccontextmanager, contextmanager

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.trace import Tracer
from service_management.core.service import Service

from observability.config import TracingConfig


class TracingService(Service):
    def __init__(self, tracing_config: TracingConfig) -> None:
        super().__init__("TracingService")
        self.tracer: Tracer | None = None
        self.tracing_config = tracing_config or TracingConfig.from_env()
        if self.tracing_config.enabled:
            provider = TracerProvider()
            processor = SimpleSpanProcessor(ConsoleSpanExporter())
            provider.add_span_processor(processor)
            trace.set_tracer_provider(provider)
            self.tracer = trace.get_tracer(self.tracing_config.service_name)

    async def before_start(self):
        pass

    async def after_start(self):
        self.logger.info(
            "TracingService started with tracking enabled = %s", self.tracing_config.enabled
        )

    async def before_stop(self):
        self.logger.info(f"{self.before_stop()} stopping.")
        self.tracer = None

    async def after_stop(self):
        pass

    @asynccontextmanager
    async def start_span(self, name: str):
        if self.tracing_config.enabled:
            with self.tracer.start_as_current_span(name) as span:
                yield span
        else:
            yield None

    @contextmanager
    def start_span_sync(self, name: str):
        if self.tracing_config.enabled:
            with self.tracer.start_as_current_span(name) as span:
                yield span
        else:
            yield None
