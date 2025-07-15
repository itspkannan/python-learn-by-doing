import logging

import websockets
from observability import ObservabilityService

_logger = logging.getLogger(__name__)


class AsyncWebSocketClient:
    async def connect(self, url: str):
        try:
            _logger.info(f"Connecting to WebSocket {url}")
            websocket = await websockets.connect(url)
            return websocket
        except Exception as e:
            _logger.error(f"WebSocket connection to {url} failed: {e}")
            raise


class TracedAsyncWebSocketClient:
    def __init__(self, observability_service: ObservabilityService):
        self.observability_service = observability_service

    async def connect(self, url: str):
        async with self.observability_service.tracing_service.start_span(f"WS CONNECT {url}"):
            async with self.observability_service.metrics_service.arecord(
                "ws_connect_duration", "histogram", attributes={"url": url}
            ) as record:
                try:
                    _logger.info(f"Connecting to WebSocket {url}")
                    websocket = await websockets.connect(url)
                    record()
                    return websocket
                except Exception as e:
                    _logger.error(f"WebSocket connection to {url} failed: {e}")
                    raise
