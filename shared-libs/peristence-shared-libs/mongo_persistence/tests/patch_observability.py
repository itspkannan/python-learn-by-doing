import sys
from unittest.mock import MagicMock

sys.modules['observability.metrics.decorator'] = MagicMock()
sys.modules['observability.tracer.decorator'] = MagicMock()

sys.modules['observability.metrics.decorator'].record_metric_async = lambda *a, **kw: lambda f: f
sys.modules['observability.tracer.decorator'].trace_span_async = lambda *a, **kw: lambda f: f
