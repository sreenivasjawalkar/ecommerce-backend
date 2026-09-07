from typing import Annotated
from fastapi import APIRouter, Depends
from app.api.v1.users.schemas import UserResponse
from app.api.dependencies.auth import get_current_user
from app.api.dependencies.authorization import require_roles
from app.infrastructure.database.models.user import User, UserRole

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=UserResponse,)
async def get_me(
    current_user: Annotated[
        User,
        Depends(get_current_user)
    ]
) -> UserResponse:

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
    )

@router.get(
    "/admin-only",
    dependencies=[
        Depends(
            require_roles(UserRole.ADMIN)
        )
    ],
)
async def admin_only() -> dict[str, str]:

    return {
        "message": "You have administrator access.",
    }
    