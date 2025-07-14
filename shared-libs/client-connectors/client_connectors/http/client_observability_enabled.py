import httpx

from observability.observability_service import ObservabilityService


import logging

_logger = logging.getLogger(__name__)


class TracedAsyncHTTPClient:
    def __init__(
        self, observability_service: ObservabilityService, timeout: float = 10.0
    ):
        self.client = httpx.AsyncClient(timeout=timeout)
        self.observability_service = observability_service

    async def request(self, method: str, url: str, **kwargs):
        async with self.observability_service.metrics_service.arecord(
            f"http_{method.lower()}_duration",
            "histogram",
            attributes={"method": method.upper(), "url": url},
        ) as record:
            try:
                response = await self.client.request(method, url, **kwargs)
                _logger.info(f"{method.upper()} {url} → {response.status_code}")
                record()
                return response
            except Exception as e:
                _logger.error(f"{method.upper()} {url} failed: {e}")
                raise

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
