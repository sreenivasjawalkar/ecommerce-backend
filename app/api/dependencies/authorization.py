from fastapi import Depends
from typing import Annotated
from collections.abc import Callable
from app.api.dependencies.auth import CurrentUser
from app.infrastructure.database.models.user import User, UserRole
from app.application.auth.authorization import AuthorizationService

def require_roles(
    *allowed_roles: UserRole,
) -> Callable:

    async def role_checker(
            current_user: CurrentUser,
    ) -> User:

        AuthorizationService.require_roles(
            user=current_user,
            allowed_roles=allowed_roles,
        )

        return current_user
    
    return role_checker