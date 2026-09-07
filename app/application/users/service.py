from uuid import UUID
from app.core.exceptions import ResourceNotFoundError
from app.infrastructure.database.models.user import User, UserRole
from app.infrastructure.database.unit_of_work import UnitOfWork
from app.core.security import (
    hash_password,
    create_access_token,
    verify_password,

)
class UserService:
    """
    Application service responsible for user-related use cases.
    """
    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._uow = unit_of_work

    async def register_user(
            self,
            *,
            email: str,
            password: str,
            first_name: str,
            last_name: str,
    ) -> User:
        """
        Register a new customer.
        """

        # 1. Check whether the email is already registered.
        existing_user = await self._uow.users.get_by_email(email)

        if existing_user is not None:
            raise ValueError("User with this email already exists.")

        password_hash = hash_password(password)
        # 2. Create the User entity.
        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=UserRole.CUSTOMER,
            is_active=True

        )

        # 3. Persist through the repository
        await self._uow.users.create_user(user)

        # 4. Return the created entity
        return user

    async def login_user(
            self,
            *,
            email: str,
            password:str,
    ) -> str:

        user = await self._uow.users.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password.")

        if not user.is_active:
            raise ValueError("User account is inactive.")

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError("Invalid email or password.")

        return create_access_token(
            str(user.id)
        )

    async def get_current_user(
            self,
            user: User,
    ) -> User:
        return user

    async def update_profile(
            self,
            user: User,
            *,
            first_name: str | None,
            last_name: str | None,
    ) -> User:

        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        await self._uow.users.update_user(user)
        
        return user