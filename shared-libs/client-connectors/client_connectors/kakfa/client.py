import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from service_management.service import Service
from service_management.status import HealthStatus

from client_connectors.kakfa.config import KafkaConfig


class KafkaConsumerClient(Service):
    def __init__(self, config: KafkaConfig = None):
        super().__init__("KafkaConsumerClient")
        self.config = config or KafkaConfig.from_env()
        self._consumer = None
        self._consumer = None
        self._running = False

    async def start(self):
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

    async def consume(self, handler):
        if not self._consumer:
            raise RuntimeError("Consumer not started. Call start() first.")
        try:
            while self._running:
                async for msg in self._consumer:
                    await handler(msg.key.decode("utf-8"), msg.value)
                    if not self._running:
                        break
        finally:
            await self._consumer.stop()

    async def stop(self):
        self._running = False


from opentelemetry import trace

class KafkaProducerClient(Service):
    def __init__(self, config: KafkaProducerClient = None):
        super().__init__("KafkaClient")
        self.config = config or KafkaConfig.from_env()
        self._producer = None

    async def start(self):
        await super().start()
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

    async def send(self, key: str, value: dict):
        if not self._producer:
            raise RuntimeError("Producer not started. Call start().")

        async with self.tracer.start_as_current_span("KafkaClient.send") as span:
            span.set_attribute("messaging.system", "kafka")
            span.set_attribute("messaging.destination", self.config.topic)
            span.set_attribute("messaging.kafka.message_key", key)

            await self._producer.send_and_wait(
                self.config.topic,
                key=key.encode("utf-8"),
                value=value,
            )

            self.increment_events()
            if self.metrics:
                with self.metrics.record(
                    name=f"{self.name}.events.count",
                    metric_type="counter",
                    attributes={"topic": self.config.topic}
                ) as inc:
                    inc()

