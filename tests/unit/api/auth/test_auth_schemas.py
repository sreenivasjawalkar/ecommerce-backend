import pytest
from pydantic import ValidationError
from app.api.v1.auth.schemas import RegisterRequest

def test_register_request_valid():
    request = RegisterRequest(
        email="user@example.com",
        password="strongpassword",
        first_name="sign",
        last_name="mighty"
    )

    assert request.email == "user@example.com"
    assert request.first_name == "sign"

def test_register_request_rejects_invalid_email():
    with pytest.raises(ValidationError):
        RegisterRequest(
            email="not-an-email",
            password="strongpassword",
            first_name="John",
            last_name="Doe",
        )

def test_register_request_rejects_short_password():
    with pytest.raises(ValidationError):
        RegisterRequest(
            email="user@example.com",
            password="short",
            first_name="John",
            last_name="Doe",
        )

def test_register_request_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        RegisterRequest(
            email="user@example.com",
            password="strongpassword",
            first_name="John",
            last_name="Doe",
            is_admin=True, # pyright: ignore[reportCallIssue]
        )