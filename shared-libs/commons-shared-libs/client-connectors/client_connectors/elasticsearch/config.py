from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ElasticsearchConfig:
    host: str
    port: int
    username: str
    password: str
    use_ssl: bool

    @staticmethod
    def from_env() -> ElasticsearchConfig:
        return ElasticsearchConfig(
            host=os.getenv("ES_HOST", "localhost"),
            port=int(os.getenv("ES_PORT", 9200)),
            username=os.getenv("ES_USERNAME", "elastic"),
            password=os.getenv("ES_PASSWORD", "changeme"),
            use_ssl=os.getenv("ES_USE_SSL", "false").lower() in ("1", "true", "yes", "on"),
        )
