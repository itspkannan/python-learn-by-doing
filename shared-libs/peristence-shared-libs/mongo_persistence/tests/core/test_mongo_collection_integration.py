import pytest
from testcontainers.mongodb import MongoDbContainer
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional

from mongo_persistence.core.collection import MongoCollection


class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: str

@pytest.mark.asyncio
async def test_mongo_collection_end_to_end():
    with MongoDbContainer("mongo:6.0") as mongo:
        uri = mongo.get_connection_url()
        db_name = "test_db"

        client = AsyncIOMotorClient(uri)
        db = client[db_name]
        collection = db["users"]

        mongo_coll = MongoCollection(collection, User)

        user = User(name="anonymous", email="anonymous@example.com")
        user_id = await mongo_coll.insert_one(user)
        assert user_id

        fetched = await mongo_coll.find_one({"name": "anonymous"})
        assert fetched is not None
        assert fetched.name == "anonymous"
        assert fetched.email == "anonymous@example.com"

        all_users = await mongo_coll.find_all()
        assert len(all_users) == 1
        assert all_users[0].name == "anonymous"

        modified_count = await mongo_coll.update_one(
            {"name": "anonymous"}, {"email": "updated@example.com"}
        )
        assert modified_count == 1

        updated = await mongo_coll.find_one({"name": "anonymous"})
        assert updated.email == "updated@example.com"

        deleted_count = await mongo_coll.delete_one({"name": "anonymous"})
        assert deleted_count == 1

        assert await mongo_coll.find_one({"name": "anonymous"}) is None

        client.close()
