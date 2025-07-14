import asyncio

import pytest
from unittest.mock import MagicMock, patch
from observability.metrics.service import MetricsService
from observability.config import MetricsConfig


@pytest.fixture
def mock_config():
    return MetricsConfig(enabled=True, service_name="test-service")


@pytest.fixture
def service(mock_config):
    with patch("observability.metrics.service.MetricsConfig.from_env", return_value=mock_config):
        with patch("observability.metrics.service.set_meter_provider"):
            with patch("observability.metrics.service.get_meter") as mock_get_meter:
                mock_meter = MagicMock()
                mock_get_meter.return_value = mock_meter
                yield MetricsService()


def test_record_counter(service):
    mock_counter = MagicMock()
    service.meter.create_counter.return_value = mock_counter

    with service.record("my_counter", metric_type="counter") as record_fn:
        record_fn()

    mock_counter.add.assert_called_once_with(1, {})


def test_record_histogram(service):
    mock_histogram = MagicMock()
    service.meter.create_histogram.return_value = mock_histogram

    with service.record("my_timer", metric_type="histogram") as record_fn:
        # simulate a short task
        import time

        time.sleep(0.01)
        record_fn()

    assert mock_histogram.record.call_count == 1
    recorded_value = mock_histogram.record.call_args[0][0]
    assert recorded_value > 0  # duration should be positive


@pytest.mark.asyncio
async def test_arecord_counter(service):
    mock_counter = MagicMock()
    service.meter.create_counter.return_value = mock_counter

    async with service.arecord("async_counter", metric_type="counter") as record_fn:
        record_fn()

    mock_counter.add.assert_called_once_with(1, {})


@pytest.mark.asyncio
async def test_arecord_histogram(service):
    mock_histogram = MagicMock()
    service.meter.create_histogram.return_value = mock_histogram

    async with service.arecord("async_timer", metric_type="histogram") as record_fn:
        await asyncio.sleep(0.01)
        record_fn()

    assert mock_histogram.record.call_count == 1
    recorded_value = mock_histogram.record.call_args[0][0]
    assert recorded_value > 0  # duration should be positive
