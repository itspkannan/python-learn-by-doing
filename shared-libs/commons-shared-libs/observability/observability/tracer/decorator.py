import functools
from contextlib import asynccontextmanager, contextmanager

from service_management.core.registry import Registry

from observability.tracer.service import TracingService


@asynccontextmanager
async def _null_async_cm():
    yield


@contextmanager
def _null_cm():
    yield


def trace_span_async(span_name: str, attributes_fn=None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            tracing_service = getattr(self, "tracing_service", None) or getattr(
                self, "tracer", None
            )

            if not tracing_service:
                try:
                    tracing_service = Registry.resolve(TracingService)
                except Exception:
                    return None

            cm = tracing_service.start_span(span_name) if tracing_service else _null_async_cm()
            attributes = attributes_fn(self, *args, **kwargs) if attributes_fn else {}
            async with cm as span:
                if span and attributes:
                    for k, v in attributes.items():
                        span.set_attributes(attributes)
                return await func(self, *args, **kwargs)

        return wrapper

    return decorator


def trace_span_sync(span_name: str, attributes_fn=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            tracing_service = (
                getattr(self, "tracing_service", None)
                or getattr(self, "tracer", None)
                or Registry.resolve(TracingService, default=None)
            )
            if not tracing_service:
                return None

            cm = tracing_service.start_span_sync(span_name) if tracing_service else _null_cm()
            attributes = attributes_fn(self, *args, **kwargs) if attributes_fn else {}

            with cm as span:
                if span and attributes:
                    span.set_attributes(attributes)
                return func(self, *args, **kwargs)

        return wrapper

    return decorator
