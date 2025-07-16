from motor.motor_asyncio import AsyncIOMotorClient
from service_management.core.service import Service
from service_management.core.status import HealthStatus

from .collection import MongoCollection, T
from .config import MongoConfig


class MongoAsyncClient(Service):
    def __init__(self, mongo_config: MongoConfig = None):
        super().__init__(name="MongoAsyncClient")
        self.mongo_config = mongo_config or MongoConfig.from_env()
        self.client: AsyncIOMotorClient | None = None
        self.db = None

    async def before_start(self):
        self.client = AsyncIOMotorClient(self.mongo_config.uri)
        self.db = self.client[self.mongo_config.database]
        self.health_status = HealthStatus.HEALTHY
        self.logger.info(f"Connected to MongoDB at {self.mongo_config.uri}")

    async def after_start(self):
        pass

    async def before_stop(self):
        if self.client:
            self.client.close()
            self.logger.info("MongoDB connection closed.")

    async def after_stop(self):
        pass

    def get_collection(self, name: str, model_cls: type[T]) -> MongoCollection[T]:
        return MongoCollection[T](collection=self.db[name], model_cls=model_cls)
