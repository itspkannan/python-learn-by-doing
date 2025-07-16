import logging

from service_management.core.service import Service
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from .config import PostgresConfig

logger = logging.getLogger(__name__)


class PostgresClient(Service):
    def __init__(self, config: PostgresConfig | None = None):
        super().__init__("PostgresClient")
        self.config = config or PostgresConfig.from_env()
        self.engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker[AsyncSession] | None = None

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(OperationalError),
        reraise=True,
    )
    async def before_start(self):
        logger.info(f"Creating engine with URI: {self.config.uri}")
        logger.info("Initializing PostgresClient with retry and connection pooling")
        self.engine = create_async_engine(
            self.config.uri,
            echo=False,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            future=True,
        )
        self._session_maker = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def after_start(self):
        pass

    async def before_stop(self):
        if self.engine:
            logger.info("Shutting down Postgres engine")
            await self.engine.dispose()

    async def after_stop(self):
        pass

    def session(self) -> AsyncSession:
        if not self._session_maker:
            raise RuntimeError("PostgresClient not initialized. Call init() first.")
        return self._session_maker()
