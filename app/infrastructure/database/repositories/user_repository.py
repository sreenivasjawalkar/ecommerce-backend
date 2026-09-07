from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models.user import User

class UserRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        result = await self._session.execute(
            select(User.id).where(User.email == email)
        )

        return result.scalar_one_or_none() is not None

    async def create_user(self, user: User) -> User:
        self._session.add(user)

        await self._session.flush()

        return user

    async def update_user(self, user: User) -> User:
        self._session.add(user)

        await self._session.flush()

        return user

    async def delete_user(self, user: User) -> None:
        await self._session.delete(user)

        await self._session.flush()

    async def list_users(
            self,
            *,
            offset: int,
            limit: int,
    ) -> tuple[list[User], int]:

        statement = (
            select(User)
            .order_by(User.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self._session.execute(statement)

        users = list(result.scalars().all())

        count_statement = select(func.count()).select_from(User)

        total = await self._session.scalar(count_statement)

        return users, total or 0


