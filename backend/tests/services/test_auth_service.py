from datetime import UTC

import pytest
from fastapi import HTTPException
from jose import jwt


def test_login_returns_token_for_valid_credentials(auth_service):
    token = auth_service.login("admin", "admin123")

    assert token is not None
    payload = jwt.decode(token, "test-secret", algorithms=["HS256"])
    assert payload["sub"] == "admin"


def test_login_returns_none_for_wrong_password(auth_service):
    assert auth_service.login("admin", "incorrecta") is None


def test_login_returns_none_for_wrong_username(auth_service):
    assert auth_service.login("otro", "admin123") is None


def test_verify_password_roundtrip(auth_service):
    hashed = auth_service._hash_password("secreto")

    assert auth_service.verify_password("secreto", hashed)
    assert not auth_service.verify_password("mal", hashed)


def test_create_access_token_has_subject_and_exp(auth_service):
    token = auth_service.create_access_token("admin")

    payload = jwt.decode(token, "test-secret", algorithms=["HS256"])
    assert payload["sub"] == "admin"
    assert "exp" in payload


def test_validate_token_returns_username(auth_service, settings):
    token = auth_service.create_access_token("admin")

    from fastapi.security import HTTPAuthorizationCredentials

    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    assert auth_service.validate_token(creds) == "admin"


def test_validate_token_rejects_invalid(auth_service):
    from fastapi.security import HTTPAuthorizationCredentials

    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials="token-basura")

    with pytest.raises(HTTPException) as exc_info:
        auth_service.validate_token(creds)
    assert exc_info.value.status_code == 401


def test_validate_token_rejects_other_user(auth_service):
    token = auth_service.create_access_token("hacker")

    from fastapi.security import HTTPAuthorizationCredentials

    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    with pytest.raises(HTTPException) as exc_info:
        auth_service.validate_token(creds)
    assert exc_info.value.status_code == 401


def test_expired_token_rejected(auth_service, settings):
    from datetime import datetime, timedelta

    from fastapi.security import HTTPAuthorizationCredentials
    from jose import jwt as _jwt

    expired = _jwt.encode(
        {
            "sub": "admin",
            "exp": datetime.now(UTC) - timedelta(minutes=5),
        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=expired)

    with pytest.raises(HTTPException) as exc_info:
        auth_service.validate_token(creds)
    assert exc_info.value.status_code == 401
