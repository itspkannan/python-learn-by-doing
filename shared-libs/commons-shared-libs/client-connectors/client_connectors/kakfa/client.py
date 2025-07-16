import json
from typing import Any

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from observability.metrics.decorator import record_metric_async
from observability.tracer.decorator import trace_span_async
from service_management.core.service import Service
from service_management.core.status import HealthStatus

from client_connectors.kakfa.config import KafkaConfig
from client_connectors.kakfa.interfaces import KafkaMessageHandler
from client_connectors.kakfa.serializer import KafkaSerializer


def kafka_attributes(self, key: str, value: dict):
    return {
        "service": self.name,
        "messaging.system": "kafka",
        "messaging.destination": self.config.topic,
        "messaging.kafka.message_key": key,
    }


class KafkaConsumerClient(Service):
    def __init__(self, config: KafkaConfig = None):
        super().__init__("KafkaConsumerClient")
        self.config = config or KafkaConfig.from_env()
        self._consumer = None
        self._running = False

    async def before_start(self):
        self._consumer = AIOKafkaConsumer(
            self.config.topic,
            bootstrap_servers=self.config.bootstrap_servers,
            group_id=self.config.group_id,
            security_protocol="SSL" if self.config.enable_ssl else "PLAINTEXT",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        await self._consumer.start()
        self._running = True

    async def after_start(self):
        pass

    async def before_stop(self):
        if self._consumer:
            await self._consumer.stop()
        self._running = False

    async def after_stop(self):
        pass

    @trace_span_async("KafkaConsumerClient.consume")
    @record_metric_async(name="KafkaConsumerClient.events.consumed", metric_type="counter")
    async def consume_message(self, key: str, value: dict):
        self.increment_events()
        self.logger.info(f"Consumed message key={key}")

    async def consume(self, handler: KafkaMessageHandler = None):
        if not self._consumer:
            raise RuntimeError("Consumer not started. Call start() first.")

        handler = handler or self.consume_message

        try:
            while self._running:
                async for msg in self._consumer:
                    await handler(msg.key.decode("utf-8"), msg.value)
                    if not self._running:
                        break
        except Exception as e:
            self.logger.exception("Error during consumption: %s", e)


class KafkaProducerClient(Service):
    def __init__(self, config: KafkaConfig = None):
        super().__init__("KafkaClient")
        self.config = config or KafkaConfig.from_env()
        self._producer = None
        self.serializer = KafkaSerializer()

    async def before_start(self):
        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.config.bootstrap_servers,
                security_protocol="SSL" if self.config.enable_ssl else "PLAINTEXT",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            await self._producer.start()
            self.health_status = HealthStatus.HEALTHY
        except Exception as e:
            self.health_status = HealthStatus.ERROR
            self.logger.error(f"Failed to start KafkaProducer: {e}")
            raise e

    async def after_start(self):
        pass

    async def before_stop(self):
        if self._producer:
            await self._producer.stop()

    async def after_stop(self):
        pass

    @trace_span_async("KafkaProducerClient.send", attributes_fn=kafka_attributes)
    @record_metric_async(
        name="KafkaProducerClient.events.sent",
        metric_type="counter",
        attributes_fn=kafka_attributes,
    )
    async def send(self, key: str, value: Any):
        if not self._producer:
            raise RuntimeError("Producer not started")

        serialized_value = self.serializer.serialize(value)

        await self._producer.send_and_wait(
            topic=self.topic,
            key=key.encode("utf-8"),
            value=serialized_value,
        )
