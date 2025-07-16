from __future__ import annotations

import logging
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TracingConfig:
    service_name: str
    enabled: bool

    @staticmethod
    def from_env() -> TracingConfig:
        return TracingConfig(
            service_name=os.getenv("SERVICE_NAME"),
            enabled=os.getenv("TRACING_ENABLED", "false").lower() == "true",
        )

@dataclass(frozen=True)
class LoggingConfig:
    service_name: str
    level: int = logging.INFO

    @staticmethod
    def from_env() -> LoggingConfig:
        return LoggingConfig(service_name=os.getenv("SERVICE_NAME"))


@dataclass(frozen=True)
class MetricsConfig:
    service_name: str
    enabled: bool

    @staticmethod
    def from_env() -> MetricsConfig:
        return MetricsConfig(
            service_name=os.getenv("SERVICE_NAME"),
            enabled=os.getenv("METRICS_ENABLED", "false").lower() == "true",
        )


@dataclass()
class ObservabilityConfig:
    logging_config: LoggingConfig
    metric_config: MetricsConfig
    tracing_config: TracingConfig

    @staticmethod
    def from_env() -> ObservabilityConfig:
        return ObservabilityConfig(
            LoggingConfig.from_env(), MetricsConfig.from_env(), TracingConfig.from_env()
        )
