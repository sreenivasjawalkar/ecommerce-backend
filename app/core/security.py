import jwt
from typing import Any
from argon2 import PasswordHasher
from app.core.config import settings
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta, timezone

_password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2id.
    """
    return _password_hasher.hash(password)

def verify_password(
        password: str,
        password_hash: str,
) -> bool:
    """
    Verify a plain-text password against an Argon2 password hash.
    """
    try: 
        return _password_hasher.verify(
            password_hash,
            password,
        )
    
    except VerifyMismatchError:
        return False

def create_access_token(subject: str) -> str:
    """
    Create a JWT access token

    'subject' identifies the authenticated user.
    """
    now = datetime.now(timezone.utc)

    expires_at = now + timedelta(
        minutes=settings.access_token_expire_minuites
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": expires_at,
        "type": "access"
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

def decode_access_token(
        token: str,
) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.
    """
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )