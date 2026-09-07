import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.unit_of_work import UnitOfWork
from app.infrastructure.database.models.user import User, UserRole
@pytest.mark.asyncio
async def test_unit_of_work_commits(db_session: AsyncSession):

    async with UnitOfWork(db_session) as uow:

        user = User(
            email="uow@example.com",
            password_hash="test_hash",
            first_name="Unit",
            last_name="Test",
            role=UserRole.CUSTOMER,
            is_active=True
        )

        await uow.users.create_user(user)

    result = await db_session.get(User, user.id)

    assert result is not None
    assert result.email == "uow@example.com"


@pytest.mark.asyncio
async def test_unit_of_work_rolls_back(db_session: AsyncSession):
    with pytest.raises(RuntimeError):
        async with UnitOfWork(db_session) as uow:

            user = User(
                        email="rollback@example.com",
                        password_hash="test_hash",
                        first_name="Rollback",
                        last_name="Test",
                        role=UserRole.CUSTOMER,
                        is_active=True
                    )

            await uow.users.create_user(user)

            raise RuntimeError("Something went wrong")

    result = await db_session.get(User, user.id)

    assert result is None

            
