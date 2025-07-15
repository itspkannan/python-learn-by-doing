import pytest
from testcontainers.mongodb import MongoDbContainer
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional

from mongo_persistence.core.collection import MongoCollection


class Group(BaseModel):
    id: str = Field(alias="_id")
    name: str


class UserWithGroup(BaseModel):
    id: str = Field(alias="_id")
    name: str
    group_id: str
    group_info: Group


@pytest.mark.asyncio
async def test_aggregate_lookup_result_model():
    with MongoDbContainer("mongo:6.0") as mongo:
        uri = mongo.get_connection_url()
        db_name = "test_db"

        client = AsyncIOMotorClient(uri)
        db = client[db_name]

        users_coll = MongoCollection(db["users"], UserWithGroup)
        groups_coll = MongoCollection(db["groups"], Group)

        # Insert related group
        await groups_coll.collection.insert_one({"_id": "g1", "name": "Engineering"})

        # Insert user referencing group
        await users_coll.collection.insert_one({
            "_id": "u1",
            "name": "Priyesh",
            "group_id": "g1"
        })

        # Aggregation with $lookup and $unwind
        pipeline = [
            {
                "$lookup": {
                    "from": "groups",
                    "localField": "group_id",
                    "foreignField": "_id",
                    "as": "group_info"
                }
            },
            {"$unwind": "$group_info"}
        ]

        results = await users_coll.aggregate(pipeline, result_model=UserWithGroup)

        assert len(results) == 1
        assert isinstance(results[0], UserWithGroup)
        assert results[0].name == "Priyesh"
        assert results[0].group_info.name == "Engineering"

        client.close()
