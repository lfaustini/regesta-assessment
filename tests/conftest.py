from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@pytest.fixture(scope="session")
async def database() -> AsyncGenerator[async_sessionmaker[AsyncSession]]:
    db_file = (Path(__file__).parent / "test-db.sqlite").resolve()
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_file}")
    yield async_sessionmaker(engine)
    await engine.dispose()
