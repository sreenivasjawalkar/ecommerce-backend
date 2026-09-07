import pytest
from app.core.security import create_access_token
from app.infrastructure.database.models.user import User, UserRole

@pytest.mark.asyncio
async def test_customer_cannot_access_admin_endpoint(
        client,
        db_session,
):
    user = User(
        email="customer@example.com",
        password_hash="hashed-password",
        first_name="Test",
        last_name="Customer",
        role=UserRole.CUSTOMER,
        is_active=True,
    )

    db_session.add(user)
    await db_session.flush()

    token = create_access_token(
        subject=str(user.id),
        )

    response = await client.get(
        "/api/v1/users/admin-only",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    print("STATUS:", response.status_code)
    print("BODY:", response.json())
    assert response.status_code == 403

    assert response.json() == {
        "error": {
            "code": "AUTHORIZATION_FAILED",
            "message": (
                "You do not have permission "
                "to perform this action."
            ),
        }
    }

@pytest.mark.asyncio
async def test_admin_can_access_admin_endpoint(
    client,
    db_session,
):
    user = User(
        email="admin@example.com",
        password_hash="hashed-password",
        first_name="Test",
        last_name="Admin",
        role=UserRole.ADMIN,
        is_active=True,
    )

    db_session.add(user)
    await db_session.flush()

    token = create_access_token(
        subject=str(user.id),
    )

    response = await client.get(
        "/api/v1/users/admin-only",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "You have administrator access.",
    }