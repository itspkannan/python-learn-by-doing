from typing import Generic

from mongo_persistence.core.client import MongoAsyncClient
from mongo_persistence.core.collection import MongoCollection, T


class BaseRepository(Generic[T]):
    def __init__(self, client: MongoAsyncClient, model_cls: type[T], collection_name: str):
        self.model_cls = model_cls
        self.collection_name = collection_name
        self.collection: MongoCollection[T] = client.get_collection(collection_name, model_cls)

    async def insert(self, obj: T) -> str:
        return await self.collection.insert_one(obj)

    async def find(self, query_filter: dict) -> T | None:
        return await self.collection.find_one(query_filter)

    async def find_all(self, query_filter: dict | None = None) -> list[T]:
        query_filter = query_filter if query_filter else {}
        return await self.collection.find_all(query_filter)

    async def update(self, query_filter: dict, update: dict) -> int:
        return await self.collection.update_one(query_filter, update)

    async def delete(self, query_filter: dict) -> int:
        return await self.collection.delete_one(query_filter)
