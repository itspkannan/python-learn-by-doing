import sys

import pytest
from unittest.mock import AsyncMock, MagicMock

from pydantic import BaseModel
from typing import Optional


from mongo_persistence.core.collection import MongoCollection

class FakeAsyncCursor:
    def __init__(self, docs):
        self._docs = docs

    def __aiter__(self):
        self._iter = iter(self._docs)
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration

class MockModel(BaseModel):
    id: Optional[str]
    name: str


@pytest.fixture
def mocked_collection():
    return AsyncMock()


@pytest.fixture
def mongo_wrapper(mocked_collection):
    return MongoCollection(mocked_collection, MockModel)


@pytest.mark.asyncio
async def test_insert_one(mongo_wrapper, mocked_collection):
    mocked_collection.insert_one.return_value.inserted_id = "abc123"

    obj = MockModel(id="abc123", name="Test User")
    inserted_id = await mongo_wrapper.insert_one(obj)

    assert inserted_id == "abc123"
    mocked_collection.insert_one.assert_awaited_once_with(obj.model_dump(by_alias=True))


@pytest.mark.asyncio
async def test_find_one_found(mongo_wrapper, mocked_collection):
    mocked_collection.find_one.return_value = {"id": "abc123", "name": "Test User"}

    result = await mongo_wrapper.find_one({"id": "abc123"})

    assert isinstance(result, MockModel)
    assert result.id == "abc123"
    assert result.name == "Test User"


@pytest.mark.asyncio
async def test_find_one_not_found(mongo_wrapper, mocked_collection):
    mocked_collection.find_one.return_value = None

    result = await mongo_wrapper.find_one({"id": "not_found"})

    assert result is None


@pytest.mark.asyncio
async def test_find_all(mongo_wrapper, mocked_collection):
    mocked_collection.find = lambda query={}: FakeAsyncCursor([
        {"id": "1", "name": "User1"},
        {"id": "2", "name": "User2"}
    ])

    results = await mongo_wrapper.find_all()

    assert len(results) == 2
    assert results[0].name == "User1"
    assert results[1].name == "User2"


@pytest.mark.asyncio
async def test_update_one(mongo_wrapper, mocked_collection):
    mocked_collection.update_one.return_value.modified_count = 1

    result = await mongo_wrapper.update_one({"id": "abc123"}, {"name": "Updated Name"})

    assert result == 1
    mocked_collection.update_one.assert_awaited_once_with({"id": "abc123"}, {"$set": {"name": "Updated Name"}})


@pytest.mark.asyncio
async def test_delete_one(mongo_wrapper, mocked_collection):
    mocked_collection.delete_one.return_value.deleted_count = 1

    result = await mongo_wrapper.delete_one({"id": "abc123"})

    assert result == 1
    mocked_collection.delete_one.assert_awaited_once_with({"id": "abc123"})
