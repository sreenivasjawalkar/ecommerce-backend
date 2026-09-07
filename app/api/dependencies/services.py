from typing import Annotated
from fastapi import Depends
from app.application.auth.service import AuthService
from app.application.users.service import UserService
from app.api.dependencies.unit_of_work import get_unit_of_work
from app.infrastructure.database.unit_of_work import UnitOfWork

def get_auth_service(
    uow: Annotated[
        UnitOfWork,
        Depends(get_unit_of_work),
    ],
) -> AuthService:
    return AuthService(uow)

def get_user_service(
        uow: Annotated[
            UnitOfWork,
            Depends(get_unit_of_work),
        ],
) -> UserService:

    return UserService(uow)
