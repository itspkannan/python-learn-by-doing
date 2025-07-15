from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, Mock

class MockObservabilityService:
    def __init__(self):
        self.tracing_service = Mock()
        self.metrics_service = Mock()

        self._span_cm = AsyncMock()
        self._record_cm = AsyncMock()

        @asynccontextmanager
        async def _mock_span_cm(name):
            yield self._span_cm

        @asynccontextmanager
        async def _mock_record_cm(metric_name, metric_type, attributes=None):
            yield self._record_cm

        self.tracing_service.start_span.side_effect = _mock_span_cm
        self.metrics_service.arecord.side_effect = _mock_record_cm
