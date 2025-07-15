
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from index_migration.kakfa.config import KafkaConfig
import json


class KafkaClient:
    def __init__(self, config: KafkaConfig = None):
        self.config = config or KafkaConfig.from_env()
        self._producer = None
        self._consumer = None

    async def start_producer(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.config.bootstrap_servers,
            security_protocol="SSL" if self.config.enable_ssl else "PLAINTEXT",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self._producer.start()

    async def send(self, key: str, value: dict):
        if not self._producer:
            raise RuntimeError("Producer not started. Call start_producer() first.")
        await self._producer.send_and_wait(
            self.config.topic, key=key.encode("utf-8"), value=value
        )

    async def stop_producer(self):
        if self._producer:
            await self._producer.stop()

    async def start_consumer(self):
        self._consumer = AIOKafkaConsumer(
            self.config.topic,
            bootstrap_servers=self.config.bootstrap_servers,
            group_id=self.config.group_id,
            security_protocol="SSL" if self.config.enable_ssl else "PLAINTEXT",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
        )
        await self._consumer.start()

    async def consume(self, handler):
        if not self._consumer:
            raise RuntimeError("Consumer not started. Call start_consumer() first.")
        try:
            async for msg in self._consumer:
                await handler(msg.key.decode("utf-8"), msg.value)
        finally:
            await self._consumer.stop()
