from contextlib import contextmanager
from functools import wraps

from service_management.core.registry import Registry

from observability.metrics import MetricsService


@contextmanager
def _null_cm():
    yield


def record_metric_async(
    name: str,
    metric_type: str = "counter",
    unit: str = "1",
    description: str = "",
    attributes_fn=None,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                metrics = Registry.resolve(MetricsService)
            except Exception:
                metrics = None

            attributes = (
                attributes_fn(self, *args, **kwargs)
                if attributes_fn
                else {"service": getattr(self, "name", "unknown")}
            )

            if metrics and metrics.metrics_config.enabled:
                async with metrics.arecord(
                    name=name,
                    metric_type=metric_type,
                    unit=unit,
                    description=description,
                    attributes=attributes,
                ) as record:
                    result = await func(self, *args, **kwargs)
                    record()
                    return result
            else:
                return await func(self, *args, **kwargs)

        return wrapper

    return decorator


def record_metric_sync(
    name: str,
    metric_type: str = "counter",
    unit: str = "1",
    description: str = "",
    attributes_fn=None,
):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                metrics = Registry.resolve(MetricsService)
            except Exception:
                metrics = None

            attributes = (
                attributes_fn(self, *args, **kwargs)
                if attributes_fn
                else {"service": getattr(self, "name", "unknown")}
            )

            cm = (
                metrics.record(
                    name=name,
                    metric_type=metric_type,
                    unit=unit,
                    description=description,
                    attributes=attributes,
                )
                if metrics and metrics.metrics_config.enabled
                else _null_cm()
            )

            with cm as record:
                result = func(self, *args, **kwargs)
                record()
                return result

        return wrapper

    return decorator
