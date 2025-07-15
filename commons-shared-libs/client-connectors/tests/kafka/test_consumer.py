import pytest

from client_connectors.kakfa.client import KafkaConsumerClient
from client_connectors.kakfa.config import KafkaConfig


class MockHandler:
    def __init__(self):
        self.calls = []

    async def __call__(self, key: str, value: dict):
        self.calls.append((key, value))


@pytest.mark.asyncio
async def test_consume_message_interface():
    config = KafkaConfig(
        bootstrap_servers="localhost:9092",
        topic="test-topic",
        group_id="test-group",
        enable_ssl=False,
    )

    client = KafkaConsumerClient(config=config)
    handler = MockHandler()

    await client.start()
    await client.consume_message("sample-key", {"hello": "world"})

    assert handler.calls == []  # Not called directly
    await client.stop()
