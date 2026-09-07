from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models.category import Category

class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(
        self,
        category_id: UUID,
    ) -> Category | None:
        statement = select(Category).where(
            Category.id == category_id,
            Category.deleted_at.is_(None),
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        name: str,
    ) -> Category | None:
        statement = select(Category).where(
            Category.name == name,
            Category.deleted_at.is_(None),
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        slug: str,
    ) -> Category | None:
        statement = select(Category).where(
            Category.slug == slug,
            Category.deleted_at.is_(None),
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_children(
        self,
        parent_id: UUID,
    ) -> list[Category]:
        statement = (
            select(Category)
            .where(
                Category.parent_id == parent_id,
                Category.deleted_at.is_(None),
            )
            .order_by(Category.name)
        )

        result = await self._session.execute(statement)

        return list(result.scalars().all())

    async def get_root_categories(self) -> list[Category]:
        statement = (
            select(Category)
            .where(
                Category.parent_id.is_(None),
                Category.deleted_at.is_(None),
            )
            .order_by(Category.name)
        )

        result = await self._session.execute(statement)

        return list(result.scalars().all())

    async def exists_by_slug(
        self,
        slug: str,
    ) -> bool:
        statement = select(Category.id).where(
            Category.slug == slug,
            Category.deleted_at.is_(None),
        ).limit(1)

        result = await self._session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def create(
        self,
        category: Category,
    ) -> Category:
        self._session.add(category)
        await self._session.flush()

        return category

    async def update(
        self,
        category: Category,
    ) -> Category:
        await self._session.flush()

        return category

    