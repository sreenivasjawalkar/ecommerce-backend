from fastapi import Depends
from typing import Annotated
from app.application.auth.service import AuthService
from app.infrastructure.database.models.user import User
from app.api.dependencies.services import get_auth_service
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer()

async def get_current_user(
        credentials: Annotated[
            HTTPAuthorizationCredentials,
            Depends(bearer_scheme)
        ],
        auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
        ],
) -> User:

    return await auth_service.authenticate(
        credentials.credentials
        )

CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]



    




