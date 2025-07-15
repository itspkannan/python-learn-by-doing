from typing import Protocol


class KafkaMessageHandler(Protocol):
    async def __call__(self, key: str, value: dict) -> None: ...
