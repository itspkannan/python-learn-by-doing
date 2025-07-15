__all__ = (
    "MetricsService",
    "record_metric",
)

from .decorator import record_metric
from .service import MetricsService
