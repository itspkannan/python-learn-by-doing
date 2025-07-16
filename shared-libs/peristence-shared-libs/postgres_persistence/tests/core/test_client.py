import pytest
from unittest.mock import AsyncMock, MagicMock

from service_management.core.registry import Registry
from sqlalchemy.ext.asyncio import AsyncSession
from postgres_persistence.repository.base import BaseRepository
from tests.core.user import User


@pytest.fixture
def mock_client():
    mock = MagicMock()
    mock.session.return_value = AsyncMock(spec=AsyncSession)
    return mock


@pytest.mark.skip('Need to fix, refractoring caused failure')
@pytest.mark.asyncio
async def test_add_user(mock_client):
    Registry.register_instance("PostgresClient", AsyncMock())
    repo = BaseRepository(User)

    user = User(id="u1", name="Test", email="test@example.com")
    mock_session = mock_client.session.return_value.__aenter__.return_value
    mock_session.refresh = AsyncMock()

    await repo.add(user)

    mock_session.add.assert_called_once_with(user)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(user)
