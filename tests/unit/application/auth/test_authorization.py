import pytest
from app.core.exceptions import AuthorizationError
from app.infrastructure.database.models.user import User, UserRole
from app.application.auth.authorization import AuthorizationService

def create_user(role: UserRole) -> User:
    return User(
        email=f"{role.value}@example.com",
        password_hash="hashed-password",
        first_name="Test",
        last_name="User",
        role=role,
        is_active=True,
    )

def test_admin_is_authorized_for_admin_role() -> None:
    user = create_user(UserRole.ADMIN)

    AuthorizationService.require_roles(
        user=user,
        allowed_roles=[UserRole.ADMIN],
    )

def test_customer_is_not_authorized_for_admin_role() -> None:
    user = create_user(UserRole.CUSTOMER)

    with pytest.raises(
        AuthorizationError,
        match="do not have permission",
    ):
        AuthorizationService.require_roles(
            user=user,
            allowed_roles=[UserRole.ADMIN],
        )

def test_customer_is_authorized_for_customer_role() -> None:
    user = create_user(UserRole.CUSTOMER)

    AuthorizationService.require_roles(
        user=user,
        allowed_roles=[UserRole.CUSTOMER],
    )

def test_multiple_roles_are_supported() -> None:
    user = create_user(UserRole.CUSTOMER)

    AuthorizationService.require_roles(
        user=user,
        allowed_roles=[
            UserRole.CUSTOMER,
            UserRole.ADMIN,
        ]
    )