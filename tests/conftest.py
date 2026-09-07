import pytest_asyncio
from app.main import app
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
)
from app.core.config import settings
from collections.abc import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from app.infrastructure.database.session import engine
from app.infrastructure.database.session import get_db_session


@pytest_asyncio.fixture
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(
    db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:

    async with db_engine.connect() as connection:

        transaction = await connection.begin()

        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        try:
            yield session

        finally:
            await session.close()
            await transaction.rollback()

@pytest_asyncio.fixture
async def client(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:

    async def override_get_db_session():
        yield db_session

    app.dependency_overrides[
        get_db_session
    ] = override_get_db_session

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test",) as client:
        yield client

    app.dependency_overrides.clear()