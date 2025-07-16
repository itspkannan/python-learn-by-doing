import logging
from abc import ABC, abstractmethod

import httpx
from observability.metrics.decorator import record_metric_async
from observability.tracer.decorator import trace_span_async

_logger = logging.getLogger(__name__)


def http_attributes(self, method: str, url: str, **kwargs):
    return {
        "service": self.__class__.__name__,
        "http.method": method.upper(),
        "http.url": url,
    }


class AbstractBaseHttpClient(ABC):
    def __init__(self, timeout: float = 10.0):
        self.client = httpx.AsyncClient(timeout=timeout)

    @abstractmethod
    async def request(self, method: str, url: str, **kwargs):
        pass

    async def get(self, url: str, **kwargs):
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs):
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs):
        return await self.request("PUT", url, **kwargs)

    async def patch(self, url: str, **kwargs):
        return await self.request("PATCH", url, **kwargs)

    async def delete(self, url: str, **kwargs):
        return await self.request("DELETE", url, **kwargs)

    async def head(self, url: str, **kwargs):
        return await self.request("HEAD", url, **kwargs)

    async def options(self, url: str, **kwargs):
        return await self.request("OPTIONS", url, **kwargs)

    async def close(self):
        await self.client.aclose()


class AsyncHTTPClient(AbstractBaseHttpClient):
    def __int__(self, timeout: float = 10.0):
        super().__init__(timeout)

    async def request(self, method: str, url: str, **kwargs):
        try:
            response = await self.client.request(method, url, **kwargs)
            _logger.info(f"{method.upper()} {url} → {response.status_code}")
            return response
        except Exception as e:
            _logger.error(f"{method.upper()} {url} failed: {e}")
            raise


class TracedAsyncHTTPClient(AbstractBaseHttpClient):
    def __init__(self, timeout: float = 10.0):
        super().__init__(timeout)

    # @trace_span_async("HttpClient.request", attributes_fn=http_attributes)
    # @record_metric_async(
    #     name="HttpClient.request.duration",
    #     metric_type="histogram",
    #     unit="s",
    #     attributes_fn=http_attributes,
    # )
    async def request(self, method: str, url: str, **kwargs):
        response = await self.client.request(method, url, **kwargs)
        _logger.info(f"{method.upper()} {url} → {response.status_code}")
        return response
