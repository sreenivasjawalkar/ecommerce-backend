from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class RegisterRequest(BaseModel):
    """
    Request body for user registration
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    email: EmailStr

    password: str = Field(min_length=8, max_length=128)

    first_name: str = Field(min_length=1, max_length=100)

    last_name: str = Field(min_length=1, max_length=100)

class RegisterResponse(BaseModel):
    """
    Response returned after successful registration.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    email: EmailStr
    first_name: str
    last_name: str

class LoginRequest(BaseModel):
    """
    Request body for user login
    """
    email: EmailStr

    password: str = Field(
        min_length=1,
        max_length=128,
    )
    model_config = ConfigDict(
        extra="forbid"
    )

class LoginResponse(BaseModel):
    """
    Response returned after successful authentication.
    """
    access_token: str
    token_type: str = "bearer"