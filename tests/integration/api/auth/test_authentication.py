import jwt
import pytest
from uuid import uuid4
from httpx import AsyncClient
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from app.core.security import create_access_token
from app.infrastructure.database.models.user import (
    User,
    UserRole
)

@pytest.mark.asyncio
async def test_get_current_user_without_token(
    client: AsyncClient,
) -> None:

    response = await client.get("/api/v1/users/me")

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_with_invalid_token(
    client: AsyncClient,
) -> None:
    response = await client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_with_valid_token(
    client: AsyncClient,
    db_session,
) -> None:

    user = User(
        id=uuid4(),
        email="auth@example.com",
        password_hash="test_hash",
        first_name="Auth",
        last_name="Test",
        role=UserRole.CUSTOMER,
        is_active=True,
    )

    db_session.add(user)

    await db_session.flush()

    token = create_access_token(
        subject=str(user.id),
    )

    response = await client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(user.id)
    assert data["email"] == "auth@example.com"
    assert data["first_name"] == "Auth"
    assert data["last_name"] == "Test"

@pytest.mark.asyncio
async def test_get_current_user_when_user_does_not_exist(
    client: AsyncClient,
) -> None:

    token = create_access_token(
        subject=str(uuid4()),
    )

    response = await client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_when_user_is_inactive(
    client: AsyncClient,
    db_session,
) -> None:

    user = User(
        id=uuid4(),
        email="inactive@example.com",
        password_hash="test_hash",
        first_name="Inactive",
        last_name="User",
        role=UserRole.CUSTOMER,
        is_active=False,
    )

    db_session.add(user)

    await db_session.flush()

    token = create_access_token(
        subject=str(user.id),
    )

    response = await client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_current_user_with_malformed_token(
    client: AsyncClient,
) -> None:

    response = await client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "Bearer abc.def.xyz",
        },
    )

    assert response.status_code == 401
@pytest.mark.asyncio
async def test_get_current_user_with_wrong_token_type(
    client: AsyncClient,
    db_session,
) -> None:

    user = User(
        id=uuid4(),
        email="wrong-type@example.com",
        password_hash="test_hash",
        first_name="Wrong",
        last_name="Type",
        role=UserRole.CUSTOMER,
        is_active=True,
    )

    db_session.add(user)

    await db_session.flush()

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user.id),
        "iat": now,
        "exp": now + timedelta(minutes=15),
        "type": "refresh",
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    response = await client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_with_expired_token(
    client: AsyncClient,
) -> None:

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(uuid4()),
        "iat": now - timedelta(minutes=30),
        "exp": now - timedelta(minutes=15),
        "type": "access",
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    response = await client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 401