import contextlib
from types import SimpleNamespace
from unittest.mock import MagicMock

from observability.tracer.service import TracingService


@contextlib.contextmanager
def _dummy_span_cm(span_obj):
    yield span_obj


def _make_service(mocker, *, enabled: bool):
    tracer_mock = MagicMock(name="tracer")
    fake_span = object()
    tracer_mock.start_as_current_span.return_value = _dummy_span_cm(fake_span)

    # Patch everything using mocker
    mocker.patch("opentelemetry.sdk.trace.TracerProvider")
    mocker.patch("opentelemetry.sdk.trace.export.SimpleSpanProcessor")
    mocker.patch("opentelemetry.sdk.trace.export.ConsoleSpanExporter")
    mocker.patch("opentelemetry.trace.set_tracer_provider")
    mocker.patch("opentelemetry.trace.get_tracer", return_value=tracer_mock)

    cfg = SimpleNamespace(service_name="svc", enabled=enabled)
    return TracingService(cfg), tracer_mock, fake_span
