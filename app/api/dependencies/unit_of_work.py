from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db_session
from app.infrastructure.database.unit_of_work import UnitOfWork


async def get_unit_of_work(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> AsyncIterator[UnitOfWork]:

    async with UnitOfWork(session) as uow:
        yield uow