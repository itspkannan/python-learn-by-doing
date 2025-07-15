import os
from dataclasses import dataclass


@dataclass(frozen=True)
class PostgresConfig:
    uri: str

    @staticmethod
    def from_env() -> "PostgresConfig":
        return PostgresConfig(
            uri=os.getenv("POSTGRES_URI", "postgresql+asyncpg://user:pass@localhost:5432/mydb")
        )
