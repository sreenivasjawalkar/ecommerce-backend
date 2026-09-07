import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.users.service import UserService
from app.infrastructure.database.unit_of_work import UnitOfWork

@pytest.mark.asyncio
async def test_register_user(
    db_session: AsyncSession
):
    async with UnitOfWork(db_session) as uow:
        service = UserService(uow)

        user = await service.register_user(
            email="service@example.com",
            password="MySecurePassword123",
            first_name="Service",
            last_name="Test"
        )

        assert user.id is not None
        assert user.email == "service@example.com"
        assert user.first_name == "Service"
        assert user.password_hash != "MySecurePassword123"
        assert user.password_hash.startswith("$argon2")

@pytest.mark.asyncio
async def test_register_user_rejects_duplicate_email(
    db_session: AsyncSession,
):
    async with UnitOfWork(db_session) as uow:

        service = UserService(uow)

        await service.register_user(
            email="duplicate@example.com",
            password="test_hash",
            first_name="First",
            last_name="User",
        )

    with pytest.raises(ValueError, match="already exists"):
        async with UnitOfWork(db_session) as uow:

            service = UserService(uow)

            await service.register_user(
                email="duplicate@example.com",
                password="another_hash",
                first_name="Second",
                last_name="User",
            )