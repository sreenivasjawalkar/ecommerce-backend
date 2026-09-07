from uuid import uuid4
from unittest.mock import AsyncMock

import pytest

from app.application.auth.service import AuthService
from app.core.exceptions import (
    AuthenticationError,
    InactiveUserError,
)
from app.core.security import create_access_token
from app.infrastructure.database.models.user import (
    User,
    UserRole,
)


@pytest.fixture
def user() -> User:
    return User(
        id=uuid4(),
        email="test@example.com",
        password_hash="test_hash",
        first_name="Test",
        last_name="User",
        role=UserRole.CUSTOMER,
        is_active=True,
    )


@pytest.fixture
def uow() -> AsyncMock:
    mock_uow = AsyncMock()
    mock_uow.users = AsyncMock()
    return mock_uow


@pytest.fixture
def auth_service(uow: AsyncMock) -> AuthService:
    return AuthService(uow)


@pytest.mark.asyncio
async def test_authenticate_with_valid_token(
    auth_service: AuthService,
    uow: AsyncMock,
    user: User,
) -> None:

    uow.users.get_by_id.return_value = user

    token = create_access_token(
        subject=str(user.id),
    )

    result = await auth_service.authenticate(token)

    assert result == user

    uow.users.get_by_id.assert_awaited_once_with(
        user.id,
    )


@pytest.mark.asyncio
async def test_authenticate_with_invalid_token(
    auth_service: AuthService,
) -> None:

    with pytest.raises(AuthenticationError):
        await auth_service.authenticate(
            "invalid-token",
        )


@pytest.mark.asyncio
async def test_authenticate_with_nonexistent_user(
    auth_service: AuthService,
    uow: AsyncMock,
) -> None:

    user_id = uuid4()

    uow.users.get_by_id.return_value = None

    token = create_access_token(
        subject=str(user_id),
    )

    with pytest.raises(AuthenticationError):
        await auth_service.authenticate(token)

    uow.users.get_by_id.assert_awaited_once_with(
        user_id,
    )


@pytest.mark.asyncio
async def test_authenticate_with_inactive_user(
    auth_service: AuthService,
    uow: AsyncMock,
    user: User,
) -> None:

    user.is_active = False

    uow.users.get_by_id.return_value = user

    token = create_access_token(
        subject=str(user.id),
    )

    with pytest.raises(InactiveUserError):
        await auth_service.authenticate(token)


@pytest.mark.asyncio
async def test_authenticate_with_malformed_subject(
    auth_service: AuthService,
) -> None:

    # This assumes your token creation/decode utilities
    # allow us to construct a token with an invalid UUID subject.

    from app.core.config import settings
    import jwt
    from datetime import datetime, timedelta, timezone

    now = datetime.now(timezone.utc)

    payload = {
        "sub": "not-a-valid-uuid",
        "iat": now,
        "exp": now + timedelta(minutes=15),
        "type": "access",
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    with pytest.raises(AuthenticationError):
        await auth_service.authenticate(token)