import pytest

from tests.tracer.conftest import _make_service


def test_get_tracer_returns_same_instance(mocker):
    service, tracer_mock, _ = _make_service(mocker, enabled=True)
    service.tracer
    assert service.tracer is tracer_mock


@pytest.mark.asyncio
async def test_start_span_async_enabled(mocker):
    service, tracer_mock, span_obj = _make_service(mocker, enabled=True)
    async with service.start_span("async-span") as span:
        assert span is span_obj
    tracer_mock.start_as_current_span.assert_called_once_with("async-span")


@pytest.mark.asyncio
async def test_start_span_async_disabled(mocker):
    service, tracer_mock, _ = _make_service(mocker, enabled=False)
    async with service.start_span("ignored") as span:
        assert span is None
    tracer_mock.start_as_current_span.assert_not_called()


def test_start_span_sync_enabled(mocker):
    service, tracer_mock, span_obj = _make_service(mocker, enabled=True)
    with service.start_span_sync("sync-span") as span:
        assert span is span_obj
    tracer_mock.start_as_current_span.assert_called_once_with("sync-span")


def test_start_span_sync_disabled(mocker):
    service, tracer_mock, _ = _make_service(mocker, enabled=False)
    with service.start_span_sync("ignored") as span:
        assert span is None
    tracer_mock.start_as_current_span.assert_not_called()
