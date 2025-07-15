from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from observability.metrics.decorator import record_metric_async
from observability.tracer.decorator import trace_span_async

from service_management.core import Service, HealthStatus
from client_connectors.elasticsearch.config import ElasticsearchConfig


def es_attributes(self, **kwargs):
    return {
        "service": self.name,
        "es.index": kwargs.get("index", "unknown"),
    }


class ESClient(Service):
    def __init__(self, config: ElasticsearchConfig = None):
        super().__init__("ESClient")
        self.config = config or ElasticsearchConfig.from_env()
        self._client = None

    async def before_start(self):
        scheme = "https" if self.config.use_ssl else "http"
        url = f"{scheme}://{self.config.host}:{self.config.port}"

        kwargs = {
            "hosts": [url],
            "verify_certs": self.config.use_ssl,
        }

        if self.config.username and self.config.password:
            kwargs["basic_auth"] = [self.config.username, self.config.password]

        self._client = AsyncElasticsearch(**kwargs)
        self.health_status = HealthStatus.HEALTHY

    async def after_start(self):
        pass

    async def before_stop(self):
        pass

    async def after_stop(self):
        if self._client:
            await self._client.close()

    @trace_span_async("ESClient.index", attributes_fn=es_attributes)
    @record_metric_async("ESClient.index.duration", "histogram", attributes_fn=es_attributes)
    async def index_document(self, index: str, doc_id: str, document: dict):
        await self._client.index(index=index, id=doc_id, document=document)
        self.increment_events()

    @trace_span_async("ESClient.get", attributes_fn=es_attributes)
    @record_metric_async("ESClient.get.duration", "histogram", attributes_fn=es_attributes)
    async def get_by_id(self, index: str, doc_id: str):
        return await self._client.get(index=index, id=doc_id)

    @trace_span_async("ESClient.search", attributes_fn=es_attributes)
    @record_metric_async("ESClient.search.duration", "histogram", attributes_fn=es_attributes)
    async def search(self, index: str, query: dict, size: int = 10):
        return await self._client.search(index=index, query=query, size=size)

    @trace_span_async("ESClient.bulk_index", attributes_fn=es_attributes)
    @record_metric_async("ESClient.bulk_index.duration", "histogram", attributes_fn=es_attributes)
    async def bulk_index(self, index: str, documents: list[dict]):
        actions = [{"_index": index, "_source": doc} for doc in documents]
        await async_bulk(self._client, actions)
        self.increment_events(count=len(documents))
