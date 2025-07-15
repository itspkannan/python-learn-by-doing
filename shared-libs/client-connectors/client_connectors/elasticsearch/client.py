from elasticsearch import AsyncElasticsearch

from client_connectors.elasticsearch.config import ElasticsearchConfig


class ESClient:
    def __init__(self, config: ElasticsearchConfig = None):
        self.config = config or ElasticsearchConfig.from_env()
        self._client = self._create_client()

    def _create_client(self) -> AsyncElasticsearch:
        scheme = "https" if self.config.use_ssl else "http"
        url = f"{scheme}://{self.config.host}:{self.config.port}"

        kwargs = {
            "hosts": [url],
            "verify_certs": self.config.use_ssl,
        }

        if self.config.username and self.config.password:
            kwargs["basic_auth"] = [self.config.username, self.config.password]

        return AsyncElasticsearch(**kwargs)

    @property
    def client(self) -> AsyncElasticsearch:
        return self._client

    async def close(self):
        await self._client.close()
