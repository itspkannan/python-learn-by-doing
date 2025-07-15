import json
from unittest.mock import AsyncMock

import pytest
from client_connectors.kakfa.client import KafkaConsumerClient, KafkaProducerClient
from client_connectors.kakfa.config import KafkaConfig


@pytest.mark.asyncio
async def test_kafka_producer_send(mocker):
    mock_producer = AsyncMock()
    mock_start = mocker.patch("aiokafka.AIOKafkaProducer.start", new=mock_producer.start)
    mock_send_and_wait = mocker.patch(
        "aiokafka.AIOKafkaProducer.send_and_wait", new=mock_producer.send_and_wait
    )
    mock_stop = mocker.patch("aiokafka.AIOKafkaProducer.stop", new=mock_producer.stop)

    config = KafkaConfig(
        bootstrap_servers="localhost:9092",
        topic="test-topic",
        group_id="test-group",
        enable_ssl=False,
    )
    producer = KafkaProducerClient(config)

    await producer.start()
    await producer.send("test-key", {"msg": "hello"})
    await producer.stop()

    mock_start.assert_called_once()
    mock_send_and_wait.assert_called_once_with(
        config.topic, key=b"test-key", value={"msg": "hello"}
    )
    mock_stop.assert_called_once()


@pytest.mark.asyncio
async def test_kafka_consumer_receive(mocker):
    # Create a mock consumer instance
    mock_consumer_instance = AsyncMock()
    mock_consumer_instance.__aiter__.return_value = [
        AsyncMock(key=b"key1", value=json.dumps({"event": "test"}).encode("utf-8"))
    ]

    # Patch the constructor to return our mock instance
    mocker.patch(
        "client_connectors.kakfa.client.AIOKafkaConsumer", return_value=mock_consumer_instance
    )

    # Create the consumer client (this will use the patched class)
    consumer = KafkaConsumerClient(
        KafkaConfig(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="test-group",
            enable_ssl=False,
        )
    )

    await consumer.start()

    received = {}

    async def handler(key, value):
        received["key"] = key
        received["value"] = value
        await consumer.stop()

    await consumer.consume(handler)

    assert received["key"] == "key1"
    assert received["value"] == b'{"event": "test"}'
    mock_consumer_instance.start.assert_called_once()
    mock_consumer_instance.stop.assert_called_once()
