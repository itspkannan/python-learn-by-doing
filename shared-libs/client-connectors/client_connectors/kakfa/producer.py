
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from index_migration.kakfa.config import KafkaConfig
import json


class KafkaClient:
    def __init__(self, config: KafkaConfig = None):
        self.config = config or KafkaConfig.from_env()
        self._producer = None

    async def start(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.config.bootstrap_servers,
            security_protocol="SSL" if self.config.enable_ssl else "PLAINTEXT",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self._producer.start()

    async def send(self, key: str, value: dict):
        if not self._producer:
            raise RuntimeError("Producer not started. Call start().")
        await self._producer.send_and_wait(
            self.config.topic, key=key.encode("utf-8"), value=value
        )

    async def stop(self):
        if self._producer:
            await self._producer.stop()
