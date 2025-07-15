import logging

import websockets
from observability.metrics.decorator import record_metric_async
from observability.tracer.decorator import trace_span_async

_logger = logging.getLogger(__name__)


def ws_attributes(self, url: str):
    return {
        "service": self.__class__.__name__,
        "websocket.url": url,
    }


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
    @trace_span_async("WebSocketClient.connect", attributes_fn=ws_attributes)
    @record_metric_async(
        name="WebSocketClient.connect.duration",
        metric_type="histogram",
        unit="s",
        attributes_fn=ws_attributes,
    )
    async def connect(self, url: str):
        _logger.info(f"Connecting to WebSocket {url}")
        websocket = await websockets.connect(url)
        return websocket
