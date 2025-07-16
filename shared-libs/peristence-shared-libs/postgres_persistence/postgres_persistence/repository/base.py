from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import Row, RowMapping, select
from sqlalchemy.orm import DeclarativeBase

from postgres_persistence.core.client import PostgresClient


class Base(DeclarativeBase):
    pass


T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model: type[T], client: PostgresClient):
        self.model = model
        self.client = client

    async def get(self, id: str) -> T | None:
        async with self.client.session() as session:
            return await session.get(self.model, id)

    async def get_all(self) -> Sequence[Row[Any] | RowMapping | Any]:
        async with self.client.session() as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()

    async def add(self, obj: T) -> T:
        async with self.client.session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    async def delete(self, id: str) -> None:
        async with self.client.session() as session:
            obj = await session.get(self.model, id)
            if obj:
                await session.delete(obj)
                await session.commit()
