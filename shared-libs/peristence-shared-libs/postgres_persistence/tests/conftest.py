from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
def mock_client():
    session = MagicMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock()

    client = MagicMock()
    client.session.return_value.__aenter__.return_value = session
    return client
