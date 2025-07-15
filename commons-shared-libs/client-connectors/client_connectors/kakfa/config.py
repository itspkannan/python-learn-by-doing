import os
from dataclasses import dataclass


def str_to_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes")


@dataclass(frozen=True)
class KafkaConfig:
    bootstrap_servers: str
    topic: str
    group_id: str
    enable_ssl: bool

    @staticmethod
    def from_env() -> "KafkaConfig":
        return KafkaConfig(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            topic=os.getenv("KAFKA_TOPIC", "company_news"),
            group_id=os.getenv("KAFKA_GROUP_ID", "default-group"),
            enable_ssl=os.getenv("KAFKA_ENABLE_SSL", "false").lower() in ("1", "true", "yes", "on"),
        )
