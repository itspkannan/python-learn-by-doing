from unittest.mock import AsyncMock

import pytest
from client_connectors.elasticsearch.client import ESClient
from client_connectors.elasticsearch.config import ElasticsearchConfig


@pytest.mark.asyncio
async def test_es_client_creation_and_close(mocker):
    mock_es_instance = AsyncMock()
    mock_es_constructor = mocker.patch(
        "client_connectors.elasticsearch.client.AsyncElasticsearch", return_value=mock_es_instance
    )

    config = ElasticsearchConfig(
        host="localhost", port=9200, username="elastic", password="changeme", use_ssl=False
    )

    client = ESClient(config)

    mock_es_constructor.assert_called_once_with(
        hosts=["http://localhost:9200"], verify_certs=False, basic_auth=["elastic", "changeme"]
    )

    await client.close()

    mock_es_instance.close.assert_awaited_once()
