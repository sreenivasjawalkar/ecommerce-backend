from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
)
from app.application.users.service import UserService
from app.api.dependencies.services import get_user_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> RegisterResponse:

        user = await user_service.register_user(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
        )

        return RegisterResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: LoginRequest,
    user_service: Annotated[
         UserService,
         Depends(get_user_service)
    ],
) -> LoginResponse:

    access_token = await user_service.login_user(
        email=request.email,
        password=request.password,
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
    )

    