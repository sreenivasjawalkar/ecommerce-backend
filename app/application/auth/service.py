from uuid import UUID

from app.core.exceptions import (
    AuthenticationError,
    InactiveUserError,
)
from app.core.security import decode_access_token
from app.infrastructure.database.models.user import User
from app.infrastructure.database.unit_of_work import UnitOfWork
from jwt import ExpiredSignatureError, InvalidTokenError

class AuthService:
    def __init__(
            self,
            uow: UnitOfWork,
    ) -> None:
        self._uow = uow

    async def authenticate(
        self,
        token: str,
    ) -> User:

        user_id = self._get_user_id_from_token(token)

        user = await self._uow.users.get_by_id(user_id)

        if user is None:
            raise AuthenticationError(
                "User not found."
            )

        if not user.is_active:
            raise InactiveUserError()

        return user

    @staticmethod
    def _get_user_id_from_token(
        token: str,
    ) -> UUID:

        try:
            payload = decode_access_token(token)

        except ExpiredSignatureError as exc:
            raise AuthenticationError(
                "Access token has expired."
            ) from exc

        except InvalidTokenError as exc:
            raise AuthenticationError(
                "Invalid access token."
            ) from exc
        
        token_type = payload.get("type")

        if token_type != "access":
            raise AuthenticationError(
                "Invalid access token."
            )

        user_id = payload.get("sub")

        if user_id is None:
            raise AuthenticationError(
        "Invalid authentication credentials."
            )

        try:
            return UUID(str(user_id))

        except (ValueError, TypeError) as exc:
            raise AuthenticationError(
                "Invalid user identifier."
            ) from exc
