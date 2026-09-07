from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

import pytest


@pytest.mark.asyncio
async def test_database_connection(db_engine: AsyncEngine):
    async with db_engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))

        assert result.scalar_one() == 1