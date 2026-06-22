import pytest
from services.auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_password(self):
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password(self):
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_wrong_password(self):
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert verify_password("wrongpassword", hashed) is False


class TestTokenCreation:
    def test_create_access_token(self):
        data = {"sub": "user123", "role": "user"}
        token = create_access_token(data)
        assert token is not None
        assert len(token) > 0

    def test_create_refresh_token(self):
        data = {"sub": "user123"}
        token = create_refresh_token(data)
        assert token is not None
        assert len(token) > 0


class TestTokenDecoding:
    def test_decode_valid_token(self):
        data = {"sub": "user123", "role": "user"}
        token = create_access_token(data)
        decoded = decode_token(token)
        assert decoded is not None
        assert decoded["sub"] == "user123"
        assert decoded["type"] == "access"

    def test_decode_invalid_token(self):
        decoded = decode_token("invalid.token.here")
        assert decoded is None

    def test_decode_refresh_token(self):
        data = {"sub": "user123"}
        token = create_refresh_token(data)
        decoded = decode_token(token)
        assert decoded is not None
        assert decoded["sub"] == "user123"
        assert decoded["type"] == "refresh"
