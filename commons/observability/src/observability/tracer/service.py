from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import Tracer
from contextlib import asynccontextmanager, contextmanager

from observability.config import TracingConfig


class TracingService:
    def __init__(self, tracing_config: TracingConfig):
        self.tracing_config = tracing_config or TracingConfig.from_env()
        if self.tracing_config.enabled:
            provider = TracerProvider()
            processor = SimpleSpanProcessor(ConsoleSpanExporter())
            provider.add_span_processor(processor)
            trace.set_tracer_provider(provider)
        self.tracer: Tracer = trace.get_tracer(self.tracing_config.service_name)

    def get_tracer(self) -> Tracer:
        return self.tracer

    def is_enabled(self) -> bool:
        return self.tracing_config.enabled

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
