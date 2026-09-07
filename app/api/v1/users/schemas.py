from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.infrastructure.database.models.user import UserRole
class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    email: str
    first_name: str
    last_name: str

class UserProfileUpdateRequest(BaseModel):
    first_name: str| None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

class AdminUserUpdateRequest(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

class UserRoleUpdateRequest(BaseModel):
    role: UserRole

class UserStatusUpdateRequest(BaseModel):
    is_active: bool

class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
    pages: int

    

