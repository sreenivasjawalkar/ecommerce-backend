import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.user import User, UserRole
from app.infrastructure.database.repositories.user_repository import UserRepository

#Test by id
@pytest.mark.asyncio
async def test_get_user_by_id(
    db_session: AsyncSession,
):
    repository = UserRepository(db_session)

    user = User(
        email="getbyid@example.com",
        password_hash="test_hash",
        first_name="Get",
        last_name="ById",
        role=UserRole.CUSTOMER,
        is_active=True,
    )

    db_session.add(user)
    await db_session.flush()

    result = await repository.get_by_id(user.id)

    assert result is not None
    assert result.id == user.id
    assert result.email == "getbyid@example.com"


@pytest.mark.asyncio
async def test_get_user_by_email(db_session: AsyncSession):
    repository = UserRepository(db_session)

    user = User(
        email="repository@example.com",
        password_hash="test_hash",
        first_name="Repository",
        last_name="Test",
        role=UserRole.CUSTOMER,
        is_active=True
    )

    db_session.add(user)
    await db_session.flush()

    result = await repository.get_by_email(
        "repository@example.com"
    )

    assert result is not None
    assert result.email == "repository@example.com"\

@pytest.mark.asyncio
async def test_get_user_by_email_returns_none_when_not_found(
    db_session: AsyncSession,
):
    repository = UserRepository(db_session)

    result = await repository.get_by_email(
        "does-not-exist@example.com"
    )

    assert result is None

@pytest.mark.asyncio
async def test_exists_by_email(
    db_session: AsyncSession,
):
    repository = UserRepository(db_session)

    user = User(
        email="exists@example.com",
        password_hash="test_hash",
        first_name="Exists",
        last_name="Test",
        role=UserRole.CUSTOMER,
        is_active=True,
    )

    db_session.add(user)
    await db_session.flush()

    assert await repository.exists_by_email(
        "exists@example.com"
    )

    assert not await repository.exists_by_email(
        "missing@example.com"
    )

@pytest.mark.asyncio
async def test_create_user(
    db_session: AsyncSession,
):
    repository = UserRepository(db_session)

    user = User(
        email="create@example.com",
        password_hash="test_hash",
        first_name="Create",
        last_name="Test",
        role=UserRole.CUSTOMER,
        is_active=True,
    )

    result = await repository.create_user(user)

    assert result is user
    assert result.id is not None
    assert result.email == "create@example.com"

@pytest.mark.asyncio
async def test_update_user(
    db_session: AsyncSession,
):
    repository = UserRepository(db_session)

    user = User(
        email="update@example.com",
        password_hash="test_hash",
        first_name="Old",
        last_name="Name",
        role=UserRole.CUSTOMER,
        is_active=True,
    )

    db_session.add(user)
    await db_session.flush()

    user.first_name = "Updated"

    result = await repository.update_user(user)

    assert result.first_name == "Updated"

@pytest.mark.asyncio
async def test_delete_user(
    db_session: AsyncSession,
):
    repository = UserRepository(db_session)

    user = User(
        email="delete@example.com",
        password_hash="test_hash",
        first_name="Delete",
        last_name="Test",
        role=UserRole.CUSTOMER,
        is_active=True,
    )

    db_session.add(user)
    await db_session.flush()

    user_id = user.id

    await repository.delete_user(user)

    result = await repository.get_by_id(user_id)

    assert result is None