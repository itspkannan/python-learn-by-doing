from unittest.mock import AsyncMock

import pytest
from client_connectors.http import AsyncHTTPClient, TracedAsyncHTTPClient


@pytest.mark.asyncio
async def test_async_http_client_get(mocker):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = "OK"

    mock_request = mocker.patch("httpx.AsyncClient.request", return_value=mock_response)

    client = AsyncHTTPClient(timeout=5.0)

    url = "http://example.com"
    response = await client.get(url)

    mock_request.assert_called_once_with("GET", url)
    assert response.status_code == 200
    assert response.text == "OK"


@pytest.mark.skip("need to be fixed")
@pytest.mark.asyncio
async def test_traced_async_http_client_get(mocker):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = "OK"

    mock_observability_service = mocker.Mock()
    mock_metrics_service = mocker.Mock()
    mock_observability_service.metrics_service = mock_metrics_service
    mock_metrics_service.arecord = AsyncMock()

    mock_request = mocker.patch("httpx.AsyncClient.request", return_value=mock_response)

    client = TracedAsyncHTTPClient(observability_service=mock_observability_service, timeout=5.0)

    url = "http://example.com"
    response = await client.get(url)

    mock_request.assert_called_once_with("GET", url)
    assert response.status_code == 200
    assert response.text == "OK"
    mock_observability_service.metrics_service.arecord.assert_called_once()


@pytest.mark.asyncio
async def test_async_http_client_post(mocker):
    mock_response = AsyncMock()
    mock_response.status_code = 201
    mock_response.text = "Created"

    mock_request = mocker.patch("httpx.AsyncClient.request", return_value=mock_response)

    client = AsyncHTTPClient(timeout=5.0)

    url = "http://example.com"
    response = await client.post(url, data={"key": "value"})

    mock_request.assert_called_once_with("POST", url, data={"key": "value"})
    assert response.status_code == 201
    assert response.text == "Created"


@pytest.mark.skip("need to be fixed")
@pytest.mark.asyncio
async def test_traced_async_http_client_post(mocker):
    mock_response = AsyncMock()
    mock_response.status_code = 201
    mock_response.text = "Created"

    mock_observability_service = mocker.Mock()
    mock_metrics_service = mocker.Mock()
    mock_observability_service.metrics_service = mock_metrics_service
    mock_metrics_service.arecord = AsyncMock()

    mock_request = mocker.patch("httpx.AsyncClient.request", return_value=mock_response)

    client = TracedAsyncHTTPClient(observability_service=mock_observability_service, timeout=5.0)

    url = "http://example.com"
    response = await client.post(url, data={"key": "value"})

    mock_request.assert_called_once_with("POST", url, data={"key": "value"})
    assert response.status_code == 201
    assert response.text == "Created"
    mock_observability_service.metrics_service.arecord.assert_called_once()
