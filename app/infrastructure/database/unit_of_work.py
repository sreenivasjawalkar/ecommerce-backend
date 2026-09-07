from typing import Self
from types import TracebackType
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.infrastructure.database.repositories.brand_repository import BrandRepository
from app.infrastructure.database.repositories.product_repository import ProductRepository
from app.infrastructure.database.repositories.category_repository import CategoryRepository
class UnitOfWork:
    """
    Coordinates database repositories and transaction boundaries.

    The UnitOfWork owns the database transaction.
    Repositories perform persistence operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.users = UserRepository(session)
        self.brand = BrandRepository(session)
        self.products = ProductRepository(session)
        self.category = CategoryRepository(session)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None
            ) -> None:

        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        """
        Commit the current transaction.
        """
        await self._session.commit()

    async def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        await self._session.rollback()

