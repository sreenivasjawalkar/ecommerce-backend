from app.core.security import (
    hash_password,
    verify_password,
)


def test_hash_password():
    password = "MySecurePassword123"

    password_hash = hash_password(password)

    assert password_hash != password
    assert password_hash.startswith("$argon2")


def test_verify_correct_password():
    password = "MySecurePassword123"

    password_hash = hash_password(password)

    assert verify_password(
        password,
        password_hash,
    )


def test_verify_wrong_password():
    password_hash = hash_password(
        "MySecurePassword123"
    )

    assert not verify_password(
        "WrongPassword123",
        password_hash,
    )


def test_same_password_generates_different_hashes():
    password = "MySecurePassword123"

    hash_1 = hash_password(password)
    hash_2 = hash_password(password)

    assert hash_1 != hash_2

    assert verify_password(password, hash_1)
    assert verify_password(password, hash_2)