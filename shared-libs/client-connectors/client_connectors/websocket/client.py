import logging

import websockets


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
