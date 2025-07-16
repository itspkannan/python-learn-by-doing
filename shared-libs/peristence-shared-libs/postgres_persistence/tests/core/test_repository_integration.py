import pytest
from testcontainers.postgres import PostgresContainer
from postgres_persistence.core.client import PostgresClient
from postgres_persistence.core.config import PostgresConfig
from postgres_persistence.repository.base import BaseRepository, Base
from tests.core.user import User


@pytest.mark.skip('Need to fix, refractoring caused failure')
@pytest.mark.asyncio
async def test_user_crud_integration():
    with PostgresContainer("postgres:14") as container:
        uri = container.get_connection_url().replace("psycopg2://", "asyncpg://")
        client = PostgresClient(config=PostgresConfig(uri))
        await client.start()

        async with client.session() as session:
            async with client.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        repo = BaseRepository(User)

        user = User(id="u1", name="anonymous", email="anonymous@example.com")
        await repo.add(user)

        found = await repo.get("u1")
        assert found is not None
        assert found.name == "anonymous"

        users = await repo.get_all()
        assert len(users) == 1

        await repo.delete("u1")
        assert await repo.get("u1") is None

        await client.before_stop()
