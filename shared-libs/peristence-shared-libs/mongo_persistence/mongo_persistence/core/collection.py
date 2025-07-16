from typing import Any, Generic, TypeVar

from motor.motor_asyncio import AsyncIOMotorCollection
from observability.metrics.decorator import record_metric_async
from observability.tracer.decorator import trace_span_async
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
AggT = TypeVar("AggT", bound=BaseModel)


def mongo_attrs(self, *args, **kwargs):
    return {
        "collection": self.collection.name,
        "model": self.model_cls.__name__,
    }


class MongoCollection(Generic[T]):
    def __init__(self, collection: AsyncIOMotorCollection, model_cls: type[T]):
        self.collection = collection
        self.model_cls = model_cls

    @trace_span_async("MongoCollection.insert_one", attributes_fn=mongo_attrs)
    @record_metric_async(
        "MongoCollection.insert.count", metric_type="counter", attributes_fn=mongo_attrs
    )
    async def insert_one(self, obj: T) -> str:
        result = await self.collection.insert_one(obj.model_dump(by_alias=True))
        return str(result.inserted_id)

    @trace_span_async("MongoCollection.find_one", attributes_fn=mongo_attrs)
    async def find_one(self, query: dict[str, Any]) -> T | None:
        doc = await self.collection.find_one(query)
        return self.model_cls.model_validate(doc) if doc else None

    @trace_span_async("MongoCollection.find_all", attributes_fn=mongo_attrs)
    async def find_all(self, query: dict[str, Any] = {}) -> list[T]:
        cursor = self.collection.find(query)
        return [self.model_cls.model_validate(doc) async for doc in cursor]

    @trace_span_async("MongoCollection.update_one", attributes_fn=mongo_attrs)
    @record_metric_async(
        "MongoCollection.delete.count", metric_type="counter", attributes_fn=mongo_attrs
    )
    async def update_one(self, query: dict[str, Any], update: dict[str, Any]) -> int:
        result = await self.collection.update_one(query, {"$set": update})
        return result.modified_count

    @trace_span_async("MongoCollection.delete_one", attributes_fn=mongo_attrs)
    @record_metric_async(
        "MongoCollection.delete.count", metric_type="counter", attributes_fn=mongo_attrs
    )
    async def delete_one(self, query: dict[str, Any]) -> int:
        result = await self.collection.delete_one(query)
        return result.deleted_count

    @trace_span_async("MongoCollection.aggregate", attributes_fn=mongo_attrs)
    async def aggregate(
        self,
        pipeline: list[dict],
        result_model: type[AggT] | None = None,
    ) -> list[AggT] | list[T] | list[dict]:
        cursor = self.collection.aggregate(pipeline)
        model = result_model or self.model_cls

        if model:
            return [model.model_validate(doc) async for doc in cursor]
        return [doc async for doc in cursor]
