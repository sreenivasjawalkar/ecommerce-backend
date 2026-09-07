class ApplicationError(Exception):
    """
    Base exception for application-level errors.
    """

    def __init__(
            self,
            message: str,
            *,
            code: str,
    ) -> None:
        self.message = message
        self.code = code
        super().__init__(message)

class ResourceNotFoundError(ApplicationError):
    """
    Raised when a requested resource does not exist.
    """

    def __init__(
            self,
            resource: str,
            identifier: str,
    ) -> None:
        super().__init__(
            message=f"{resource} '{identifier}' was not found.",
            code="RESOURCE_NOT_FOUND",
        )

class ResourceAlreadyExistsError(ApplicationError):
    """
    Raised when attempting to create a resource that already exists.
    """
    def __init__(
            self,
            resource: str,
            identifier: str,
    ) -> None:
        super().__init__(
            message=f"{resource} '{identifier}' already exists.",
            code="RESOURCE_ALREADY_EXISTS",
        )

class AuthenticationError(ApplicationError):
    """
    Raised when authentication fails.
    """

    def __init__(
        self,
        message: str = "Authentication failed.",
    ) -> None:
        super().__init__(
            message=message,
            code="AUTHENTICATION_FAILED",
        )

class AuthorizationError(ApplicationError):
    """
    Raised when an authenticated user lacks permission.
    """

    def __init__(
        self,
        message: str = "You do not have permission to perform this action.",
    ) -> None:
        super().__init__(
            message=message,
            code="AUTHORIZATION_FAILED",
        )

class UserNotFoundError(ApplicationError):
    """
    Raised when a user cannot be found.
    """

    def __init__(
        self,
        user_id: str,
    ) -> None:
        super().__init__(
            message=f"User '{user_id}' was not found.",
            code="USER_NOT_FOUND",
        )


class InactiveUserError(AuthenticationError):
    """
    Raised when an inactive user attempts authentication.
    """

    def __init__(self) -> None:
        super().__init__(
            message="User account is inactive.",
        )