from collections.abc import Iterable
from app.core.exceptions import AuthorizationError
from app.infrastructure.database.models.user import User, UserRole

class AuthorizationService:
    """
    Application service responsible for authorization decisions.
    """

    @staticmethod
    def require_roles(
        user: User,
        allowed_roles: Iterable[UserRole],
    ) -> None:
        """Require the authenticated user to have one of the allowed roles."""
        allowed_roles = set(allowed_roles)

        if user.role not in allowed_roles:
            raise AuthorizationError(
                "You do not have permission to perform this action."
            )
        