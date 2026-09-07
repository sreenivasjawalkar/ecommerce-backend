from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models.product import Product

class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(
        self,
        product_id: UUID,
    ) -> Product | None:
        statement = select(Product).where(
            Product.id == product_id,
            Product.deleted_at.is_(None),
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_sku(
        self,
        sku: str,
    ) -> Product | None:
        statement = select(Product).where(
            Product.sku == sku,
            Product.deleted_at.is_(None),
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        slug: str,
    ) -> Product | None:
        statement = select(Product).where(
            Product.slug == slug,
            Product.deleted_at.is_(None),
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def exists_by_sku(
        self,
        sku: str,
    ) -> bool:
        statement = select(Product.id).where(
            Product.sku == sku,
            Product.deleted_at.is_(None),
        ).limit(1)

        result = await self._session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def exists_by_slug(
        self,
        slug: str,
    ) -> bool:
        statement = select(Product.id).where(
            Product.slug == slug,
            Product.deleted_at.is_(None),
        ).limit(1)

        result = await self._session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def create(
        self,
        product: Product,
    ) -> Product:
        self._session.add(product)
        await self._session.flush()

        return product
