from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models.brand import Brand

class BrandRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(
            self,
            brand_id: UUID,
    ) -> Brand | None:
        
        statement = select(Brand).where(
            Brand.id == brand_id,
            Brand.deleted_at.is_(None),
            )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_name(
            self,
            name: str,
    ) -> Brand | None:
        statement = select(Brand).where(
            Brand.name == name,
            Brand.deleted_at.is_(None),
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        slug: str,
    ) -> Brand | None:
        statement = select(Brand).where(
            Brand.slug == slug,
            Brand.deleted_at.is_(None),
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def exists_by_name(
        self,
        name: str,
    ) -> bool:
        statement = select(Brand.id).where(
            Brand.name == name,
            Brand.deleted_at.is_(None),
        ).limit(1)

        result = await self._session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def exists_by_slug(
        self,
        slug: str,
    ) -> bool:
        statement = select(Brand.id).where(
            Brand.slug == slug,
            Brand.deleted_at.is_(None),
        ).limit(1)

        result = await self._session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def create(
        self,
        brand: Brand,
    ) -> Brand:
        self._session.add(brand)
        await self._session.flush()

        return brand

    async def update(
        self,
        brand: Brand,
    ) -> Brand:
        await self._session.flush()

        return brand