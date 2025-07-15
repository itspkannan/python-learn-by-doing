import asyncio
import time
from contextlib import asynccontextmanager, contextmanager

from opentelemetry.metrics import get_meter, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from service_management.core import Service

from observability.config import MetricsConfig


class MetricsService(Service):
    def __init__(self, metrics_config: MetricsConfig = None) -> None:
        super().__init__("MetricsService")
        self.metrics_config = metrics_config or MetricsConfig.from_env()
        if self.metrics_config.enabled:
            resource = Resource.create(
                attributes={"service.name": self.metrics_config.service_name}
            )
            provider = MeterProvider(resource=resource)
            set_meter_provider(provider)
            self.meter = get_meter(self.metrics_config.service_name)
        else:
            self.meter = None

    async def on_start(self):
        self.logger.info(
            "MetricsService started with metrics enabled = %s", self.metrics_config.enabled
        )

    async def on_stop(self):
        self.logger.info("MetricsService stopped.")
        self.meter = None

    @contextmanager
    def record(
        self,
        name: str,
        metric_type: str = "counter",
        unit: str = "1",
        description: str = "",
        attributes: dict | None = None,
    ):
        if self.metrics_config.enabled:
            metric = None
            if metric_type == "counter":
                metric = self.meter.create_counter(name=name, unit=unit, description=description)
                yield lambda: metric.add(1, attributes or {})
            elif metric_type == "histogram":
                metric = self.meter.create_histogram(name=name, unit=unit, description=description)
                start_time = time.perf_counter()
                yield lambda: metric.record(time.perf_counter() - start_time, attributes or {})
            else:
                yield lambda: None

    @asynccontextmanager
    async def arecord(
        self,
        name: str,
        metric_type: str = "counter",
        unit: str = "1",
        description: str = "",
        attributes: dict | None = None,
    ):
        if self.metrics_config.enabled:
            metric = None
            if metric_type == "counter":
                metric = self.meter.create_counter(name=name, unit=unit, description=description)
                yield lambda: metric.add(1, attributes or {})
            elif metric_type == "histogram":
                metric = self.meter.create_histogram(name=name, unit=unit, description=description)
                start_time = asyncio.get_event_loop().time()
                # Track elapsed time asynchronously inside the context manager
                try:
                    yield lambda: metric.record(
                        asyncio.get_event_loop().time() - start_time, attributes or {}
                    )
                finally:
                    # Capture any end-of-task or cleanup code here if needed
                    pass
            else:
                yield lambda: None
