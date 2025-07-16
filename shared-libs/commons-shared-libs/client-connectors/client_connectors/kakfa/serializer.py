import json
from typing import Any, Union

try:
    from pydantic import BaseModel
    HAS_PYDANTIC = True
except ImportError:
    BaseModel = object
    HAS_PYDANTIC = False

try:
    from dataclasses import is_dataclass, asdict
    HAS_DATACLASSES = True
except ImportError:
    is_dataclass = lambda x: False
    HAS_DATACLASSES = False


class KafkaSerializer:
    @staticmethod
    def serialize(value: Union[Any, dict, str]) -> bytes:
        if HAS_PYDANTIC and isinstance(value, BaseModel):
            return value.json().encode("utf-8")

        if HAS_DATACLASSES and is_dataclass(value):
            return json.dumps(asdict(value)).encode("utf-8")

        if isinstance(value, dict):
            return json.dumps(value).encode("utf-8")

        if isinstance(value, str):
            try:
                json.loads(value)
                return value.encode("utf-8")
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string passed to Kafka")

        raise TypeError(f"Unsupported type {type(value)} passed to Kafka serializer")
