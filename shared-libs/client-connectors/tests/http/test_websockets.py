from unittest.mock import AsyncMock

import pytest
import websockets

from client_connectors.http import AsyncWebSocketClient
from client_connectors.http.websocket.client import TracedAsyncWebSocketClient
from tests.utils import MockObservabilityService


@pytest.mark.skip('need to be fixed')
@pytest.mark.asyncio
async def test_async_websocket_client_connect(mocker):
    mock_websocket = AsyncMock()
    mock_connect = mocker.patch("websockets.connect", return_value=mock_websocket)
    mock_logger = mocker.patch("client_connectors.http.websocket.client._logger")

    client = AsyncWebSocketClient()
    url = "ws://example.com"
    websocket = await client.connect(url)

    mock_connect.assert_called_once_with(url)
    assert websocket == mock_websocket
    mock_logger.info.assert_called_with(f"Connecting to WebSocket {url}")


@pytest.mark.skip('need to be fixed')
@pytest.mark.asyncio
async def test_traced_async_websocket_client_connect(mocker):
    mock_websocket = AsyncMock()
    mock_connect = mocker.patch("websockets.connect", new_callable=AsyncMock)
    mock_connect.return_value = mock_websocket

    mock_logger = mocker.patch("client_connectors.http.websocket.client._logger")

    class MockObservabilityService:
        def __init__(self):
            self.tracing_service = mocker.Mock()
            self.metrics_service = mocker.Mock()

            @pytest.asynccontextmanager
            async def fake_span(name):
                yield AsyncMock()

            @pytest.asynccontextmanager
            async def fake_record(metric_name, metric_type, attributes=None):
                yield AsyncMock()

            self.tracing_service.start_span.side_effect = fake_span
            self.metrics_service.arecord.side_effect = fake_record

    mock_observability_service = MockObservabilityService()

    client = TracedAsyncWebSocketClient(observability_service=mock_observability_service)

    url = "ws://example.com"
    websocket = await client.connect(url)

    mock_connect.assert_called_once_with(url)
    assert websocket == mock_websocket
    mock_logger.info.assert_called_with(f"Connecting to WebSocket {url}")
    mock_observability_service.tracing_service.start_span.assert_called_once_with(f"WS CONNECT {url}")
    mock_observability_service.metrics_service.arecord.assert_called_once_with(
        "ws_connect_duration", "histogram", attributes={"url": url}
    )


@pytest.mark.skip('need to be fixed')
@pytest.mark.asyncio
async def test_async_websocket_client_connect_failure(mocker):
    mock_connect = mocker.patch(
        "websockets.connect",
        side_effect=websockets.exceptions.WebSocketException("Connection failed")
    )
    mock_logger = mocker.patch("client_connectors.http.websocket.client._logger")

    client = AsyncWebSocketClient()
    url = "ws://example.com"

    with pytest.raises(websockets.exceptions.WebSocketException):
        await client.connect(url)

    mock_connect.assert_called_once_with(url)
    mock_logger.error.assert_called_with(f"WebSocket connection to {url} failed: Connection failed")


@pytest.mark.skip('need to be fixed')
@pytest.mark.asyncio
async def test_traced_async_websocket_client_connect_failure(mocker):
    mock_connect = mocker.patch(
        "websockets.connect",
        side_effect=websockets.exceptions.WebSocketException("Connection failed")
    )
    mock_logger = mocker.patch("client_connectors.http.websocket.client._logger")

    mock_observability_service = MockObservabilityService()
    client = TracedAsyncWebSocketClient(observability_service=mock_observability_service)

    url = "ws://example.com"
    with pytest.raises(websockets.exceptions.WebSocketException):
        await client.connect(url)

    mock_connect.assert_called_once_with(url)
    mock_logger.error.assert_called_with(f"WebSocket connection to {url} failed: Connection failed")
    mock_observability_service.tracing_service.start_span.assert_called_once_with(f"WS CONNECT {url}")
    mock_observability_service.metrics_service.arecord.assert_called_once_with(
        "ws_connect_duration", "histogram", attributes={"url": url}
    )
